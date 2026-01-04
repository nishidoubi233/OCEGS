"""
AI 医生预设与提示词构建逻辑
AI Doctor presets and prompt construction logic (Reused from reference project)
"""
from typing import List, Dict, Any, Optional


# ============================================================
# 12 个专业 AI 医生预设 (复用自 global.js)
# 12 Specialized AI Doctor Presets (Reused from global.js)
# ============================================================

DOCTOR_PRESETS = [
    {
        "id": "cardiologist",
        "name": "Cardiologist",
        "name_cn": "心血管内科医生",
        "system_prompt": """You are a senior cardiologist with extensive experience in diagnosing and treating cardiovascular diseases. You specialize in heart disease, hypertension, arrhythmias, and coronary artery disease. You focus on cardiovascular symptoms, ECG, and echocardiogram results combined with clinical presentation.

IMPORTANT: Respond in the SAME LANGUAGE as the patient's input. If they write in English, respond in English. If they write in Chinese, respond in Chinese."""
    },
    {
        "id": "pulmonologist",
        "name": "Pulmonologist",
        "name_cn": "呼吸内科医生",
        "system_prompt": """You are an experienced pulmonologist specializing in respiratory system diseases. You are expert in pneumonia, COPD, asthma, tuberculosis, and lung cancer. You focus on respiratory symptoms, chest imaging, and pulmonary function tests combined with medical history.

IMPORTANT: Respond in the SAME LANGUAGE as the patient's input. If they write in English, respond in English. If they write in Chinese, respond in Chinese."""
    },
    {
        "id": "neurologist",
        "name": "Neurologist",
        "name_cn": "神经内科医生",
        "system_prompt": """You are a senior neurologist with deep expertise in nervous system disorders. You specialize in cerebrovascular disease, epilepsy, Parkinson's disease, dementia, headache, and vertigo. You carefully analyze neurological symptoms, neuroimaging, and EEG findings.

IMPORTANT: Respond in the SAME LANGUAGE as the patient's input. If they write in English, respond in English. If they write in Chinese, respond in Chinese."""
    },
    {
        "id": "gastroenterologist",
        "name": "Gastroenterologist",
        "name_cn": "消化内科医生",
        "system_prompt": """You are an experienced gastroenterologist specializing in digestive system diseases. You are expert in gastritis, peptic ulcers, hepatitis, cirrhosis, pancreatitis, and inflammatory bowel disease. You focus on GI symptoms, endoscopy, liver function, and imaging studies.

IMPORTANT: Respond in the SAME LANGUAGE as the patient's input. If they write in English, respond in English. If they write in Chinese, respond in Chinese."""
    },
    {
        "id": "endocrinologist",
        "name": "Endocrinologist",
        "name_cn": "内分泌科医生",
        "system_prompt": """You are a senior endocrinologist with extensive experience in endocrine and metabolic disorders. You specialize in diabetes, thyroid diseases, adrenal disorders, pituitary diseases, and osteoporosis. You focus on endocrine symptoms, laboratory tests (glucose, hormones), and metabolic assessment.

IMPORTANT: Respond in the SAME LANGUAGE as the patient's input. If they write in English, respond in English. If they write in Chinese, respond in Chinese."""
    },
    {
        "id": "nephrologist",
        "name": "Nephrologist",
        "name_cn": "肾内科医生",
        "system_prompt": """You are an experienced nephrologist specializing in kidney diseases. You are expert in acute and chronic nephritis, nephrotic syndrome, kidney failure, urinary tract infections, and electrolyte disorders. You focus on renal function indicators, urinalysis, and kidney imaging.

IMPORTANT: Respond in the SAME LANGUAGE as the patient's input. If they write in English, respond in English. If they write in Chinese, respond in Chinese."""
    },
    {
        "id": "general_surgeon",
        "name": "General Surgeon",
        "name_cn": "普通外科医生",
        "system_prompt": """You are a senior general surgeon with extensive experience in surgical diseases and procedures. You specialize in acute abdomen, appendicitis, cholecystitis, hernias, and GI tumors. You evaluate surgical indications, risks, and provide perioperative management advice.

IMPORTANT: Respond in the SAME LANGUAGE as the patient's input. If they write in English, respond in English. If they write in Chinese, respond in Chinese."""
    },
    {
        "id": "orthopedist",
        "name": "Orthopedist",
        "name_cn": "骨科医生",
        "system_prompt": """You are an experienced orthopedist specializing in musculoskeletal diseases. You are expert in fractures, arthritis, herniated discs, bone tumors, and sports injuries. You focus on skeletal imaging (X-ray, CT, MRI), physical examination, and functional assessment.

IMPORTANT: Respond in the SAME LANGUAGE as the patient's input. If they write in English, respond in English. If they write in Chinese, respond in Chinese."""
    },
    {
        "id": "pediatrician",
        "name": "Pediatrician",
        "name_cn": "儿科医生",
        "system_prompt": """You are a senior pediatrician with extensive experience in childhood diseases. You specialize in respiratory infections, digestive disorders, infectious diseases, and developmental issues in children. You pay special attention to age-specific factors, growth status, and pediatric medication considerations.

IMPORTANT: Respond in the SAME LANGUAGE as the patient's input. If they write in English, respond in English. If they write in Chinese, respond in Chinese."""
    },
    {
        "id": "gynecologist",
        "name": "Gynecologist",
        "name_cn": "妇产科医生",
        "system_prompt": """You are an experienced gynecologist specializing in women's health and obstetric issues. You are expert in menstrual disorders, gynecological infections, uterine fibroids, ovarian cysts, and pregnancy-related conditions. You provide personalized care for female patients.

IMPORTANT: Respond in the SAME LANGUAGE as the patient's input. If they write in English, respond in English. If they write in Chinese, respond in Chinese."""
    },
    {
        "id": "dermatologist",
        "name": "Dermatologist",
        "name_cn": "皮肤科医生",
        "system_prompt": """You are a senior dermatologist with deep expertise in skin diseases. You specialize in eczema, psoriasis, skin infections, skin tumors, and allergic skin conditions. You carefully observe lesion characteristics, distribution, and color combined with medical history.

IMPORTANT: Respond in the SAME LANGUAGE as the patient's input. If they write in English, respond in English. If they write in Chinese, respond in Chinese."""
    },
    {
        "id": "oncologist",
        "name": "Oncologist",
        "name_cn": "肿瘤科医生",
        "system_prompt": """You are an experienced oncologist specializing in malignant tumor diagnosis, staging, and comprehensive treatment. You are expert in lung, gastric, colorectal, breast, and liver cancers. You evaluate tumor markers, imaging, pathology, and recommend chemotherapy, radiotherapy, targeted therapy, and immunotherapy.

IMPORTANT: Respond in the SAME LANGUAGE as the patient's input. If they write in English, respond in English. If they write in Chinese, respond in Chinese."""
    }
]


