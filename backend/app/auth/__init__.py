"""
认证模块初始化
Auth module initialization
"""
from app.auth.router import router
from app.auth.dependencies import (
    get_current_user,
    get_current_active_user,
    require_role,
    require_patient,
    require_doctor,
    require_caretaker,
    require_admin
)

__all__ = [
    "router",
    "get_current_user",
    "get_current_active_user",
    "require_role",
    "require_patient",
    "require_doctor",
    "require_caretaker",
    "require_admin"
]
