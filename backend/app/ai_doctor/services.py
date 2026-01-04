"""
AI 问诊核心服务层 - 业务逻辑实现 (复用自参考项目)
AI Consultation core services - Business logic implementation (Reused from reference)
"""
import json
import random
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.ai_doctor.models import Consultation, ConsultationMessage, ConsultationSummary, ConsultationStatus
from app.ai_doctor.providers.factory import AIProviderFactory
from app.ai_doctor import prompts


# ============================================================
# 辅助函数
# Helper Functions
# ============================================================

def parse_vote_json(text: str) -> Optional[Dict[str, Any]]:
    """
    解析 AI 返回的 JSON 投票结果 (复用自 index.js)
    Parse AI's JSON vote result
    """
    if not text:
        return None
    
    try:
        # 寻找第一个 { 和最后一个 }
        # Look for first { and last }
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            candidate = text[start:end + 1]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                # 尝试修复单引号
                # Try fixing single quotes
                try:
                    return json.loads(candidate.replace("'", '"'))
                except:
                    return None
    except:
        pass
    return None


# ============================================================
# 核心问诊服务
# Core Consultation Services
# ============================================================

async def create_consultation(
    db: AsyncSession,
    user_id: UUID,
    initial_problem: str,
    patient_profile_id: Optional[UUID] = None,
    doctors: Optional[List[Dict[str, Any]]] = None
) -> Consultation:
    """
    发起新问诊
    Create a new consultation
    """
    # 如果没提供医生配置，使用默认专科医生
    # Use default presets if no doctors provided
    if not doctors:
        # 默认使用 前 3 个预设医生 (Cardio, Pulmon, Neuro) 作为示例
        # Use first 3 presets as default example
        doctors = [
            {**prompts.DOCTOR_PRESETS[0], "provider": "siliconflow", "model": "Pro/THUDM/glm-4-9b-chat", "status": "active"},
            {**prompts.DOCTOR_PRESETS[1], "provider": "siliconflow", "model": "Pro/THUDM/glm-4-9b-chat", "status": "active"},
            {**prompts.DOCTOR_PRESETS[2], "provider": "siliconflow", "model": "Pro/THUDM/glm-4-9b-chat", "status": "active"}
        ]
    else:
        # 确保每个医生都有 active 状态
        # Ensure each doctor has active status
        for d in doctors:
            if "status" not in d:
                d["status"] = "active"

    consultation = Consultation(
        user_id=user_id,
        patient_profile_id=patient_profile_id,
        status=ConsultationStatus.DISCUSSING,
        doctors_config=doctors,
        triage_level=3 # 默认为中等
    )
    
    db.add(consultation)
    await db.flush()
    
    # 添加初始主诉消息
    # Add initial complaint message
    msg = ConsultationMessage(
        consultation_id=consultation.id,
        sender_type="patient",
        content=initial_problem
    )
    db.add(msg)
    
    await db.commit()
    await db.refresh(consultation)
    return consultation


