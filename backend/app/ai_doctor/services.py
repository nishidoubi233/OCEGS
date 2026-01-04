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

async def perform_triage(db: AsyncSession, initial_problem: str, patient_profile: dict = None) -> Dict[str, Any]:
    """
    进行 AI 分诊评估，包含用户资料和医生分配
    Perform AI triage evaluation with patient profile and doctor assignment
    """
    prompt_data = prompts.build_triage_prompt(initial_problem, patient_profile)
    
    # 从 SystemSetting 获取分诊配置 (优先使用专用配置，否则回退全局)
    # Get triage config (prefer triage-specific, fallback to global)
    from app.admin.models import SystemSetting
    stmt = select(SystemSetting).where(SystemSetting.key.in_([
        "default_api_key", "default_base_url", "default_model",
        "triage_api_key", "triage_base_url", "triage_model"
    ]))
    result = await db.execute(stmt)
    settings_list = result.scalars().all()
    settings_map = {s.key: s.value for s in settings_list}
    
    # 优先使用分诊专用配置
    # Prefer triage-specific settings
    api_key = settings_map.get("triage_api_key") or settings_map.get("default_api_key", "")
    base_url = settings_map.get("triage_base_url") or settings_map.get("default_base_url", "")
    model = settings_map.get("triage_model") or settings_map.get("default_model", "gpt-3.5-turbo")
    
    # 使用 OpenAI 兼容模式
    # Use OpenAI compatible mode
    provider = AIProviderFactory.get_provider("openai", api_key, model, base_url)
    
    content = await provider.chat_completion([
        {"role": "system", "content": prompt_data["system"]},
        {"role": "user", "content": prompt_data["user"]}
    ])
    
    result = parse_vote_json(content) # 复用 JSON 解析逻辑
    if not result:
        # 回退默认值
        # Fallback default
        result = {
            "severity": 3,
            "department": "General Medicine",
            "is_emergency": False,
            "emergency_advice": "Please consult a doctor soon.",
            "risks": ["Unable to assess specific risks"],
            "summary": "AI was unable to parse triage results clearly.",
            "assigned_doctors": ["pulmonologist"]  # Default fallback doctor
        }
    
    # 确保有 assigned_doctors 字段
    # Ensure assigned_doctors field exists
    if "assigned_doctors" not in result or not result["assigned_doctors"]:
        result["assigned_doctors"] = ["pulmonologist"]  # Default
    
    return result


async def create_consultation(
    db: AsyncSession,
    user_id: UUID,
    initial_problem: str,
    patient_profile_id: Optional[UUID] = None,
    patient_profile: Optional[Dict[str, Any]] = None
) -> Consultation:
    """
    发起新问诊，使用分诊自动分配医生
    Create a new consultation with triage-assigned doctors
    """
    # 1. 自动执行分诊，传入用户资料
    # 1. Perform automatic triage with patient profile
    triage_result = await perform_triage(db, initial_problem, patient_profile)
    triage_level = triage_result.get("severity", 3)
    assigned_doctor_ids = triage_result.get("assigned_doctors", ["pulmonologist"])

    # 2. 根据分诊结果中的 assigned_doctors 匹配预设医生
    # 2. Match assigned doctor IDs to preset doctors
    doctors = []
    preset_map = {p["id"]: p for p in prompts.DOCTOR_PRESETS}
    
    for doc_id in assigned_doctor_ids:
        if doc_id in preset_map:
            doctor = {**preset_map[doc_id], "status": "active"}
            doctors.append(doctor)
    
    # 如果没有匹配到任何医生，使用呼吸科作为默认
    # If no doctors matched, use pulmonologist as default
    if not doctors:
        default_doc = preset_map.get("pulmonologist", prompts.DOCTOR_PRESETS[1])
        doctors = [{**default_doc, "status": "active"}]

    consultation = Consultation(
        user_id=user_id,
        patient_profile_id=patient_profile_id,
        status=ConsultationStatus.DISCUSSING,
        doctors_config=doctors,
        triage_level=triage_level
    )
    
    db.add(consultation)
    await db.flush()
    
    # 3. 添加分诊结果作为系统第一条消息
    # 3. Add triage result as first system message
    triage_msg = ConsultationMessage(
        consultation_id=consultation.id,
        sender_type="system",
        content=f"[Triage Level: {triage_level}] Recommendation: {triage_result.get('department')}. Summary: {triage_result.get('summary')}"
    )
    db.add(triage_msg)

    # 4. 添加初始主诉消息
    # 4. Add initial complaint message
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
    
    # 如果已经没有活跃医生，直接完成
    # If no active doctors, complete directly
    if not active_doctors:
        consultation.status = ConsultationStatus.COMPLETED
        await db.commit()
        return {"status": "completed", "message": "Consultation completed."}

    # 1. 讨论阶段 (DISCUSSING)
    # 1. Discussion Phase
    if consultation.status == ConsultationStatus.DISCUSSING:
        # 找出下一个该发言的医生 (基于消息历史)
        # Find next doctor to speak based on history
        doctor_responses = [m.doctor_id for m in consultation.messages if m.sender_type == "doctor"]
        
        # 本轮发言过的医生
        # Doctors who spoke this round
        spoken_ids = []
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
            # 本轮讨论结束，直接进入 COMPLETED 状态（禁用投票环节）
            # Discussion finished, go directly to COMPLETED (voting disabled)
            consultation.status = ConsultationStatus.COMPLETED
            await db.commit()
            return {"status": "completed", "message": "All doctors have provided their assessments. Consultation complete."}

    # 2. 投票阶段 (VOTING) - 已禁用
    # 2. Voting Phase - DISABLED
    # if consultation.status == ConsultationStatus.VOTING:
    #     return await _handle_voting_and_elimination(db, consultation, active_doctors)

    # 3. 总结阶段 (SUMMARIZING) - 用户追问时可能触发
    # 3. Summarizing Phase - may be triggered on follow-up
    if consultation.status == ConsultationStatus.SUMMARIZING:
        return await _handle_summarizing(db, consultation, active_doctors)

    return {"status": str(consultation.status)}


