"""
AI 医生模块初始化
AI Doctor module initialization
"""
from app.ai_doctor.models import (
    Consultation,
    ConsultationMessage,
    ConsultationSummary,
    ConsultationStatus
)

__all__ = [
    "Consultation",
    "ConsultationMessage",
    "ConsultationSummary",
    "ConsultationStatus"
]
