"""
管理模块
Admin Module
"""
from app.admin.router import router
from app.admin.models import SystemSetting, SETTING_KEYS
from app.admin.schemas import *
