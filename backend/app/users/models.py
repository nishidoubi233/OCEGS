"""
用户数据库模型
User database models for OCEGS authentication system
"""
import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class UserRole(str, PyEnum):
    """
    用户角色枚举
    User role enumeration for access control
    """
    PATIENT = "patient"         # 患者 - Patient user
    DOCTOR = "doctor"           # 医生 - Medical professional
    CARETAKER = "caretaker"     # 看护者 - Family caretaker
    ADMIN = "admin"             # 管理员 - System administrator


class User(Base):
    """
    用户模型 - 存储用户账户信息
    User model - Stores user account information for authentication
    """
    __tablename__ = "users"

    # 主键 - Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    # 邮箱 - 唯一标识符用于登录
    # Email - Unique identifier for login
    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    
    # 密码哈希 - 使用bcrypt加密存储
    # Password hash - Stored using bcrypt encryption
    password_hash = Column(
        String(255),
        nullable=False
    )
    
    # 用户角色 - 用于权限控制
    # User role - For access control
    role = Column(
        Enum(UserRole),
        default=UserRole.PATIENT,
        nullable=False
    )
    
    # 账户状态 - 可用于禁用账户
    # Account status - Can be used to disable accounts
    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )
    
    # 创建时间
    # Created timestamp
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    # 更新时间
    # Updated timestamp
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return f"<User {self.email}>"
