"""
认证依赖注入 - FastAPI依赖项
Authentication dependencies - FastAPI dependency injection
"""
from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.users.models import User, UserRole
from app.auth.jwt import verify_token
from app.auth.services import get_user_by_id


# HTTP Bearer认证方案
# HTTP Bearer authentication scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    获取当前登录用户 - 从JWT令牌中解析
    Get current logged-in user - Parse from JWT token
    
    Args:
        credentials: HTTP Bearer凭据 / HTTP Bearer credentials
        db: 数据库会话 / Database session
    
    Returns:
        User: 当前用户对象 / Current user object
    
    Raises:
        HTTPException: 认证失败时抛出401错误
                      Raises 401 on authentication failure
    """
    # 凭据未认证异常
    # Credentials not authenticated exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 验证令牌
    # Verify token
    token = credentials.credentials
    user_id = verify_token(token, token_type="access")
    
    if user_id is None:
        raise credentials_exception
    
    # 查询用户
    # Query user
    user = await get_user_by_id(db, user_id)
    
    if user is None:
        raise credentials_exception
    
    # 检查账户激活状态
    # Check account active status
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前活跃用户 - 确保用户账户处于激活状态
    Get current active user - Ensure user account is active
    
    Args:
        current_user: 当前用户 / Current user
    
    Returns:
        User: 活跃用户对象 / Active user object
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


def require_role(*allowed_roles: UserRole):
    """
    角色权限装饰器工厂 - 创建角色检查依赖
    Role permission decorator factory - Create role check dependency
    
    Args:
        *allowed_roles: 允许的角色列表 / List of allowed roles
    
    Returns:
        依赖函数 / Dependency function
    
    Example:
        @router.get("/admin-only")
        async def admin_endpoint(
            user: User = Depends(require_role(UserRole.ADMIN))
        ):
            return {"message": "Admin access granted"}
    """
    async def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        """
        检查用户角色
        Check user role
        """
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    
    return role_checker


# 便捷角色依赖
# Convenient role dependencies
require_patient = require_role(UserRole.PATIENT, UserRole.ADMIN)
require_doctor = require_role(UserRole.DOCTOR, UserRole.ADMIN)
require_caretaker = require_role(UserRole.CARETAKER, UserRole.ADMIN)
require_admin = require_role(UserRole.ADMIN)