async def handle_follow_up(db: AsyncSession, consultation_id: UUID, message: str) -> Dict[str, Any]:
    """
    处理用户追问 - 保存消息并让所有医生再次回复
    Handle user follow-up - save message and have all doctors respond again
    """
    consultation = await get_consultation_full(db, consultation_id)
    if not consultation:
        return {"error": "Consultation not found"}
    
    # 保存用户追问消息
    # Save user's follow-up message
    follow_up_msg = ConsultationMessage(
        consultation_id=consultation.id,
        sender_type="patient",
        content=message
    )
    db.add(follow_up_msg)
    
    # 重置状态为 DISCUSSING，让医生们重新发言
    # Reset status to DISCUSSING so doctors respond again
    consultation.status = ConsultationStatus.DISCUSSING
    
    # 清除医生本轮已发言标记（通过重置，医生们会再说一轮）
    # Clear doctor spoken flags for this round
    doctors = consultation.doctors_config
    for d in doctors:
        d["spoken_this_round"] = False
    consultation.doctors_config = doctors
    
    await db.commit()
    
    # 返回成功信息，前端可以继续调用 run_next_step
    # Return success, frontend can continue calling run_next_step
    return {
        "status": "follow_up_received",
        "message": "Follow-up question received. Doctors will respond.",
        "consultation_status": str(consultation.status)
    }

async def _call_doctor_discussion(db: AsyncSession, consultation: Consultation, doctor: Dict[str, Any]) -> Dict[str, Any]:
    """
    调用单个医生的讨论发言
    Call single doctor's discussion response
    """
    # 准备病历 - 从 patient_profile 获取详细信息
    # Prepare case info - get details from patient_profile
    case_info = {
        "name": "Patient",
        "current_problem": next((m.content for m in consultation.messages if m.sender_type == "patient"), "")
    }
    
    # 如果有患者资料，加载并添加到 case_info
    # If patient profile exists, load and add to case_info
    if consultation.patient_profile_id:
        from app.user.models import PatientProfile
        profile = await db.get(PatientProfile, consultation.patient_profile_id)
        if profile:
            case_info["name"] = profile.name or "Patient"
            case_info["age"] = profile.age
            case_info["gender"] = profile.gender
            case_info["medical_history"] = profile.medical_history
            case_info["allergies"] = profile.allergies
            case_info["current_medications"] = profile.current_medications
    
    # 构建提示词
    # Build prompt
    msg_history = [{"type": m.sender_type, "content": m.content, "doctor_name": m.doctor_name} for m in consultation.messages]
    prompt_data = prompts.build_full_prompt(
        doctor.get("system_prompt", ""), 
        case_info, 
        msg_history, 
        doctor["name"]
    )
    
    # 获取 AI 配置 (per-doctor > global fallback)
    # Get AI config (per-doctor > global fallback)
    api_key, base_url, model = await _get_ai_config(db, doctor)
    
    # 实例化提供商并调用 (统一使用 OpenAI 兼容模式)
    # Instantiate provider and call (use unified OpenAI compatible mode)
    provider = AIProviderFactory.get_provider(
        "openai",  # 统一使用 OpenAI 兼容模式
        api_key or "",
        model,
        base_url
    )
    
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


