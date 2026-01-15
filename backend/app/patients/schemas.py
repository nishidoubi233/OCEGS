"""
患者档案数据模式（Pydantic）
Patient profile Pydantic schemas for request/response validation
"""
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from app.patients.models import Gender, MedicalConditionStatus


# ============================================================
# 共用验证函数
# Shared Validation Functions
# ============================================================

def validate_name(value: str) -> str:
    """
    验证姓名：不能为纯空格，必须包含至少一个字母（支持中英文及其他语言）
    Validate name: cannot be whitespace-only, must contain at least one letter
    """
    if not value or not value.strip():
        raise ValueError("Name cannot be empty or whitespace-only")
    
    stripped = value.strip()
    
    # 检查是否为纯数字
    # Check if purely numeric
    if stripped.isdigit():
        raise ValueError("Name cannot be purely numeric")
    
    # 检查是否包含至少一个字母（使用 unicodedata 检测 Unicode 字母类别）
    # Check for at least one letter using unicodedata
    import unicodedata
    has_letter = any(unicodedata.category(c).startswith('L') for c in stripped)
    
    if not has_letter:
        raise ValueError("Name must contain at least one letter")
    
    return stripped


# ============================================================
# 患者档案模式
# Patient Profile Schemas
# ============================================================

class PatientProfileBase(BaseModel):
    """
    患者档案基础模式
    Patient profile base schema
    """
    full_name: str = Field(..., min_length=1, max_length=255, description="Full name")
    gender: Optional[Gender] = Field(None, description="Gender")
    date_of_birth: Optional[date] = Field(None, description="Date of birth")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    address: Optional[str] = Field(None, description="Address")

    # 姓名验证器
    # Name validator
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        return validate_name(v)


class PatientProfileCreate(PatientProfileBase):
    """
    创建患者档案请求模式
    Create patient profile request schema
    """
    pass


class PatientProfileUpdate(BaseModel):
    """
    更新患者档案请求模式
    Update patient profile request schema
    """
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    gender: Optional[Gender] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = None

    # 姓名验证器 (仅当提供时验证)
    # Name validator (only validate when provided)
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return validate_name(v)
        return v


class PatientProfileResponse(PatientProfileBase):
    """
    患者档案响应模式
    Patient profile response schema
    """
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# 病史模式
# Medical History Schemas
# ============================================================

class MedicalHistoryBase(BaseModel):
    """
    病史基础模式
    Medical history base schema
    """
    condition: str = Field(..., min_length=1, max_length=255, description="Condition name")
    diagnosis_date: Optional[date] = Field(None, description="Diagnosis date")
    status: MedicalConditionStatus = Field(
        default=MedicalConditionStatus.ACTIVE,
        description="Condition status"
    )
    notes: Optional[str] = Field(None, description="Additional notes")


class MedicalHistoryCreate(MedicalHistoryBase):
    """
    创建病史请求模式
    Create medical history request schema
    """
    pass


class MedicalHistoryUpdate(BaseModel):
    """
    更新病史请求模式
    Update medical history request schema
    """
    condition: Optional[str] = Field(None, min_length=1, max_length=255)
    diagnosis_date: Optional[date] = None
    status: Optional[MedicalConditionStatus] = None
    notes: Optional[str] = None


class MedicalHistoryResponse(MedicalHistoryBase):
    """
    病史响应模式
    Medical history response schema
    """
    id: UUID
    patient_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# 紧急联系人模式
# Emergency Contact Schemas
# ============================================================

class EmergencyContactBase(BaseModel):
    """
    紧急联系人基础模式
    Emergency contact base schema
    """
    name: str = Field(..., min_length=1, max_length=255, description="Contact name")
    relationship: str = Field(..., min_length=1, max_length=100, description="Relationship")
    phone: str = Field(..., min_length=1, max_length=50, description="Phone number")
    is_caretaker: bool = Field(default=False, description="Is caretaker (receives notifications)")

    # 姓名验证器
    # Name validator
    @field_validator('name')
    @classmethod
    def validate_contact_name(cls, v: str) -> str:
        return validate_name(v)


class EmergencyContactCreate(EmergencyContactBase):
    """
    创建紧急联系人请求模式
    Create emergency contact request schema
    """
    pass


class EmergencyContactUpdate(BaseModel):
    """
    更新紧急联系人请求模式
    Update emergency contact request schema
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    relationship: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=1, max_length=50)
    is_caretaker: Optional[bool] = None

    # 姓名验证器 (仅当提供时验证)
    # Name validator (only validate when provided)
    @field_validator('name')
    @classmethod
    def validate_contact_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return validate_name(v)
        return v


class EmergencyContactResponse(BaseModel):
    """
    紧急联系人响应模式
    Emergency contact response schema
    """
    id: UUID
    patient_id: UUID
    name: str
    relationship: str = Field(..., alias="relation_to_patient")
    phone: str
    is_caretaker: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


# ============================================================
# 完整患者档案响应（含病史和紧急联系人）
# Complete Patient Profile Response (with history and contacts)
# ============================================================

class PatientProfileFullResponse(PatientProfileBase):
    """
    完整患者档案响应 - 包含病史和紧急联系人
    Complete patient profile response - Includes medical history and emergency contacts
    """
    id: UUID
    user_id: UUID
    medical_histories: List[MedicalHistoryResponse] = []
    emergency_contacts: List[EmergencyContactResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
