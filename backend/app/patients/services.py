"""
患者档案服务 - 业务逻辑处理
Patient profile services - Business logic handling
"""
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.patients.models import PatientProfile, MedicalHistory, EmergencyContact
from app.patients.schemas import (
    PatientProfileCreate,
    PatientProfileUpdate,
    MedicalHistoryCreate,
    MedicalHistoryUpdate,
    EmergencyContactCreate,
    EmergencyContactUpdate
)


# ============================================================
# 患者档案服务
# Patient Profile Services
# ============================================================

async def get_patient_profile_by_user_id(
    db: AsyncSession,
    user_id: UUID
) -> Optional[PatientProfile]:
    """
    通过用户ID查询患者档案
    Get patient profile by user ID
    
    Args:
        db: 数据库会话 / Database session
        user_id: 用户UUID / User UUID
    
    Returns:
        Optional[PatientProfile]: 患者档案或None / Patient profile or None
    """
    stmt = select(PatientProfile).where(
        PatientProfile.user_id == user_id
    ).options(
        selectinload(PatientProfile.medical_histories),
        selectinload(PatientProfile.emergency_contacts)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_patient_profile_by_id(
    db: AsyncSession,
    profile_id: UUID
) -> Optional[PatientProfile]:
    """
    通过档案ID查询患者档案
    Get patient profile by profile ID
    
    Args:
        db: 数据库会话 / Database session
        profile_id: 档案UUID / Profile UUID
    
    Returns:
        Optional[PatientProfile]: 患者档案或None / Patient profile or None
    """
    stmt = select(PatientProfile).where(
        PatientProfile.id == profile_id
    ).options(
        selectinload(PatientProfile.medical_histories),
        selectinload(PatientProfile.emergency_contacts)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_patient_profile(
    db: AsyncSession,
    user_id: UUID,
    profile_data: PatientProfileCreate
) -> PatientProfile:
    """
    创建患者档案
    Create patient profile
    
    Args:
        db: 数据库会话 / Database session
        user_id: 用户UUID / User UUID
        profile_data: 档案数据 / Profile data
    
    Returns:
        PatientProfile: 新创建的档案 / Newly created profile
    """
    profile = PatientProfile(
        user_id=user_id,
        full_name=profile_data.full_name,
        gender=profile_data.gender,
        date_of_birth=profile_data.date_of_birth,
        phone=profile_data.phone,
        address=profile_data.address
    )
    
    db.add(profile)
    await db.flush()
    await db.refresh(profile)
    
    return profile


async def update_patient_profile(
    db: AsyncSession,
    profile: PatientProfile,
    profile_data: PatientProfileUpdate
) -> PatientProfile:
    """
    更新患者档案
    Update patient profile
    
    Args:
        db: 数据库会话 / Database session
        profile: 现有档案 / Existing profile
        profile_data: 更新数据 / Update data
    
    Returns:
        PatientProfile: 更新后的档案 / Updated profile
    """
    update_dict = profile_data.model_dump(exclude_unset=True)
    
    for field, value in update_dict.items():
        setattr(profile, field, value)
    
    await db.flush()
    await db.refresh(profile)
    
    return profile


# ============================================================
# 病史服务
# Medical History Services
# ============================================================

async def get_medical_histories(
    db: AsyncSession,
    patient_id: UUID
) -> List[MedicalHistory]:
    """
    获取患者的所有病史记录
    Get all medical history records for a patient
    
    Args:
        db: 数据库会话 / Database session
        patient_id: 患者档案UUID / Patient profile UUID
    
    Returns:
        List[MedicalHistory]: 病史列表 / List of medical histories
    """
    stmt = select(MedicalHistory).where(
        MedicalHistory.patient_id == patient_id
    ).order_by(MedicalHistory.diagnosis_date.desc().nullsfirst())
    
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_medical_history_by_id(
    db: AsyncSession,
    history_id: UUID
) -> Optional[MedicalHistory]:
    """
    通过ID获取病史记录
    Get medical history by ID
    
    Args:
        db: 数据库会话 / Database session
        history_id: 病史UUID / History UUID
    
    Returns:
        Optional[MedicalHistory]: 病史记录或None / History or None
    """
    stmt = select(MedicalHistory).where(MedicalHistory.id == history_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_medical_history(
    db: AsyncSession,
    patient_id: UUID,
    history_data: MedicalHistoryCreate
) -> MedicalHistory:
    """
    创建病史记录
    Create medical history record
    
    Args:
        db: 数据库会话 / Database session
        patient_id: 患者档案UUID / Patient profile UUID
        history_data: 病史数据 / History data
    
    Returns:
        MedicalHistory: 新创建的病史 / Newly created history
    """
    history = MedicalHistory(
        patient_id=patient_id,
        condition=history_data.condition,
        diagnosis_date=history_data.diagnosis_date,
        status=history_data.status,
        notes=history_data.notes
    )
    
    db.add(history)
    await db.flush()
    await db.refresh(history)
    
    return history


async def update_medical_history(
    db: AsyncSession,
    history: MedicalHistory,
    history_data: MedicalHistoryUpdate
) -> MedicalHistory:
    """
    更新病史记录
    Update medical history record
    
    Args:
        db: 数据库会话 / Database session
        history: 现有病史 / Existing history
        history_data: 更新数据 / Update data
    
    Returns:
        MedicalHistory: 更新后的病史 / Updated history
    """
    update_dict = history_data.model_dump(exclude_unset=True)
    
    for field, value in update_dict.items():
        setattr(history, field, value)
    
    await db.flush()
    await db.refresh(history)
    
    return history


async def delete_medical_history(
    db: AsyncSession,
    history: MedicalHistory
) -> None:
    """
    删除病史记录
    Delete medical history record
    
    Args:
        db: 数据库会话 / Database session
        history: 病史记录 / History record
    """
    await db.delete(history)
    await db.flush()


# ============================================================
# 紧急联系人服务
# Emergency Contact Services
# ============================================================

async def get_emergency_contacts(
    db: AsyncSession,
    patient_id: UUID
) -> List[EmergencyContact]:
    """
    获取患者的所有紧急联系人
    Get all emergency contacts for a patient
    
    Args:
        db: 数据库会话 / Database session
        patient_id: 患者档案UUID / Patient profile UUID
    
    Returns:
        List[EmergencyContact]: 紧急联系人列表 / List of emergency contacts
    """
    stmt = select(EmergencyContact).where(
        EmergencyContact.patient_id == patient_id
    ).order_by(EmergencyContact.created_at)
    
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_emergency_contact_by_id(
    db: AsyncSession,
    contact_id: UUID
) -> Optional[EmergencyContact]:
    """
    通过ID获取紧急联系人
    Get emergency contact by ID
    
    Args:
        db: 数据库会话 / Database session
        contact_id: 联系人UUID / Contact UUID
    
    Returns:
        Optional[EmergencyContact]: 紧急联系人或None / Contact or None
    """
    stmt = select(EmergencyContact).where(EmergencyContact.id == contact_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_emergency_contact(
    db: AsyncSession,
    patient_id: UUID,
    contact_data: EmergencyContactCreate
) -> EmergencyContact:
    """
    创建紧急联系人
    Create emergency contact
    
    Args:
        db: 数据库会话 / Database session
        patient_id: 患者档案UUID / Patient profile UUID
        contact_data: 联系人数据 / Contact data
    
    Returns:
        EmergencyContact: 新创建的联系人 / Newly created contact
    """
    contact = EmergencyContact(
        patient_id=patient_id,
        name=contact_data.name,
        relation_to_patient=contact_data.relationship,
        phone=contact_data.phone,
        is_caretaker=contact_data.is_caretaker
    )
    
    db.add(contact)
    await db.flush()
    await db.refresh(contact)
    
    return contact


async def update_emergency_contact(
    db: AsyncSession,
    contact: EmergencyContact,
    contact_data: EmergencyContactUpdate
) -> EmergencyContact:
    """
    更新紧急联系人
    Update emergency contact
    
    Args:
        db: 数据库会话 / Database session
        contact: 现有联系人 / Existing contact
        contact_data: 更新数据 / Update data
    
    Returns:
        EmergencyContact: 更新后的联系人 / Updated contact
    """
    update_dict = contact_data.model_dump(exclude_unset=True)
    
    for field, value in update_dict.items():
        setattr(contact, field, value)
    
    await db.flush()
    await db.refresh(contact)
    
    return contact


async def delete_emergency_contact(
    db: AsyncSession,
    contact: EmergencyContact
) -> None:
    """
    删除紧急联系人
    Delete emergency contact
    
    Args:
        db: 数据库会话 / Database session
        contact: 联系人 / Contact
    """
    await db.delete(contact)
    await db.flush()