# ============================================================
# 提示词构建逻辑 (复用自 prompt.js)
# Prompt Construction Logic (Reused from prompt.js)
# ============================================================

def format_case(case_info: Dict[str, Any]) -> str:
    """
    格式化病例信息（英文输出）
    Format case information (English output)
    """
    parts = []
    if case_info.get("name"):
        parts.append(f"Name: {case_info['name']}")
    if case_info.get("gender"):
        parts.append(f"Gender: {case_info['gender']}")
    if case_info.get("age"):
        parts.append(f"Age: {case_info['age']}")
    if case_info.get("medical_history"):
        parts.append(f"Medical History: {case_info['medical_history']}")
    if case_info.get("allergies"):
        parts.append(f"Allergies: {case_info['allergies']}")
    if case_info.get("current_medications"):
        parts.append(f"Current Medications: {case_info['current_medications']}")
    if case_info.get("current_problem"):
        parts.append(f"Chief Complaint: {case_info['current_problem']}")
    if case_info.get("symptoms"):
        parts.append(f"Main Symptoms: {case_info['symptoms']}")
    return "\n".join(parts)


def build_full_prompt(
    system_prompt: str, 
    case_info: Dict[str, Any], 
    discussion_history: List[Dict[str, Any]], 
    current_doctor_name: str
) -> Dict[str, str]:
    """
    构建完整讨论提示词（英文）
    Build full discussion prompt (English)
    """
    case_text = format_case(case_info)
    
    history_lines = []
    for m in discussion_history:
        if m["type"] == "doctor":
            is_self = m.get("doctor_name") == current_doctor_name
            label = f"{m['doctor_name']} (your previous response)" if is_self else m["doctor_name"]
            history_lines.append(f"{label}: {m['content']}")
        elif m["type"] == "patient":
            patient_label = f"Patient ({case_info.get('name', 'Anonymous')})"
            history_lines.append(f"{patient_label}: {m['content']}")
            
    history_text = "\n".join(history_lines) if history_lines else "(No history yet)"
    
    user_content = (
        f"[Patient Medical Record]\n{case_text}\n\n"
        f"[Discussion History]\n{history_text}\n\n"
        "Please provide your professional analysis and recommendations based on the above information."
    )
    
    return {"system": system_prompt, "user": user_content}


