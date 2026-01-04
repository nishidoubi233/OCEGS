"""
管理面板数据模式 (Pydantic)
Admin Panel Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class AdminLoginRequest(BaseModel):
    """
    管理员登录请求
    Admin login request
    """
    password: str


class AdminLoginResponse(BaseModel):
    """
    管理员登录响应
    Admin login response
    """
    success: bool
    token: str = ""
    message: str = ""


class SettingBase(BaseModel):
    """
    系统设置基础模式
    System setting base schema
    """
    key: str
    value: str = ""
    description: Optional[str] = None


class SettingResponse(SettingBase):
    """
    系统设置响应 (隐藏敏感值)
    System setting response (mask sensitive values)
    """
    id: UUID
    is_secret: bool
    # 如果是敏感数据，返回掩码
    # If sensitive, return masked value
    display_value: str = ""
    updated_at: datetime

    class Config:
        from_attributes = True


class SettingUpdate(BaseModel):
    """
    更新系统设置
    Update system setting
    """
    value: str


class AIProviderConfig(BaseModel):
    """
    AI 供应商配置
    AI Provider configuration
    """
    provider: str = Field(..., pattern="^(openai|anthropic|gemini|siliconflow)$")
    api_key: str = ""
    base_url: Optional[str] = None
    model: str = ""


class DoctorConfig(BaseModel):
    """
    单个 AI 医生配置
    Single AI doctor configuration
    """
    id: str
    name: str
    name_cn: str
    provider: str = "siliconflow"
    model: str = "Pro/THUDM/glm-4-9b-chat"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    system_prompt: str = ""
    status: str = "active"


class DoctorsConfigUpdate(BaseModel):
    """
    更新医生团队配置
    Update doctors team configuration
    """
    doctors: List[DoctorConfig]


class SystemStatusResponse(BaseModel):
    """
    系统状态响应
    System status response
    """
    total_users: int = 0
    total_consultations: int = 0
    active_consultations: int = 0
    default_provider: str = "siliconflow"
    default_model: str = "Pro/THUDM/glm-4-9b-chat"
