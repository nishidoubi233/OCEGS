"""
AI 问诊会话模型
AI Consultation session models
"""
import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Dict, Any
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class ConsultationStatus(str, PyEnum):
    """
    问诊状态枚举
    Consultation status enumeration
    """
    TRIAGE = "triage"           # 预检分诊中
    DISCUSSING = "discussing"   # 医生讨论中
    VOTING = "voting"           # 投票评估中
    SUMMARIZING = "summarizing" # 总结报告中
    COMPLETED = "completed"     # 已完成
    FAILED = "failed"           # 失败


class Consultation(Base):
    """
    问诊会话模型
    Consultation session model
    """
    __tablename__ = "consultations"

    # 主键
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    # 关联用户
    # Associated user
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # 关联患者档案 (可选，如果用户还没创建档案)
    # Associated patient profile
    patient_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # 问诊状态
    # Consultation status
    status = Column(
        Enum(ConsultationStatus),
        default=ConsultationStatus.TRIAGE,
        nullable=False
    )
    
    # 分诊/严重等级 (1-5)
    # Triage/Severity level
    triage_level = Column(
        Integer,
        default=3
    )
    
    # 参与会诊的 AI 医生配置
    # AI doctors configuration for this consultation
    doctors_config = Column(
        JSON,
        nullable=True
    )
    
    # 创建时间
    # Created timestamp
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    # 完成时间
    # Completed timestamp
    completed_at = Column(
        DateTime,
        nullable=True
    )
    
    # 关系 - 对话历史
    # Relationship - Chat history
    messages = relationship(
        "ConsultationMessage",
        back_populates="consultation",
        cascade="all, delete-orphan",
        order_by="ConsultationMessage.created_at"
    )
    
    # 关系 - 最终总结
    # Relationship - Final summary
    summary = relationship(
        "ConsultationSummary",
        back_populates="consultation",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Consultation {self.id} (Status: {self.status})>"


class ConsultationMessage(Base):
    """
    问诊消息记录
    Consultation message record
    """
    __tablename__ = "consultation_messages"

    # 主键
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    # 关联问诊会话
    # Associated consultation session
    consultation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("consultations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # 消息发送者类型: patient, doctor, system
    # Sender type: patient, doctor, system
    sender_type = Column(
        String(20),
        nullable=False
    )
    
    # 医生 ID (如果是医生发言)
    # Doctor ID (if sender is a doctor)
    doctor_id = Column(
        String(50),
        nullable=True
    )
    
    # 医生姓名
    # Doctor name
    doctor_name = Column(
        String(100),
        nullable=True
    )
    
    # 消息内容
    # Message content
    content = Column(
        Text,
        nullable=False
    )
    
    # 创建时间
    # Created timestamp
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    # 关系 - 所属会话
    # Relationship - Parent consultation
    consultation = relationship(
        "Consultation",
        back_populates="messages"
    )


class ConsultationSummary(Base):
    """
    问诊最终总结报告
    Consultation final summary report
    """
    __tablename__ = "consultation_summaries"

    # 主键
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    # 关联问诊会话
    # Associated consultation session
    consultation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("consultations.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    
    # 总结内容 (Markdown 格式)
    # Summary content (Markdown format)
    content = Column(
        Text,
        nullable=False
    )
    
    # 参与投票情况
    # Voting details
    voting_details = Column(
        JSON,
        nullable=True
    )
    
    # 选出的最优方案建议者
    # The chosen best doctor/advisor
    best_doctor_name = Column(
        String(100),
        nullable=True
    )
    
    # 创建时间
    # Created timestamp
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    # 关系 - 所属会话
    # Relationship - Parent consultation
    consultation = relationship(
        "Consultation",
        back_populates="summary"
    )
