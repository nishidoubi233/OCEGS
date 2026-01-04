"""
认证服务 - 用户注册、登录和密码管理
Authentication services - User registration, login and password management
"""
from typing import Optional
from uuid import UUID

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User, UserRole
from app.users.schemas import UserCreate


# 密码加密上下文 - 使用bcrypt
# Password hashing context - Using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    对密码进行哈希加密
    Hash a password using bcrypt
    
    Args:
        password: 明文密码 / Plain text password
    
    Returns:
        str: 加密后的密码哈希 / Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否匹配
    Verify if password matches the hash
    
    Args:
        plain_password: 明文密码 / Plain text password
        hashed_password: 存储的密码哈希 / Stored password hash
    
    Returns:
        bool: 密码是否匹配 / Whether password matches
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    通过邮箱查询用户
    Get user by email address
    
    Args:
        db: 数据库会话 / Database session
        email: 用户邮箱 / User email
    
    Returns:
        Optional[User]: 用户对象或None / User object or None
    """
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: UUID) -> Optional[User]:
    """
    通过ID查询用户
    Get user by ID
    
    Args:
        db: 数据库会话 / Database session
        user_id: 用户UUID / User UUID
    
    Returns:
        Optional[User]: 用户对象或None / User object or None
    """
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    user_data: UserCreate
) -> User:
    """
    创建新用户
    Create a new user account
    
    Args:
        db: 数据库会话 / Database session
        user_data: 用户注册数据 / User registration data
    
    Returns:
        User: 新创建的用户对象 / Newly created user object
    """
    # 加密密码
    # Hash the password
    hashed_password = hash_password(user_data.password)
    
    # 创建用户对象
    # Create user object
    user = User(
        email=user_data.email,
        password_hash=hashed_password,
        role=user_data.role or UserRole.PATIENT,
        is_active=True
    )
    
    # 保存到数据库
    # Save to database
    db.add(user)
    await db.flush()
    await db.refresh(user)
    
    return user


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str
) -> Optional[User]:
    """
    验证用户凭据
    Authenticate user credentials
    
    Args:
        db: 数据库会话 / Database session
        email: 用户邮箱 / User email
        password: 明文密码 / Plain text password
    
    Returns:
        Optional[User]: 认证成功返回用户，失败返回None
                       User if authenticated, None if failed
    """
    # 查询用户
    # Find user
    user = await get_user_by_email(db, email)
    
    if user is None:
        return None
    
    # 验证密码
    # Verify password
    if not verify_password(password, user.password_hash):
        return None
    
    # 检查账户是否激活
    # Check if account is active
    if not user.is_active:
        return None
    
    return user


async def update_user_password(
    db: AsyncSession,
    user: User,
    new_password: str
) -> User:
    """
    更新用户密码
    Update user password
    
    Args:
        db: 数据库会话 / Database session
        user: 用户对象 / User object
        new_password: 新密码 / New password
    
    Returns:
        User: 更新后的用户对象 / Updated user object
    """
    user.password_hash = hash_password(new_password)
    await db.flush()
    await db.refresh(user)
    return user
