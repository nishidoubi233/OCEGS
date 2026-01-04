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
    # 统一 AI 配置 (OpenAI 兼容模式)
    # Unified AI Config (OpenAI Compatible Mode)
    {"key": "default_api_key", "description": "Default API Key for all AI calls", "is_secret": True},
    {"key": "default_base_url", "description": "Default Base URL (e.g., https://api.openai.com)", "is_secret": False},
    {"key": "default_model", "description": "Default Model Name (e.g., gpt-4, claude-3-opus)", "is_secret": False},
    
    # 分诊专用配置 (可选，留空则使用全局配置)
    # Triage-specific config (optional, uses global if empty)
    {"key": "triage_api_key", "description": "Triage-specific API Key (optional)", "is_secret": True},
    {"key": "triage_base_url", "description": "Triage-specific Base URL (optional)", "is_secret": False},
    {"key": "triage_model", "description": "Triage-specific Model (optional)", "is_secret": False},
    
    # Doctor Team Config (JSON) - 每个医生可覆盖 apiKey, baseUrl, model
    # Doctor Team Config (JSON) - Each doctor can override apiKey, baseUrl, model
    {"key": "doctors_config", "description": "JSON config for AI doctor team", "is_secret": False},
]
