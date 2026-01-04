/**
 * OCEGS HTTP客户端配置
 * OCEGS HTTP Client Configuration - Axios instance with interceptors
 */
import axios from 'axios'

// 创建axios实例
// Create axios instance
const http = axios.create({
    baseURL: '/api',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
})

// 请求拦截器 - 添加认证Token
// Request interceptor - Add auth token
http.interceptors.request.use(
    (config) => {
        // 从localStorage获取Token并添加到请求头
        // Get token from localStorage and add to headers
        const token = localStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// 响应拦截器 - 处理错误
// Response interceptor - Handle errors
http.interceptors.response.use(
    (response) => {
        return response
    },
    async (error) => {
        const originalRequest = error.config

        // 处理401未授权错误 - 尝试刷新Token
        // Handle 401 unauthorized - Try to refresh token
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true

            const refreshToken = localStorage.getItem('refresh_token')
            if (refreshToken) {
                try {
                    // 刷新Token
                    // Refresh token
                    const response = await axios.post('/api/auth/refresh', {
                        refresh_token: refreshToken
                    })

                    const { access_token, refresh_token: newRefreshToken } = response.data
                    localStorage.setItem('access_token', access_token)
                    localStorage.setItem('refresh_token', newRefreshToken)

                    // 重试原始请求
                    // Retry original request
                    originalRequest.headers.Authorization = `Bearer ${access_token}`
                    return http(originalRequest)
                } catch (refreshError) {
                    // 刷新失败，清除Token并重定向到登录页
                    // Refresh failed, clear tokens and redirect to login
                    localStorage.removeItem('access_token')
                    localStorage.removeItem('refresh_token')
                    window.location.href = '/login'
                    return Promise.reject(refreshError)
                }
            }
        }

        // 处理其他错误
        // Handle other errors
        if (error.response) {
            switch (error.response.status) {
                case 403:
                    console.error('Access forbidden')
                    break
                case 500:
                    console.error('Server error')
                    break
            }
        }
        return Promise.reject(error)
    }
)

export default http

