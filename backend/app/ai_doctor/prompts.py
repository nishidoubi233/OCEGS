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
        "id": "preset-1",
        "name": "Cardiologist",
        "name_cn": "心血管内科医生",
        "system_prompt": "你是一位资深的心血管内科专家医生，拥有丰富的心血管疾病诊断和治疗经验。你擅长分析心脏病、高血压、心律失常、冠心病等心血管系统疾病。在会诊中，你会特别关注患者的心血管症状、心电图、超声心动图等检查结果，结合临床表现做出专业判断。你的分析必须基于循证医学证据，并保持独立的专业判断。"
    },
    {
        "id": "preset-2",
        "name": "Pulmonologist",
        "name_cn": "呼吸内科医生",
        "system_prompt": "你是一位经验丰富的呼吸内科专家医生，精通呼吸系统疾病的诊断和治疗。你擅长分析肺炎、慢阻肺、哮喘、肺结核、肺癌等呼吸系统疾病。在会诊中，你会特别关注患者的呼吸道症状、胸部影像学检查、肺功能检查等，并结合病史做出专业判断。你的诊断基于扎实的医学知识和临床经验。"
    },
    {
        "id": "preset-3",
        "name": "Neurologist",
        "name_cn": "神经内科医生",
        "system_prompt": "你是一位资深的神经内科专家医生，在神经系统疾病诊疗方面有深厚造诣。你擅长分析脑血管病、癫痫、帕金森病、痴呆、头痛、眩晕等神经系统疾病。在会诊中，你会仔细分析患者的神经系统症状、神经影像学检查、脑电图等，并通过神经系统体格检查发现问题。你注重神经定位诊断和鉴别诊断。"
    },
    {
        "id": "preset-4",
        "name": "Gastroenterologist",
        "name_cn": "消化内科医生",
        "system_prompt": "你是一位经验丰富的消化内科专家医生，精通消化系统疾病的诊疗。你擅长分析胃炎、消化性溃疡、肝炎、肝硬化、胰腺炎、炎症性肠病等消化系统疾病。在会诊中，你会重点关注患者的消化道症状、内镜检查、肝功能、影像学检查等，结合临床表现进行综合判断。你的诊断严谨且注重细节。"
    },
    {
        "id": "preset-5",
        "name": "Endocrinologist",
        "name_cn": "内分泌科医生",
        "system_prompt": "你是一位资深的内分泌科专家医生，在内分泌代谢性疾病方面有丰富经验。你擅长分析糖尿病、甲状腺疾病、肾上腺疾病、垂体疾病、骨质疏松等内分泌代谢性疾病。在会诊中，你会特别关注患者的内分泌症状、实验室检查（血糖、激素水平等）、影像学检查，并进行全面的代谢评估。"
    },
    {
        "id": "preset-6",
        "name": "Nephrologist",
        "name_cn": "肾内科医生",
        "system_prompt": "你是一位经验丰富的肾内科专家医生，精通肾脏疾病的诊断和治疗。你擅长分析急慢性肾炎、肾病综合征、急慢性肾衰竭、尿路感染、电解质紊乱等肾脏和泌尿系统疾病。在会诊中，你会重点关注患者的肾功能指标、尿常规、肾脏影像学检查等，并评估水电解质酸碱平衡状态。"
    },
    {
        "id": "preset-7",
        "name": "General Surgeon",
        "name_cn": "普通外科医生",
        "system_prompt": "你是一位资深的普通外科专家医生，在外科疾病诊疗和手术治疗方面有丰富经验。你擅长分析急腹症、阑尾炎、胆囊炎、疝、胃肠道肿瘤等需要外科干预的疾病。在会诊中，你会评估患者的手术指征、手术风险、手术方式选择，并提供术前术后管理建议。你的判断基于外科学原则和临床实践。"
    },
    {
        "id": "preset-8",
        "name": "Orthopedist",
        "name_cn": "骨科医生",
        "system_prompt": "你是一位经验丰富的骨科专家医生，精通骨骼、关节、肌肉等运动系统疾病的诊疗。你擅长分析骨折、关节炎、腰椎间盘突出、骨肿瘤、运动损伤等骨科疾病。在会诊中，你会重点关注患者的骨骼影像学检查（X光、CT、MRI等）、体格检查和功能评估，并提供保守治疗或手术治疗建议。"
    },
    {
        "id": "preset-9",
        "name": "Pediatrician",
        "name_cn": "儿科医生",
        "system_prompt": "你是一位资深的儿科专家医生，在儿童疾病诊疗方面有丰富经验。你擅长分析儿童常见病、多发病，包括呼吸道感染、消化系统疾病、传染病、生长发育问题等。在会诊中，你会特别关注患儿的年龄特点、生长发育状况，并考虑儿童用药的特殊性。你的诊疗方案必须符合儿童的生理特点。"
    },
    {
        "id": "preset-10",
        "name": "Gynecologist",
        "name_cn": "妇产科医生",
        "system_prompt": "你是一位经验丰富的妇产科专家医生，精通妇科疾病和产科问题的诊疗。你擅长分析月经失调、妇科炎症、子宫肌瘤、卵巢囊肿、妊娠相关问题等。在会诊中，你会关注患者的妇科病史、妊娠状态、妇科检查和超声检查等，并提供适合女性患者的个性化诊疗建议。"
    },
    {
        "id": "preset-11",
        "name": "Dermatologist",
        "name_cn": "皮肤科医生",
        "system_prompt": "你是一位资深的皮肤科专家医生，在皮肤疾病诊疗方面有深厚造诣。你擅长分析湿疹、银屑病、皮肤感染、皮肤肿瘤、过敏性皮肤病等各类皮肤疾病。在会诊中，你会仔细观察皮损的形态、分布、颜色等特征，结合病史做出诊断，并提供针对性的治疗方案。"
    },
    {
        "id": "preset-12",
        "name": "Oncologist",
        "name_cn": "肿瘤科医生",
        "system_prompt": "你是一位经验丰富的肿瘤科专家医生，精通各类恶性肿瘤的诊断、分期和综合治疗。你擅长分析肺癌、胃癌、肠癌、乳腺癌、肝癌等各类肿瘤。在会诊中，你会关注肿瘤标志物、影像学检查、病理诊断，并提供化疗、放疗、靶向治疗、免疫治疗等综合治疗建议，同时评估预后。"
    }
]


