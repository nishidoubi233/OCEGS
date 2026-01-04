"""
系统设置数据模型
System Settings Data Models
"""
from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.database import Base


class SystemSetting(Base):
    """
    系统设置表，用于存储 AI 供应商配置等
    System settings table for AI provider configs etc.
    """
    __tablename__ = "system_settings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 设置键名 (如 "openai_api_key", "default_model")
    # Setting key (e.g., "openai_api_key", "default_model")
    key = Column(String(100), unique=True, nullable=False, index=True)
    
    # 设置值 (加密存储敏感信息)
    # Setting value (encrypted for sensitive data)
    value = Column(Text, nullable=False, default="")
    
    # 是否为敏感数据 (如 API Key)
    # Whether this is sensitive data (like API Key)
    is_secret = Column(Boolean, default=False)
    
    # 设置描述
    # Setting description
    description = Column(String(255), nullable=True)
    
    # 时间戳
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# 预定义的系统设置键
# Predefined system setting keys
SETTING_KEYS = [
    # AI Providers
    {"key": "openai_api_key", "description": "OpenAI API Key", "is_secret": True},
    {"key": "openai_base_url", "description": "OpenAI Base URL (optional)", "is_secret": False},
    {"key": "anthropic_api_key", "description": "Anthropic API Key", "is_secret": True},
    {"key": "gemini_api_key", "description": "Google Gemini API Key", "is_secret": True},
    {"key": "siliconflow_api_key", "description": "SiliconFlow API Key", "is_secret": True},
    
    # Default Model Settings
    {"key": "default_provider", "description": "Default AI Provider (openai/anthropic/gemini/siliconflow)", "is_secret": False},
    {"key": "default_model", "description": "Default Model Name", "is_secret": False},
    
    # Doctor Team Config (JSON)
    {"key": "doctors_config", "description": "JSON config for AI doctor team", "is_secret": False},
]