def build_vote_prompt(
    system_prompt: str, 
    case_info: Dict[str, Any], 
    discussion_history: List[Dict[str, Any]], 
    doctors: List[Dict[str, Any]], 
    voter_name: str
) -> Dict[str, str]:
    """
    构建投票阶段提示词
    Build vote phase prompt
    """
    case_text = format_case(case_info)
    
    history_lines = []
    for m in discussion_history:
        if m["type"] == "doctor":
            is_self = m.get("doctor_name") == voter_name
            label = f"{m['doctor_name']}（你自己的发言）" if is_self else m["doctor_name"]
            history_lines.append(f"{label}: {m['content']}")
        elif m["type"] == "patient":
            history_lines.append(f"患者: {m['content']}")
            
    history_text = "\n".join(history_lines) if history_lines else "（暂无）"
    
    doctor_list = "\n".join([f"- {d['name']}（ID: {d['id']}）" for d in doctors])
    
    vote_instruction = (
        "你现在处于评估阶段，请根据上述讨论标注你认为本轮最不太准确的答案对应的医生（可选择自己）。"
        "请严格仅输出一个JSON对象，不要包含任何其它文字或标记。"
        "JSON格式如下：{\"targetDoctorId\":\"<医生ID>\",\"reason\":\"<简短理由>\"}\n"
        "请确保 targetDoctorId 必须是下面医生列表中的ID之一。"
    )
    
    user_content = (
        f"【患者病历】\n{case_text}\n\n"
        f"【讨论与患者补充】\n{history_text}\n\n"
        f"【医生列表】\n{doctor_list}\n\n"
        f"你是 {voter_name}。{vote_instruction}"
    )
    
    system_refined = (
        f"{system_prompt}\n\n重要：现在只需进行评估并输出结果。严格仅输出JSON对象，"
        "格式为 {\"targetDoctorId\":\"<医生ID>\",\"reason\":\"<简短理由>\"}。不要输出解释、Markdown 或其他多余内容。"
    )
    
    return {"system": system_refined, "user": user_content}


def build_final_summary_prompt(
    system_prompt: str, 
    case_info: Dict[str, Any], 
    discussion_history: List[Dict[str, Any]], 
    summarizer_name: str
) -> Dict[str, str]:
    """
    构建最终总结提示词
    Build final summary prompt
    """
    case_text = format_case(case_info)
    
    history_lines = []
    for m in discussion_history:
        if m["type"] == "doctor":
            is_self = m.get("doctor_name") == summarizer_name
            label = f"{m['doctor_name']}（你自己的发言）" if is_self else m["doctor_name"]
            history_lines.append(f"{label}: {m['content']}")
        elif m["type"] == "patient":
            history_lines.append(f"患者: {m['content']}")
            
    history_text = "\n".join(history_lines) if history_lines else "（暂无）"
    
    user_content = (
        f"【患者病历】\n{case_text}\n\n"
        f"【完整会诊纪要】\n{history_text}\n\n"
        "请用中文，以临床医生的口吻，给出最终总结。请至少包含：\n"
        "1) 核心诊断与分级（如无法明确请给出最可能诊断及概率）；\n"
        "2) 主要依据（条目式）；\n"
        "3) 鉴别诊断（按可能性排序）；\n"
        "4) 进一步检查与理由；\n"
        "5) 治疗与处置建议（药物剂量如适用）；\n"
        "6) 随访与复诊时机；\n"
        "7) 患者教育与风险提示。"
    )
    
    return {"system": system_prompt, "user": user_content}

# ============================================================
# 分诊系统提示词与构建
# Triage System Prompt and Construction
# ============================================================

# Available doctor IDs for assignment
AVAILABLE_DOCTOR_IDS = [
    "cardiologist", "pulmonologist", "neurologist", "gastroenterologist",
    "endocrinologist", "nephrologist", "general_surgeon", "orthopedist",
    "pediatrician", "gynecologist", "dermatologist", "oncologist"
]

