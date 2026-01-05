"""
AI 问诊 API 路由
AI Consultation API router
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.users.models import User
from app.ai_doctor import services, schemas

router = APIRouter(prefix="/consultations", tags=["AI Consultation"])


@router.post("/", response_model=schemas.ConsultationResponse, status_code=status.HTTP_201_CREATED)
async def start_new_consultation(
    req: schemas.ConsultationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    发起新的 AI 医生会诊
    Start a new AI doctor consultation
    """
    try:
        consultation = await services.create_consultation(
            db, 
            current_user.id, 
            req.initial_problem, 
            req.patient_profile_id,
            req.doctors
        )
        return consultation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{consultation_id}", response_model=schemas.ConsultationFullResponse)
async def get_consultation_details(
    consultation_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取问诊详情（含对话历史和总结）
    Get consultation details (with history and summary)
    """
    consultation = await services.get_consultation_full(db, consultation_id)
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    
    # 权限检查
    # Permission check
    if consultation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this consultation")
        
    return consultation


@router.post("/{consultation_id}/step", response_model=dict)
async def advance_consultation(
    consultation_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    推进问诊流程一步（由前端驱动或轮询调用）
    Advance consultation process by one step (driven by frontend or polling)
    """
    # 鉴权
    # Auth
    consultation = await services.get_consultation_full(db, consultation_id)
    if not consultation or consultation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    try:
        result = await services.run_next_step(db, consultation_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error advancing consultation: {str(e)}")


@router.post("/{consultation_id}/reply", response_model=dict)
async def send_follow_up(
    consultation_id: UUID,
    req: schemas.FollowUpRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    发送追问消息，让医生们回复
    Send follow-up message, have doctors respond
    """
    consultation = await services.get_consultation_full(db, consultation_id)
    if not consultation or consultation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    try:
        result = await services.handle_follow_up(db, consultation_id, req.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending follow-up: {str(e)}")



@router.get("/my/all", response_model=List[schemas.ConsultationResponse])
async def list_my_consultations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取我的所有问诊历史
    Get all my consultation history
    """
    from sqlalchemy import select
    from app.ai_doctor.models import Consultation
    
    stmt = select(Consultation).where(Consultation.user_id == current_user.id).order_by(Consultation.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/triage", response_model=schemas.TriageResponse)
async def perform_triage_evaluation(
    req: schemas.TriageRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    进行 AI 预检分诊评估
    Perform AI triage evaluation
    """
    try:
        result = await services.perform_triage(db, req.initial_problem)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing triage: {str(e)}")


@router.get("/{consultation_id}/emergency-guide", response_model=schemas.EmergencyGuideResponse)
async def get_emergency_guide(
    consultation_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取针对该会诊的急救指导
    Get targeted emergency guidance for this consultation
    """
    consultation = await services.get_consultation_full(db, consultation_id)
    if not consultation or consultation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    try:
        result = await services.generate_emergency_guide(db, consultation_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating emergency guide: {str(e)}")
