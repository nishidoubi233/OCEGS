"""
用户数据模式（Pydantic）
User Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from app.users.models import UserRole


# ============================================================
# 基础模式
# Base Schemas
# ============================================================

class UserBase(BaseModel):
    """
    用户基础模式 - 共享字段
    User base schema - Shared fields
    """
    email: EmailStr = Field(..., description="User email address")


# ============================================================
# 请求模式
# Request Schemas
# ============================================================

class UserCreate(UserBase):
    """
    用户注册请求模式
    User registration request schema
    """
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password (min 8 characters)"
    )
    role: Optional[UserRole] = Field(
        default=UserRole.PATIENT,
        description="User role (default: patient)"
    )


class UserLogin(BaseModel):
    """
    用户登录请求模式
    User login request schema
    """
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserUpdate(BaseModel):
    """
    用户更新请求模式
    User update request schema
    """
    email: Optional[EmailStr] = Field(None, description="New email address")
    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=100,
        description="New password"
    )
    is_active: Optional[bool] = Field(None, description="Account status")


# ============================================================
# 响应模式
# Response Schemas
# ============================================================

class UserResponse(UserBase):
    """
    用户响应模式 - 返回给客户端
    User response schema - Returned to client
    """
    id: UUID
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """
    用户简要信息 - 用于显示
    User brief info - For display purposes
    """
    id: UUID
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True


# ============================================================
# 认证相关模式
# Authentication Schemas
# ============================================================

class Token(BaseModel):
    """
    JWT令牌响应模式
    JWT token response schema
    """
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenPayload(BaseModel):
    """
    JWT令牌载荷模式
    JWT token payload schema
    """
    sub: str = Field(..., description="Subject (user ID)")
    exp: datetime = Field(..., description="Expiration time")
    type: str = Field(..., description="Token type (access/refresh)")


class RefreshTokenRequest(BaseModel):
    """
    刷新令牌请求模式
    Refresh token request schema
    """
    refresh_token: str = Field(..., description="Refresh token to exchange")


class MessageResponse(BaseModel):
    """
    通用消息响应模式
    Generic message response schema
    """
    message: str = Field(..., description="Response message")
    success: bool = Field(default=True, description="Operation success status")
