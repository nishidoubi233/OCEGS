"""
患者档案数据库模型
Patient profile database models for OCEGS health records
"""
import uuid
from datetime import date, datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Boolean, Date, DateTime, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Gender(str, PyEnum):
    """
    性别枚举
    Gender enumeration
    """
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class MedicalConditionStatus(str, PyEnum):
    """
    病情状态枚举
    Medical condition status enumeration
    """
    ACTIVE = "active"           # 活跃/进行中
    RESOLVED = "resolved"       # 已解决/治愈
    CHRONIC = "chronic"         # 慢性病
    MANAGED = "managed"         # 控制中


class PatientProfile(Base):
    """
    患者档案模型 - 存储患者基本信息
    Patient profile model - Stores basic patient information
    """
    __tablename__ = "patient_profiles"

    # 主键
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    # 关联用户 - 一对一关系
    # Associated user - One-to-one relationship
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True
    )
    
    # 全名
    # Full name
    full_name = Column(
        String(255),
        nullable=False
    )
    
    # 性别
    # Gender
    gender = Column(
        Enum(Gender),
        nullable=True
    )
    
    # 出生日期
    # Date of birth
    date_of_birth = Column(
        Date,
        nullable=True
    )
    
    # 电话号码
    # Phone number
    phone = Column(
        String(50),
        nullable=True
    )
    
    # 地址
    # Address
    address = Column(
        Text,
        nullable=True
    )
    
    # 创建时间
    # Created timestamp
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    # 更新时间
    # Updated timestamp
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # 关系 - 病史记录
    # Relationship - Medical history records
    medical_histories = relationship(
        "MedicalHistory",
        back_populates="patient",
        cascade="all, delete-orphan"
    )
    
    # 关系 - 紧急联系人
    # Relationship - Emergency contacts
    emergency_contacts = relationship(
        "EmergencyContact",
        back_populates="patient",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<PatientProfile {self.full_name}>"


class MedicalHistory(Base):
    """
    病史记录模型 - 存储患者的疾病历史
    Medical history model - Stores patient's disease history
    """
    __tablename__ = "medical_histories"

    # 主键
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    # 关联患者档案
    # Associated patient profile
    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # 疾病/病症名称
    # Condition/disease name
    condition = Column(
        String(255),
        nullable=False
    )
    
    # 诊断日期
    # Diagnosis date
    diagnosis_date = Column(
        Date,
        nullable=True
    )
    
    # 病情状态
    # Condition status
    status = Column(
        Enum(MedicalConditionStatus),
        default=MedicalConditionStatus.ACTIVE,
        nullable=False
    )
    
    # 备注
    # Notes
    notes = Column(
        Text,
        nullable=True
    )
    
    # 创建时间
    # Created timestamp
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    # 更新时间
    # Updated timestamp
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # 关系 - 所属患者
    # Relationship - Parent patient
    patient = relationship(
        "PatientProfile",
        back_populates="medical_histories"
    )

    def __repr__(self):
        return f"<MedicalHistory {self.condition}>"


class EmergencyContact(Base):
    """
    紧急联系人模型 - 存储患者的紧急联系人信息
    Emergency contact model - Stores patient's emergency contact information
    """
    __tablename__ = "emergency_contacts"

    # 主键
    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    # 关联患者档案
    # Associated patient profile
    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # 联系人姓名
    # Contact name
    name = Column(
        String(255),
        nullable=False
    )
    
    # 与患者的关系
    # Relationship to patient
    relation_to_patient = Column(
        String(100),
        nullable=False
    )
    
    # 电话号码
    # Phone number
    phone = Column(
        String(50),
        nullable=False
    )
    
    # 是否为看护者（可接收通知）
    # Is caretaker (can receive notifications)
    is_caretaker = Column(
        Boolean,
        default=False,
        nullable=False
    )
    
    # 创建时间
    # Created timestamp
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    # 更新时间
    # Updated timestamp
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # 关系 - 所属患者
    # Relationship - Parent patient
    patient = relationship(
        "PatientProfile",
        back_populates="emergency_contacts"
    )

    def __repr__(self):
        return f"<EmergencyContact {self.name} ({self.relation_to_patient})>"
