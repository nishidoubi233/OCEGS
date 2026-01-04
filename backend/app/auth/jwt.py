"""
JWT令牌工具 - 生成和验证JSON Web Tokens
JWT token utilities - Generate and verify JSON Web Tokens
"""
from datetime import datetime, timedelta
from typing import Optional, Tuple
from uuid import UUID

from jose import jwt, JWTError
from app.config import settings


# JWT配置
# JWT Configuration
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days


def create_access_token(
    user_id: UUID,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    创建访问令牌
    Create access token for user authentication
    
    Args:
        user_id: 用户UUID / User UUID
        expires_delta: 过期时间增量 / Expiration time delta
    
    Returns:
        str: JWT访问令牌 / JWT access token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 令牌载荷
    # Token payload
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access",
        "iat": datetime.utcnow()
    }
    
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=ALGORITHM)


def create_refresh_token(
    user_id: UUID,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    创建刷新令牌 - 用于获取新的访问令牌
    Create refresh token - Used to obtain new access tokens
    
    Args:
        user_id: 用户UUID / User UUID
        expires_delta: 过期时间增量 / Expiration time delta
    
    Returns:
        str: JWT刷新令牌 / JWT refresh token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    # 令牌载荷
    # Token payload
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh",
        "iat": datetime.utcnow()
    }
    
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=ALGORITHM)


def create_tokens(user_id: UUID) -> Tuple[str, str]:
    """
    创建访问令牌和刷新令牌对
    Create both access and refresh tokens
    
    Args:
        user_id: 用户UUID / User UUID
    
    Returns:
        Tuple[str, str]: (访问令牌, 刷新令牌) / (access_token, refresh_token)
    """
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    return access_token, refresh_token


def verify_token(token: str, token_type: str = "access") -> Optional[UUID]:
    """
    验证JWT令牌并返回用户ID
    Verify JWT token and return user ID
    
    Args:
        token: JWT令牌字符串 / JWT token string
        token_type: 令牌类型 ("access" 或 "refresh") / Token type
    
    Returns:
        Optional[UUID]: 用户ID（验证成功）或 None（验证失败）
                       User ID if valid, None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[ALGORITHM]
        )
        
        # 验证令牌类型
        # Verify token type
        if payload.get("type") != token_type:
            return None
        
        # 提取用户ID
        # Extract user ID
        user_id_str = payload.get("sub")
        if user_id_str is None:
            return None
        
        return UUID(user_id_str)
        
    except JWTError:
        return None
    except ValueError:
        # UUID解析失败
        # UUID parsing failed
        return None


def decode_token(token: str) -> Optional[dict]:
    """
    解码JWT令牌（不验证过期）
    Decode JWT token (without expiration validation)
    
    Args:
        token: JWT令牌字符串 / JWT token string
    
    Returns:
        Optional[dict]: 令牌载荷 / Token payload
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[ALGORITHM],
            options={"verify_exp": False}
        )
        return payload
    except JWTError:
        return None
