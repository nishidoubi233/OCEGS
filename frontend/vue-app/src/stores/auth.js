/**
 * 认证状态管理 (Pinia Store)
 * Authentication state management (Pinia Store)
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authApi from '@/api/auth'
import http from '@/api/http'

export const useAuthStore = defineStore('auth', () => {
    // ============================================================
    // 状态
    // State
    // ============================================================

    // 当前用户信息
    // Current user info
    const user = ref(null)

    // 访问令牌
    // Access token
    const accessToken = ref(localStorage.getItem('access_token') || null)

    // 刷新令牌
    // Refresh token
    const refreshToken = ref(localStorage.getItem('refresh_token') || null)

    // 加载状态
    // Loading state
    const loading = ref(false)

    // 错误信息
    // Error message
    const error = ref(null)

    // ============================================================
    // 计算属性
    // Computed properties
    // ============================================================

    // 是否已认证
    // Is authenticated
    const isAuthenticated = computed(() => !!accessToken.value && !!user.value)

    // 用户角色
    // User role
    const userRole = computed(() => user.value?.role || null)

    // 是否为管理员
    // Is admin
    const isAdmin = computed(() => user.value?.role === 'admin')

    // ============================================================
    // 动作
    // Actions
    // ============================================================

    /**
     * 设置令牌到本地存储
     * Save tokens to localStorage
     */
    function setTokens(access, refresh) {
        accessToken.value = access
        refreshToken.value = refresh
        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)

        // 设置Axios默认Header
        // Set Axios default header
        http.defaults.headers.common['Authorization'] = `Bearer ${access}`
    }

    /**
     * 清除令牌
     * Clear tokens
     */
    function clearTokens() {
        accessToken.value = null
        refreshToken.value = null
        user.value = null
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        delete http.defaults.headers.common['Authorization']
    }

    /**
     * 用户注册
     * User registration
     */
    async function register(email, password, role = 'patient') {
        loading.value = true
        error.value = null

        try {
            const userData = await authApi.register(email, password, role)

            // 注册成功后自动登录
            // Auto login after successful registration
            await login(email, password)

            return userData
        } catch (err) {
            error.value = err.response?.data?.detail || 'Registration failed'
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * 用户登录
     * User login
     */
    async function login(email, password) {
        loading.value = true
        error.value = null

        try {
            // 获取令牌
            // Get tokens
            const tokens = await authApi.login(email, password)
            setTokens(tokens.access_token, tokens.refresh_token)

            // 获取用户信息
            // Get user info
            await fetchCurrentUser()

            return user.value
        } catch (err) {
            error.value = err.response?.data?.detail || 'Login failed'
            clearTokens()
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * 获取当前用户信息
     * Fetch current user info
     */
    async function fetchCurrentUser() {
        if (!accessToken.value) return null

        try {
            // 确保Header已设置
            // Ensure header is set
            http.defaults.headers.common['Authorization'] = `Bearer ${accessToken.value}`

            const userData = await authApi.getCurrentUser()
            user.value = userData
            return userData
        } catch (err) {
            // 令牌无效，尝试刷新
            // Token invalid, try refresh
            if (err.response?.status === 401 && refreshToken.value) {
                try {
                    await refreshTokens()
                    return await fetchCurrentUser()
                } catch {
                    clearTokens()
                }
            }
            throw err
        }
    }

    /**
     * 刷新令牌
     * Refresh tokens
     */
    async function refreshTokens() {
        if (!refreshToken.value) {
            throw new Error('No refresh token available')
        }

        try {
            const tokens = await authApi.refreshToken(refreshToken.value)
            setTokens(tokens.access_token, tokens.refresh_token)
            return tokens
        } catch (err) {
            clearTokens()
            throw err
        }
    }

    /**
     * 用户登出
     * User logout
     */
    async function logout() {
        try {
            if (accessToken.value) {
                await authApi.logout()
            }
        } catch {
            // 忽略登出错误
            // Ignore logout errors
        } finally {
            clearTokens()
        }
    }

    /**
     * 初始化认证状态（应用启动时调用）
     * Initialize auth state (called on app startup)
     */
    async function initialize() {
        if (accessToken.value) {
            try {
                await fetchCurrentUser()
            } catch {
                // 令牌无效，清除
                // Token invalid, clear it
                clearTokens()
            }
        }
    }

    return {
        // State
        user,
        accessToken,
        refreshToken,
        loading,
        error,

        // Computed
        isAuthenticated,
        userRole,
        isAdmin,

        // Actions
        register,
        login,
        logout,
        fetchCurrentUser,
        refreshTokens,
        initialize,
        clearTokens
    }
})