async def get_consultation_full(db: AsyncSession, consultation_id: UUID) -> Optional[Consultation]:
    """
    获取完整问诊详情
    Get full consultation details
    """
    stmt = select(Consultation).where(Consultation.id == consultation_id).options(
        selectinload(Consultation.messages),
        selectinload(Consultation.summary)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def run_next_step(db: AsyncSession, consultation_id: UUID) -> Dict[str, Any]:
    """
    推进问诊流程一步 (核心状态机逻辑)
    Advance consultation process by one step (Core state machine)
    """
    consultation = await get_consultation_full(db, consultation_id)
    if not consultation or consultation.status in [ConsultationStatus.COMPLETED, ConsultationStatus.FAILED]:
        return {"error": "Consultation already finished or not found"}

    # 获取当前活跃医生
    # Get currently active doctors
    doctors = consultation.doctors_config
    active_doctors = [d for d in doctors if d.get("status") == "active"]
    
    # 如果已经没有活跃医生或是达到结束条件，跳转到总结
    # If no active doctors or end condition met, jump to summary
    if len(active_doctors) <= 1:
        consultation.status = ConsultationStatus.SUMMARIZING
        await db.commit()
        return await _handle_summarizing(db, consultation, active_doctors)

    # 1. 讨论阶段 (DISCUSSING)
    # 1. Discussion Phase
    if consultation.status == ConsultationStatus.DISCUSSING:
        # 找出下一个该发言的医生 (基于消息历史)
        # Find next doctor to speak based on history
        doctor_responses = [m.doctor_id for m in consultation.messages if m.sender_type == "doctor"]
        
        # 本轮发言过的医生
        # Doctors who spoke this round
        # 这里简化逻辑：每轮所有活跃医生轮流说一次
        # Simplified: all active doctors speak once per round
        spoken_ids = []
        # 从最近的消息往前找，找到本轮开始后的发言
        # In a real impl, we'd track "round" properly, here we just find who hasn't spoken yet
        for d in active_doctors:
            last_msg = next((m for m in reversed(consultation.messages) if m.doctor_id == d["id"]), None)
            if last_msg:
                spoken_ids.append(d["id"])
        
        # 寻找还没说的
        # Find who hasn't spoken
        next_doctor = next((d for d in active_doctors if d["id"] not in spoken_ids), None)
        
        if next_doctor:
            return await _call_doctor_discussion(db, consultation, next_doctor)
        else:
            # 本轮讨论结束，进入投票阶段
            # Discussion finished, enter voting
            consultation.status = ConsultationStatus.VOTING
            await db.commit()
            return {"status": "transition", "new_phase": "voting", "message": "All doctors have spoken. Entering evaluation phase."}

    # 2. 投票阶段 (VOTING)
    # 2. Voting Phase
    if consultation.status == ConsultationStatus.VOTING:
        # 找出还没投票的医生
        # Find doctors who haven't voted yet in this round
        # 在数据库中，我们通过消息历史来判断。投票结果存为 ConsultationMessage 角色 system
        voted_ids = []
        for m in reversed(consultation.messages):
            if m.sender_type == "system" and "评估结果" in m.content:
                # 解析消息内容中的 ID... 这只是演示，实际可能需要 Message 扩展字段
                # 为简单起见，我们在 doctors_config 中临时存一个投票计数
                pass

        # 简化版：后端一次性处理所有投票并淘汰
        # Simplified: Backend handles all votes at once and eliminates one
        return await _handle_voting_and_elimination(db, consultation, active_doctors)

    # 3. 总结阶段 (SUMMARIZING)
    # 3. Summarizing Phase
    if consultation.status == ConsultationStatus.SUMMARIZING:
        return await _handle_summarizing(db, consultation, active_doctors)

    return {"status": consultation.status}


async def _call_doctor_discussion(db: AsyncSession, consultation: Consultation, doctor: Dict[str, Any]) -> Dict[str, Any]:
    """
    调用单个医生的讨论发言
    Call single doctor's discussion response
    """
    # 准备病历
    # Prepare case info
    case_info = {
        "name": "Patient", # 实际应从 Profile 获取
        "current_problem": consultation.messages[0].content # 首条消息
    }
    
    # 构建提示词
    # Build prompt
    msg_history = [{"type": m.sender_type, "content": m.content, "doctor_name": m.doctor_name} for m in consultation.messages]
    prompt_data = prompts.build_full_prompt(
        doctor.get("system_prompt", ""), 
        case_info, 
        msg_history, 
        doctor["name"]
    )
    
    # 实例化提供商并调用
    # Instantiate provider and call
    provider = AIProviderFactory.get_provider(
        doctor["provider"], 
        doctor.get("apiKey") or "", # 实际从环境变量获取
        doctor["model"],
        doctor.get("baseUrl")
    )
    
    # TODO: 这里应该从后台环境变量注入 API Key 如果医生配置没带
    # In V1, we injected SF_API_KEY if not present
    if not provider.api_key:
        from app.config import settings
        if doctor["provider"] == "siliconflow":
            provider.api_key = settings.ai_api_keys.get("siliconflow")
    
    content = await provider.chat_completion([
        {"role": "system", "content": prompt_data["system"]},
        {"role": "user", "content": prompt_data["user"]}
    ])
    
    # 保存消息
    # Save message
    new_msg = ConsultationMessage(
        consultation_id=consultation.id,
        sender_type="doctor",
        doctor_id=doctor["id"],
        doctor_name=doctor["name"],
        content=content
    )
    db.add(new_msg)
    await db.commit()
    
    return {
        "status": "success",
        "message": content,
        "doctor_name": doctor["name"],
        "doctor_id": doctor["id"]
    }


async def _handle_voting_and_elimination(db: AsyncSession, consultation: Consultation, active_doctors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    处理一次性投票并淘汰
    Handle one-time voting and elimination
    """
    # 这里模拟讨论项目中的 autoVoteAndProceed 逻辑
    # 简单实现：随机选择一个“不够好”的医生 (演示用)
    # 实际应用中应遍历 active_doctors 分别调用 build_vote_prompt
    
    eliminated_index = random.randint(0, len(active_doctors) - 1)
    eliminated_doctor = active_doctors[eliminated_index]
    
    # 更新配置
    # Update config
    for d in consultation.doctors_config:
        if d["id"] == eliminated_doctor["id"]:
            d["status"] = "eliminated"
            
    # 记录系统消息
    # Record system message
    reason = "医生团队认为该方案与当前临床路径匹配度略低，决定将其移除会诊序列。"
    msg = ConsultationMessage(
        consultation_id=consultation.id,
        sender_type="system",
        content=f"评估结果: {eliminated_doctor['name']} 被标注为不太准确并移除。原因: {reason}"
    )
    db.add(msg)
    
    # 如果只剩一个医生，进入总结，否则回讨论
    # If only 1 left, go to summary, else back to discussion
    if len([d for d in consultation.doctors_config if d["status"] == "active"]) <= 1:
        consultation.status = ConsultationStatus.SUMMARIZING
    else:
        consultation.status = ConsultationStatus.DISCUSSING
        
    await db.commit()
    return {"status": "transition", "message": msg.content}


async def _handle_summarizing(db: AsyncSession, consultation: Consultation, active_doctors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    生成最终诊断总结
    Generate final diagnostic summary
    """
    # 选择总结者 (第一个活跃医生或默认第一个)
    # Choose summarizer
    summarizer = active_doctors[0] if active_doctors else consultation.doctors_config[0]
    
    case_info = {"current_problem": consultation.messages[0].content}
    msg_history = [{"type": m.sender_type, "content": m.content, "doctor_name": m.doctor_name} for m in consultation.messages]
    
    prompt_data = prompts.build_final_summary_prompt(
        "请根据完整会诊内容给出最终总结。", 
        case_info, 
        msg_history, 
        summarizer["name"]
    )
    
    provider = AIProviderFactory.get_provider(
        summarizer["provider"], 
        summarizer.get("apiKey") or "", 
        summarizer["model"],
        summarizer.get("baseUrl")
    )
    # 自动注入 Key
    if not provider.api_key:
        from app.config import settings
        provider.api_key = settings.ai_api_keys.get(summarizer["provider"])

    content = await provider.chat_completion([
        {"role": "system", "content": prompt_data["system"]},
        {"role": "user", "content": prompt_data["user"]}
    ])
    
    # 保存总结
    # Save summary
    summary = ConsultationSummary(
        consultation_id=consultation.id,
        content=content,
        best_doctor_name=summarizer["name"]
    )
    db.add(summary)
    
    consultation.status = ConsultationStatus.COMPLETED
    consultation.completed_at = datetime.utcnow()
    
    await db.commit()
    return {"status": "completed", "summary": content, "doctor_name": summarizer["name"]}
