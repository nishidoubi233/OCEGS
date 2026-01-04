"""
患者档案API路由
Patient profile API routes
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.users.models import User
from app.auth.dependencies import get_current_user
from app.patients.models import PatientProfile, MedicalHistory, EmergencyContact
from app.patients.schemas import (
    PatientProfileCreate,
    PatientProfileUpdate,
    PatientProfileResponse,
    PatientProfileFullResponse,
    MedicalHistoryCreate,
    MedicalHistoryUpdate,
    MedicalHistoryResponse,
    EmergencyContactCreate,
    EmergencyContactUpdate,
    EmergencyContactResponse
)
from app.patients import services


router = APIRouter()


# ============================================================
# 患者档案路由
# Patient Profile Routes
# ============================================================

@router.get(
    "/profile",
    response_model=PatientProfileFullResponse,
    summary="Get my profile",
    description="Get the current user's patient profile with medical history and emergency contacts"
)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的患者档案
    Get current user's patient profile
    """
    profile = await services.get_patient_profile_by_user_id(db, current_user.id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found. Please create one first."
        )
    
    return profile


@router.post(
    "/profile",
    response_model=PatientProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create my profile",
    description="Create a patient profile for the current user"
)
async def create_my_profile(
    profile_data: PatientProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建当前用户的患者档案
    Create patient profile for current user
    """
    # 检查是否已存在档案
    # Check if profile already exists
    existing = await services.get_patient_profile_by_user_id(db, current_user.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient profile already exists. Use PUT to update."
        )
    
    profile = await services.create_patient_profile(db, current_user.id, profile_data)
    await db.commit()
    
    return profile


@router.put(
    "/profile",
    response_model=PatientProfileResponse,
    summary="Update my profile",
    description="Update the current user's patient profile"
)
async def update_my_profile(
    profile_data: PatientProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新当前用户的患者档案
    Update current user's patient profile
    """
    profile = await services.get_patient_profile_by_user_id(db, current_user.id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found. Please create one first."
        )
    
    updated_profile = await services.update_patient_profile(db, profile, profile_data)
    await db.commit()
    
    return updated_profile


# ============================================================
# 病史路由
# Medical History Routes
# ============================================================

async def _get_patient_profile_or_404(
    db: AsyncSession,
    user_id: UUID
) -> PatientProfile:
    """
    辅助函数：获取患者档案或返回404
    Helper: Get patient profile or raise 404
    """
    profile = await services.get_patient_profile_by_user_id(db, user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found. Please create a profile first."
        )
    return profile


@router.get(
    "/medical-history",
    response_model=List[MedicalHistoryResponse],
    summary="Get my medical history",
    description="Get all medical history records for the current user"
)
async def get_my_medical_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的所有病史记录
    Get all medical history for current user
    """
    profile = await _get_patient_profile_or_404(db, current_user.id)
    histories = await services.get_medical_histories(db, profile.id)
    return histories


@router.post(
    "/medical-history",
    response_model=MedicalHistoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add medical history",
    description="Add a new medical history record"
)
async def add_medical_history(
    history_data: MedicalHistoryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    添加病史记录
    Add medical history record
    """
    profile = await _get_patient_profile_or_404(db, current_user.id)
    history = await services.create_medical_history(db, profile.id, history_data)
    await db.commit()
    
    return history


@router.put(
    "/medical-history/{history_id}",
    response_model=MedicalHistoryResponse,
    summary="Update medical history",
    description="Update a specific medical history record"
)
async def update_medical_history(
    history_id: UUID,
    history_data: MedicalHistoryUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新病史记录
    Update medical history record
    """
    profile = await _get_patient_profile_or_404(db, current_user.id)
    
    history = await services.get_medical_history_by_id(db, history_id)
    if not history or history.patient_id != profile.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical history record not found"
        )
    
    updated = await services.update_medical_history(db, history, history_data)
    await db.commit()
    
    return updated


@router.delete(
    "/medical-history/{history_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete medical history",
    description="Delete a specific medical history record"
)
async def delete_medical_history(
    history_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除病史记录
    Delete medical history record
    """
    profile = await _get_patient_profile_or_404(db, current_user.id)
    
    history = await services.get_medical_history_by_id(db, history_id)
    if not history or history.patient_id != profile.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical history record not found"
        )
    
    await services.delete_medical_history(db, history)
    await db.commit()


# ============================================================
# 紧急联系人路由
# Emergency Contact Routes
# ============================================================

@router.get(
    "/emergency-contacts",
    response_model=List[EmergencyContactResponse],
    summary="Get my emergency contacts",
    description="Get all emergency contacts for the current user"
)
async def get_my_emergency_contacts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户的所有紧急联系人
    Get all emergency contacts for current user
    """
    profile = await _get_patient_profile_or_404(db, current_user.id)
    contacts = await services.get_emergency_contacts(db, profile.id)
    return contacts


@router.post(
    "/emergency-contacts",
    response_model=EmergencyContactResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add emergency contact",
    description="Add a new emergency contact"
)
async def add_emergency_contact(
    contact_data: EmergencyContactCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    添加紧急联系人
    Add emergency contact
    """
    profile = await _get_patient_profile_or_404(db, current_user.id)
    contact = await services.create_emergency_contact(db, profile.id, contact_data)
    await db.commit()
    
    return contact


@router.put(
    "/emergency-contacts/{contact_id}",
    response_model=EmergencyContactResponse,
    summary="Update emergency contact",
    description="Update a specific emergency contact"
)
async def update_emergency_contact(
    contact_id: UUID,
    contact_data: EmergencyContactUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新紧急联系人
    Update emergency contact
    """
    profile = await _get_patient_profile_or_404(db, current_user.id)
    
    contact = await services.get_emergency_contact_by_id(db, contact_id)
    if not contact or contact.patient_id != profile.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency contact not found"
        )
    
    updated = await services.update_emergency_contact(db, contact, contact_data)
    await db.commit()
    
    return updated


@router.delete(
    "/emergency-contacts/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete emergency contact",
    description="Delete a specific emergency contact"
)
async def delete_emergency_contact(
    contact_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除紧急联系人
    Delete emergency contact
    """
    profile = await _get_patient_profile_or_404(db, current_user.id)
    
    contact = await services.get_emergency_contact_by_id(db, contact_id)
    if not contact or contact.patient_id != profile.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency contact not found"
        )
    
    await services.delete_emergency_contact(db, contact)
    await db.commit()
