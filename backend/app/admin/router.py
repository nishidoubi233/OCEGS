"""
管理面板路由
Admin Panel Router
"""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from jose import jwt, JWTError
from datetime import datetime, timedelta
import json

from app.database import get_db
from app.config import settings
from app.admin import schemas
from app.admin.models import SystemSetting, SETTING_KEYS
from app.users.models import User
from app.ai_doctor.models import Consultation, ConsultationStatus


router = APIRouter(prefix="/admin", tags=["Admin"])

# 管理员 Token 有效期 (小时)
# Admin token validity (hours)
ADMIN_TOKEN_EXPIRE_HOURS = 24


def create_admin_token() -> str:
    """
    创建管理员访问令牌
    Create admin access token
    """
    expire = datetime.utcnow() + timedelta(hours=ADMIN_TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": "admin",
        "exp": expire,
        "type": "admin"
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def verify_admin_token(authorization: Optional[str] = Header(None)) -> bool:
    """
    验证管理员令牌
    Verify admin token
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Admin token required")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        if payload.get("type") != "admin":
            raise HTTPException(status_code=403, detail="Invalid admin token")
        return True
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired admin token")


@router.post("/login", response_model=schemas.AdminLoginResponse)
async def admin_login(req: schemas.AdminLoginRequest):
    """
    管理员登录
    Admin login with fixed password
    """
    if req.password == settings.admin_password:
        token = create_admin_token()
        return schemas.AdminLoginResponse(
            success=True,
            token=token,
            message="Login successful"
        )
    else:
        return schemas.AdminLoginResponse(
            success=False,
            token="",
            message="Invalid password"
        )


@router.get("/status", response_model=schemas.SystemStatusResponse)
async def get_system_status(
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_admin_token)
):
    """
    获取系统状态
    Get system status
    """
    # 统计用户数
    # Count users
    user_count = await db.scalar(select(func.count()).select_from(User))
    
    # 统计会诊数
    # Count consultations
    total_consultations = await db.scalar(select(func.count()).select_from(Consultation))
    active_consultations = await db.scalar(
        select(func.count()).select_from(Consultation).where(
            Consultation.status != ConsultationStatus.COMPLETED
        )
    )
    
    # 获取默认供应商配置
    # Get default provider config
    default_provider = "siliconflow"
    default_model = "Pro/THUDM/glm-4-9b-chat"
    
    provider_setting = await db.scalar(
        select(SystemSetting).where(SystemSetting.key == "default_provider")
    )
    if provider_setting and provider_setting.value:
        default_provider = provider_setting.value
        
    model_setting = await db.scalar(
        select(SystemSetting).where(SystemSetting.key == "default_model")
    )
    if model_setting and model_setting.value:
        default_model = model_setting.value
    
    return schemas.SystemStatusResponse(
        total_users=user_count or 0,
        total_consultations=total_consultations or 0,
        active_consultations=active_consultations or 0,
        default_provider=default_provider,
        default_model=default_model
    )


@router.get("/settings", response_model=List[schemas.SettingResponse])
async def get_all_settings(
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_admin_token)
):
    """
    获取所有系统设置
    Get all system settings
    """
    result = await db.execute(select(SystemSetting))
    settings_list = result.scalars().all()
    
    response = []
    for s in settings_list:
        display_value = s.value
        if s.is_secret and s.value:
            # 对敏感数据进行掩码
            # Mask sensitive data
            display_value = s.value[:4] + "****" + s.value[-4:] if len(s.value) > 8 else "****"
        
        response.append(schemas.SettingResponse(
            id=s.id,
            key=s.key,
            value=s.value if not s.is_secret else "",
            display_value=display_value,
            description=s.description,
            is_secret=s.is_secret,
            updated_at=s.updated_at
        ))
    
    return response


@router.put("/settings/{key}")
async def update_setting(
    key: str,
    update: schemas.SettingUpdate,
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_admin_token)
):
    """
    更新系统设置
    Update system setting
    """
    setting = await db.scalar(select(SystemSetting).where(SystemSetting.key == key))
    
    if not setting:
        # 如果不存在，查找预定义的设置并创建
        # If not exists, find predefined setting and create
        predefined = next((s for s in SETTING_KEYS if s["key"] == key), None)
        if not predefined:
            raise HTTPException(status_code=404, detail=f"Setting key '{key}' not found")
        
        setting = SystemSetting(
            key=key,
            value=update.value,
            is_secret=predefined.get("is_secret", False),
            description=predefined.get("description", "")
        )
        db.add(setting)
    else:
        setting.value = update.value
        setting.updated_at = datetime.utcnow()
    
    await db.commit()
    return {"success": True, "message": f"Setting '{key}' updated"}


@router.post("/init-settings")
async def init_settings(
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_admin_token)
):
    """
    初始化所有预定义设置
    Initialize all predefined settings
    """
    created = 0
    for preset in SETTING_KEYS:
        existing = await db.scalar(
            select(SystemSetting).where(SystemSetting.key == preset["key"])
        )
        if not existing:
            setting = SystemSetting(
                key=preset["key"],
                value="",
                is_secret=preset.get("is_secret", False),
                description=preset.get("description", "")
            )
            db.add(setting)
            created += 1
    
    await db.commit()
    return {"success": True, "message": f"Initialized {created} settings"}


@router.get("/doctors-config")
async def get_doctors_config(
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_admin_token)
):
    """
    获取医生团队配置
    Get doctors team configuration
    """
    setting = await db.scalar(
        select(SystemSetting).where(SystemSetting.key == "doctors_config")
    )
    
    if setting and setting.value:
        try:
            return {"doctors": json.loads(setting.value)}
        except json.JSONDecodeError:
            pass
    
    # 返回默认配置
    # Return default config
    from app.ai_doctor.prompts import DOCTOR_PRESETS
    return {"doctors": DOCTOR_PRESETS}


@router.put("/doctors-config")
async def update_doctors_config(
    update: schemas.DoctorsConfigUpdate,
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_admin_token)
):
    """
    更新医生团队配置
    Update doctors team configuration
    """
    setting = await db.scalar(
        select(SystemSetting).where(SystemSetting.key == "doctors_config")
    )
    
    doctors_json = json.dumps([d.model_dump() for d in update.doctors])
    
    if not setting:
        setting = SystemSetting(
            key="doctors_config",
            value=doctors_json,
            is_secret=False,
            description="JSON config for AI doctor team"
        )
        db.add(setting)
    else:
        setting.value = doctors_json
        setting.updated_at = datetime.utcnow()
    
    await db.commit()
    return {"success": True, "message": "Doctors config updated"}