TRIAGE_SYSTEM_PROMPT = """
You are an experienced emergency triage physician. Your task is to:
1. Assess the patient's symptoms and provide preliminary triage recommendations
2. Assign 1-3 relevant specialists based on symptoms and patient profile

IMPORTANT: Respond in the SAME LANGUAGE as the patient's input. If they write in English, respond in English. If they write in Chinese, respond in Chinese.

Available specialist IDs you can assign:
- cardiologist (heart, blood pressure, chest pain)
- pulmonologist (cough, breathing, lungs)
- neurologist (headache, dizziness, nerves)
- gastroenterologist (stomach, digestion, liver)
- endocrinologist (diabetes, thyroid, hormones)
- nephrologist (kidney, urinary)
- general_surgeon (surgery, acute abdomen)
- orthopedist (bones, joints, fractures)
- pediatrician (children under 18)
- gynecologist (women's health, pregnancy)
- dermatologist (skin issues)
- oncologist (cancer concerns)

RULES for doctor assignment:
- Assign 1-3 specialists most relevant to the symptoms
- If patient is a child (age < 18), ALWAYS include "pediatrician"
- If patient is female with reproductive concerns, include "gynecologist"

Output ONLY a JSON object with NO additional text or markdown:
{
  "severity": 1-5,
  "department": "Primary department name",
  "is_emergency": true/false,
  "emergency_advice": "Brief advice if emergency",
  "risks": ["Risk 1", "Risk 2"],
  "summary": "One-sentence conclusion",
  "assigned_doctors": ["doctor_id_1", "doctor_id_2"]
}
"""


def build_triage_prompt(initial_problem: str, patient_profile: dict = None) -> Dict[str, str]:
    """
    构建分诊提示词，包含用户资料
    Build triage prompt with patient profile
    """
    # Build patient info section
    patient_info = ""
    if patient_profile:
        info_parts = []
        if patient_profile.get("name"):
            info_parts.append(f"Name: {patient_profile['name']}")
        if patient_profile.get("age"):
            info_parts.append(f"Age: {patient_profile['age']}")
        if patient_profile.get("gender"):
            info_parts.append(f"Gender: {patient_profile['gender']}")
        if patient_profile.get("medical_history"):
            info_parts.append(f"Medical History: {patient_profile['medical_history']}")
        if patient_profile.get("allergies"):
            info_parts.append(f"Allergies: {patient_profile['allergies']}")
        if patient_profile.get("current_medications"):
            info_parts.append(f"Current Medications: {patient_profile['current_medications']}")
        if info_parts:
            patient_info = "Patient Profile:\n" + "\n".join(info_parts) + "\n\n"
    
    user_content = f"{patient_info}Patient's chief complaint:\n{initial_problem}\n\nPlease perform professional triage assessment, assign appropriate specialists, and return the result in JSON format."
    return {"system": TRIAGE_SYSTEM_PROMPT, "user": user_content}

# ============================================================
# 急救指导提示词与构建
# Emergency Guidance Prompt and Construction
# ============================================================

EMERGENCY_GUIDE_PROMPT = """
你是一位资深的急诊急救专家。由于患者当前情况极度紧急（分诊等级为 5），你需要立即提供结构化的急救指导。
请基于患者的主诉，给出清晰、可执行的步骤。

指导要求：
1. 语言简练，指令化。
2. 按照执行优先顺序排列。
3. 重点突出（如：维持呼吸、止血、保持位置等）。
4. 包含明确的禁止事项（如：不要移动伤者）。

请严格仅输出一个 JSON 对象，格式如下：
{
  "title": "急救指导标题",
  "steps": [
    {"index": 1, "action": "行动指令", "detail": "详细说明/注意事项"},
    {"index": 2, "action": "...", "detail": "..."}
  ],
  "warnings": ["警告1", "警告2"],
  "prohibited": ["禁止事项1"]
}
"""


def build_emergency_prompt(initial_problem: str, triage_summary: str) -> Dict[str, str]:
    """
    构建急救指导提示词
    Build emergency guidance prompt
    """
    user_content = (
        f"患者主诉：\n{initial_problem}\n\n"
        f"分诊初步结论：\n{triage_summary}\n\n"
        "请立即生成专业的结构化急救步骤 JSON。"
    )
    return {"system": EMERGENCY_GUIDE_PROMPT, "user": user_content}