async def _get_ai_config(db: AsyncSession, doctor: Dict[str, Any]) -> tuple:
    """
    获取 AI 配置：优先使用医生自身配置，否则回退到全局设置
    Get AI config: prefer per-doctor, fallback to global settings
    """
    from app.admin.models import SystemSetting
    
    # 1. 首先获取全局默认配置
    # 1. First get global defaults
    stmt = select(SystemSetting).where(SystemSetting.key.in_([
        "default_api_key", "default_base_url", "default_model"
    ]))
    result = await db.execute(stmt)
    settings_list = result.scalars().all()
    settings_map = {s.key: s.value for s in settings_list}
    
    # 全局默认值
    # Global defaults
    global_api_key = settings_map.get("default_api_key", "")
    global_base_url = settings_map.get("default_base_url", "")
    global_model = settings_map.get("default_model", "gpt-3.5-turbo")
    
    # 2. 使用医生自身配置覆盖（如果有的话）
    # 2. Override with per-doctor config if provided
    api_key = doctor.get("api_key") or doctor.get("apiKey") or global_api_key
    base_url = doctor.get("base_url") or doctor.get("baseUrl") or global_base_url
    
    # 对于 model：只有医生有专门配置且不是旧格式才使用
    # For model: only use doctor's if explicitly set and not old format
    doctor_model = doctor.get("model") or ""
    if doctor_model and not doctor_model.startswith("Pro/"):  # 排除旧 SiliconFlow 格式
        model = doctor_model
    else:
        model = global_model
    
    return api_key, base_url, model



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


async def generate_emergency_guide(db: AsyncSession, consultation_id: UUID) -> Dict[str, Any]:
    """
    生成针对性急救指南
    Generate targeted emergency guidance
    """
    consultation = await get_consultation_full(db, consultation_id)
    if not consultation:
        return {"error": "Consultation not found"}
        
    initial_problem = ""
    triage_summary = "极度紧急情况"
    
    for msg in consultation.messages:
        if msg.sender_type == "patient":
            initial_problem = msg.content
            break
            
    for msg in consultation.messages:
        if msg.sender_type == "system" and "[Triage Level:" in msg.content:
            triage_summary = msg.content
            break

    prompt_data = prompts.build_emergency_prompt(initial_problem, triage_summary)
    
    from app.config import settings
    # 急救指导使用较强的模型
    # Emergency guide uses a stronger model
    provider_name = "siliconflow" if settings.siliconflow_api_key else "openai"
    api_key = settings.siliconflow_api_key if provider_name == "siliconflow" else settings.openai_api_key
    model = "Pro/THUDM/glm-4-9b-chat" if provider_name == "siliconflow" else "gpt-3.5-turbo"
    
    provider = AIProviderFactory.get_provider(provider_name, api_key, model)
    
    content = await provider.chat_completion([
        {"role": "system", "content": prompt_data["system"]},
        {"role": "user", "content": prompt_data["user"]}
    ])
    
    result = parse_vote_json(content)
    if not result:
        # 回退默认紧急指令
        # Fallback default emergency instructions
        result = {
            "title": "Immediate Actions Required",
            "steps": [
                {"index": 1, "action": "Call Local Emergency Services", "detail": "Immediately dial your local emergency number (e.g., 120, 911, 999)."},
                {"index": 2, "action": "Stay Calm and with the Patient", "detail": "Do not leave the patient alone."},
                {"index": 3, "action": "Check Breathing", "detail": "Ensure the patient's airway is clear."}
            ],
            "warnings": ["Do not attempt to give food or water.", "Wait for medical professionals."],
            "prohibited": ["Do not move the patient unless in immediate danger."]
        }
    return result
