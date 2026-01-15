"""
AI 问诊数据模式（Pydantic）
AI Consultation Pydantic schemas
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field
from app.ai_doctor.models import ConsultationStatus


class MessageBase(BaseModel):
    """
    会诊消息基础模式
    Consultation message base schema
    """
    sender_type: str = Field(..., pattern="^(patient|doctor|system)$")
    content: str
    doctor_id: Optional[str] = None
    doctor_name: Optional[str] = None


class MessageResponse(MessageBase):
    """
    会诊消息响应模式
    Consultation message response schema
    """
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class SummaryResponse(BaseModel):
    """
    会诊总结响应模式
    Consultation summary response schema
    """
    id: UUID
    content: str
    voting_details: Optional[Dict[str, Any]] = None
    best_doctor_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConsultationBase(BaseModel):
    """
    问诊会话基础模式
    Consultation session base schema
    """
    patient_profile_id: Optional[UUID] = None
    triage_level: int = 3


class ConsultationCreate(ConsultationBase):
    """
    创建问诊请求
    Create consultation request
    """
    # 讨论的初始问题
    # Initial problem for discussion
    initial_problem: str = Field(..., min_length=1, max_length=10000, description="Initial problem for discussion")
    # 医生列表 (默认从后端配置，或由前端指定)
    # List of doctors (default from backend or specified by frontend)
    doctors: Optional[List[Dict[str, Any]]] = None


class ConsultationResponse(ConsultationBase):
    """
    问诊会话响应模式
    Consultation session response schema
    """
    id: UUID
    user_id: UUID
    status: ConsultationStatus
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ConsultationFullResponse(ConsultationResponse):
    """
    完整问诊响应（含消息和总结）
    Full consultation response (with messages and summary)
    """
    messages: List[MessageResponse] = []
    summary: Optional[SummaryResponse] = None
    doctors_config: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes = True


class ConsultationStep(BaseModel):
    """
    单次会诊推进步骤模式
    Consultation single step pattern
    """
    content: str
    doctor_name: str
    doctor_id: str
    phase: ConsultationStatus


class FollowUpRequest(BaseModel):
    """
    用户追问请求
    User follow-up request
    """
    message: str = Field(..., min_length=1, description="Follow-up question or message")


class TriageRequest(BaseModel):
    """
    分诊请求
    Triage request
    """
    initial_problem: str = Field(..., min_length=1, max_length=10000, description="Initial problem for triage")


class TriageResponse(BaseModel):
    """
    分诊评估响应
    Triage evaluation response
    """
    severity: int = Field(..., ge=1, le=5)
    department: str
    is_emergency: bool
    emergency_advice: Optional[str] = None
    risks: List[str] = []
    summary: str

class EmergencyStep(BaseModel):
    """
    急救步骤条目
    Emergency step item
    """
    index: int
    action: str
    detail: str


class EmergencyGuideResponse(BaseModel):
    """
    急救指南响应
    Emergency guide response
    """
    title: str
    steps: List[EmergencyStep]
    warnings: List[str] = []
    prohibited: List[str] = []