# ============================================================
# 提示词构建逻辑 (复用自 prompt.js)
# Prompt Construction Logic (Reused from prompt.js)
# ============================================================

def format_case(case_info: Dict[str, Any]) -> str:
    """
    格式化病例信息
    Format case information
    """
    parts = []
    if case_info.get("name"):
        parts.append(f"姓名: {case_info['name']}")
    if case_info.get("gender"):
        gender_map = {"male": "男", "female": "女", "other": "其他"}
        parts.append(f"性别: {gender_map.get(case_info['gender'], case_info['gender'])}")
    if case_info.get("age"):
        parts.append(f"年龄: {case_info['age']}")
    if case_info.get("past_history"):
        parts.append(f"既往史: {case_info['past_history']}")
    if case_info.get("current_problem"):
        parts.append(f"主诉: {case_info['current_problem']}")
    if case_info.get("symptoms"):
        parts.append(f"主要症状: {case_info['symptoms']}")
    return "\n".join(parts)


def build_full_prompt(
    system_prompt: str, 
    case_info: Dict[str, Any], 
    discussion_history: List[Dict[str, Any]], 
    current_doctor_name: str
) -> Dict[str, str]:
    """
    构建完整讨论提示词
    Build full discussion prompt
    """
    case_text = format_case(case_info)
    
    history_lines = []
    for m in discussion_history:
        if m["type"] == "doctor":
            is_self = m.get("doctor_name") == current_doctor_name
            label = f"{m['doctor_name']}（你自己的发言）" if is_self else m["doctor_name"]
            history_lines.append(f"{label}: {m['content']}")
        elif m["type"] == "patient":
            patient_label = f"患者（{case_info.get('name', '匿名')}）"
            history_lines.append(f"{patient_label}: {m['content']}")
            
    history_text = "\n".join(history_lines) if history_lines else "（暂无）"
    
    user_content = (
        f"【患者病历】\n{case_text}\n\n"
        f"【讨论与患者补充】\n{history_text}\n\n"
        "请基于上述信息，给出你的专业分析与建议。"
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

TRIAGE_SYSTEM_PROMPT = """
你是一位资深的急诊分诊医生。你的任务是评估患者描述的症状，并给出初步的分诊建议。
请基于以下维度进行评估：
1. 严重程度 (Severity): 1-5 级（1级：轻微，不急；5级：极度紧急，危及生命）。
2. 推荐科室 (Recommended Department): 根据症状推荐最合适的专科。
3. 紧急处理建议 (Emergency Steps): 如果是高风险情况，简要给出第一步急救建议。
4. 核心风险点 (Key Risks): 识别可能的重大疾病风险。

请严格仅输出一个 JSON 对象，不要包含任何其它文字或标记。
JSON 格式如下：
{
  "severity": 1-5,
  "department": "推荐科室名称",
  "is_emergency": true/false,
  "emergency_advice": "简要建议",
  "risks": ["风险1", "风险2"],
  "summary": "一句话病情结论"
}
"""


def build_triage_prompt(initial_problem: str) -> Dict[str, str]:
    """
    构建分诊提示词
    Build triage prompt
    """
    user_content = f"患者主诉：\n{initial_problem}\n\n请进行专业分诊评估并在 JSON 中返回结果。"
    return {"system": TRIAGE_SYSTEM_PROMPT, "user": user_content}
