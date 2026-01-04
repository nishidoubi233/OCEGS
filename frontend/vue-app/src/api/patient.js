/**
 * 患者档案API服务
 * Patient profile API service
 */
import http from '@/api/http'

// ============================================================
// 患者档案
// Patient Profile
// ============================================================

/**
 * 获取当前用户的患者档案
 * Get current user's patient profile
 * 
 * @returns {Promise} 患者档案（含病史和紧急联系人）
 */
export async function getMyProfile() {
    const response = await http.get('/patients/profile')
    return response.data
}

/**
 * 创建患者档案
 * Create patient profile
 * 
 * @param {Object} profileData - 档案数据
 * @returns {Promise} 新创建的档案
 */
export async function createProfile(profileData) {
    const response = await http.post('/patients/profile', profileData)
    return response.data
}

/**
 * 更新患者档案
 * Update patient profile
 * 
 * @param {Object} profileData - 更新数据
 * @returns {Promise} 更新后的档案
 */
export async function updateProfile(profileData) {
    const response = await http.put('/patients/profile', profileData)
    return response.data
}

// ============================================================
// 病史记录
// Medical History
// ============================================================

/**
 * 获取所有病史记录
 * Get all medical history records
 * 
 * @returns {Promise} 病史列表
 */
export async function getMedicalHistory() {
    const response = await http.get('/patients/medical-history')
    return response.data
}

/**
 * 添加病史记录
 * Add medical history record
 * 
 * @param {Object} historyData - 病史数据
 * @returns {Promise} 新创建的病史
 */
export async function addMedicalHistory(historyData) {
    const response = await http.post('/patients/medical-history', historyData)
    return response.data
}

/**
 * 更新病史记录
 * Update medical history record
 * 
 * @param {string} historyId - 病史ID
 * @param {Object} historyData - 更新数据
 * @returns {Promise} 更新后的病史
 */
export async function updateMedicalHistory(historyId, historyData) {
    const response = await http.put(`/patients/medical-history/${historyId}`, historyData)
    return response.data
}

/**
 * 删除病史记录
 * Delete medical history record
 * 
 * @param {string} historyId - 病史ID
 * @returns {Promise}
 */
export async function deleteMedicalHistory(historyId) {
    await http.delete(`/patients/medical-history/${historyId}`)
}

// ============================================================
// 紧急联系人
// Emergency Contacts
// ============================================================

/**
 * 获取所有紧急联系人
 * Get all emergency contacts
 * 
 * @returns {Promise} 紧急联系人列表
 */
export async function getEmergencyContacts() {
    const response = await http.get('/patients/emergency-contacts')
    return response.data
}

/**
 * 添加紧急联系人
 * Add emergency contact
 * 
 * @param {Object} contactData - 联系人数据
 * @returns {Promise} 新创建的联系人
 */
export async function addEmergencyContact(contactData) {
    const response = await http.post('/patients/emergency-contacts', contactData)
    return response.data
}

/**
 * 更新紧急联系人
 * Update emergency contact
 * 
 * @param {string} contactId - 联系人ID
 * @param {Object} contactData - 更新数据
 * @returns {Promise} 更新后的联系人
 */
export async function updateEmergencyContact(contactId, contactData) {
    const response = await http.put(`/patients/emergency-contacts/${contactId}`, contactData)
    return response.data
}

/**
 * 删除紧急联系人
 * Delete emergency contact
 * 
 * @param {string} contactId - 联系人ID
 * @returns {Promise}
 */
export async function deleteEmergencyContact(contactId) {
    await http.delete(`/patients/emergency-contacts/${contactId}`)
}
