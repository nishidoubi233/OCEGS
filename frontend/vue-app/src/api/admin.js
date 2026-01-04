/**
 * 管理面板 API 服务
 * Admin Panel API Service
 */
import http from './http'

export default {
    /**
     * 管理员登录
     * Admin login
     * @param {string} password - Admin password
     */
    login(password) {
        return http.post('/admin/login', { password })
    },

    /**
     * 获取系统状态
     * Get system status
     */
    getStatus() {
        return http.get('/admin/status')
    },

    /**
     * 获取所有系统设置
     * Get all system settings
     */
    getSettings() {
        return http.get('/admin/settings')
    },

    /**
     * 更新系统设置
     * Update system setting
     * @param {string} key - Setting key
     * @param {string} value - New value
     */
    updateSetting(key, value) {
        return http.put(`/admin/settings/${key}`, { value })
    },

    /**
     * 初始化系统设置
     * Initialize system settings
     */
    initSettings() {
        return http.post('/admin/init-settings')
    },

    /**
     * 获取医生团队配置
     * Get doctors team configuration
     */
    getDoctorsConfig() {
        return http.get('/admin/doctors-config')
    },

    /**
     * 更新医生团队配置
     * Update doctors team configuration
     * @param {Array} doctors - Doctors configuration array
     */
    updateDoctorsConfig(doctors) {
        return http.put('/admin/doctors-config', { doctors })
    },

    /**
     * 获取可用模型列表
     * Fetch available models from API
     * @param {string} apiKey - API key
     * @param {string} baseUrl - Base URL
     */
    fetchModels(apiKey, baseUrl) {
        return http.post('/admin/models', { api_key: apiKey, base_url: baseUrl })
    }
}
