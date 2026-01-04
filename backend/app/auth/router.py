"""
认证API路由 - 注册、登录、令牌刷新
Authentication API routes - Register, login, token refresh
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.users.models import User
from app.users.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    RefreshTokenRequest,
    MessageResponse
)
from app.auth.services import (
    get_user_by_email,
    create_user,
    authenticate_user
)
from app.auth.jwt import create_tokens, verify_token
from app.auth.dependencies import get_current_user


router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account with email and password"
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    用户注册接口
    User registration endpoint
    
    - 验证邮箱是否已存在
    - 创建新用户账户
    - 返回用户信息（不含密码）
    
    - Check if email already exists
    - Create new user account
    - Return user info (without password)
    """
    # 检查邮箱是否已注册
    # Check if email is already registered
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 创建用户
    # Create user
    user = await create_user(db, user_data)
    await db.commit()
    
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="User login",
    description="Authenticate user and return JWT tokens"
)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录接口
    User login endpoint
    
    - 验证邮箱和密码
    - 生成访问令牌和刷新令牌
    - 返回令牌对
    
    - Verify email and password
    - Generate access and refresh tokens
    - Return token pair
    """
    # 验证用户凭据
    # Authenticate user credentials
    user = await authenticate_user(db, credentials.email, credentials.password)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 生成令牌
    # Generate tokens
    access_token, refresh_token = create_tokens(user.id)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh access token",
    description="Exchange refresh token for new access and refresh tokens"
)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    刷新令牌接口
    Token refresh endpoint
    
    - 验证刷新令牌
    - 生成新的令牌对
    - 返回新令牌
    
    - Verify refresh token
    - Generate new token pair
    - Return new tokens
    """
    # 验证刷新令牌
    # Verify refresh token
    user_id = verify_token(request.refresh_token, token_type="refresh")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户是否存在且激活
    # Check if user exists and is active
    from app.auth.services import get_user_by_id
    user = await get_user_by_id(db, user_id)
    
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # 生成新令牌
    # Generate new tokens
    access_token, new_refresh_token = create_tokens(user.id)
    
    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get information about the currently authenticated user"
)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户信息
    Get current user information
    
    - 需要有效的访问令牌
    - 返回当前用户详细信息
    
    - Requires valid access token
    - Returns current user details
    """
    return current_user


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="User logout",
    description="Logout current user (client should discard tokens)"
)
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    用户登出接口
    User logout endpoint
    
    注意：JWT是无状态的，服务端不存储令牌
    客户端应删除本地存储的令牌
    
    Note: JWT is stateless, server doesn't store tokens
    Client should delete locally stored tokens
    """
    # 实际登出由客户端处理（删除令牌）
    # Actual logout handled by client (deleting tokens)
    # 未来可实现令牌黑名单
    # Future: implement token blacklist
    
    return MessageResponse(
        message="Successfully logged out",
        success=True
    )
