"""
OCEGS Database Configuration
Async SQLAlchemy setup for PostgreSQL
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings


# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL queries in debug mode
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Base class for all database models"""
    pass


async def get_db() -> AsyncSession:
    """
    Dependency that provides a database session.
    Usage in FastAPI routes:
        async def my_route(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    初始化数据库表
    Initialize database tables.
    Called on application startup.
    """
    async with engine.begin() as conn:
        # 导入所有模型以确保它们被注册
        # Import all models here to ensure they're registered
        from app.users.models import User  # noqa: F401
        from app.patients.models import PatientProfile, MedicalHistory, EmergencyContact  # noqa: F401
        # etc.
        
        # 创建所有表（生产环境使用Alembic迁移）
        # Create all tables (use Alembic for production migrations)
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """
    Close database connections.
    Called on application shutdown.
    """
    await engine.dispose()
