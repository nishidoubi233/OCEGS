/**
 * AI 问诊 API 服务
 * AI Consultation API service
 */
import http from './http'

export default {
    /**
     * 发起新的 AI 问诊
     * Start a new AI consultation
     * @param {Object} data - initialProblem, patientProfileId, doctors
     */
    startConsultation(data) {
        return http.post('/consultation/consultations/', data)
    },

    /**
     * 获取问诊详情
     * Get consultation details
     * @param {string} id - Consultation ID
     */
    getConsultation(id) {
        return http.get(`/consultation/consultations/${id}`)
    },

    /**
     * 向前推进一个会诊步骤 (发言/投票/总结)
     * Advance consultation by one step (speech/vote/summary)
     * @param {string} id - Consultation ID
     */
    advanceStep(id) {
        return http.post(`/consultation/consultations/${id}/step`)
    },

    /**
     * 获取当前用户的所有问诊历史
     * Get all my consultation history
     */
    getMyHistory() {
        return http.get('/consultation/consultations/my/all')
    },

    /**
     * 进行预检分诊评估
     * Perform triage evaluation
     * @param {Object} data - initial_problem
     */
    performTriage(data) {
        return http.post('/consultation/consultations/triage', data)
    },

    /**
     * 获取指定会诊的急救指导
     * Get emergency guide for a consultation
     * @param {string} id - Consultation ID
     */
    getEmergencyGuide(id) {
        return http.get(`/consultation/consultations/${id}/emergency-guide`)
    }
}
