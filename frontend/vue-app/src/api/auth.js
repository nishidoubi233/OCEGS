/**
 * 认证API服务
 * Authentication API service
 */
import http from '@/api/http'

/**
 * 用户注册
 * User registration
 * 
 * @param {string} email - 用户邮箱 / User email
 * @param {string} password - 用户密码 / User password
 * @param {string} role - 用户角色 / User role (optional)
 * @returns {Promise} 用户信息 / User info
 */
export async function register(email, password, role = 'patient') {
    const response = await http.post('/auth/register', {
        email,
        password,
        role
    })
    return response.data
}

/**
 * 用户登录
 * User login
 * 
 * @param {string} email - 用户邮箱 / User email
 * @param {string} password - 用户密码 / User password
 * @returns {Promise} Token对象 / Token object
 */
export async function login(email, password) {
    const response = await http.post('/auth/login', {
        email,
        password
    })
    return response.data
}

/**
 * 刷新令牌
 * Refresh tokens
 * 
 * @param {string} refreshToken - 刷新令牌 / Refresh token
 * @returns {Promise} 新Token对象 / New token object
 */
export async function refreshToken(refreshToken) {
    const response = await http.post('/auth/refresh', {
        refresh_token: refreshToken
    })
    return response.data
}

/**
 * 获取当前用户信息
 * Get current user info
 * 
 * @returns {Promise} 用户信息 / User info
 */
export async function getCurrentUser() {
    const response = await http.get('/auth/me')
    return response.data
}

/**
 * 用户登出
 * User logout
 * 
 * @returns {Promise} 消息响应 / Message response
 */
export async function logout() {
    const response = await http.post('/auth/logout')
    return response.data
}
