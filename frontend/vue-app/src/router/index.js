/**
 * OCEGS Vue Router配置
 * OCEGS Vue Router Configuration
 */
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('@/views/HomeView.vue'),
        meta: { requiresProfile: true },
    },
    {
        path: '/consultation',
        name: 'Consultation',
        component: () => import('@/views/ConsultationView.vue'),
        meta: { requiresAuth: true, requiresProfile: true },
    },
    // 认证路由
    // Auth routes
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/auth/LoginView.vue'),
        meta: { guest: true },
    },
    // 患者档案路由
    // Patient profile routes
    {
        path: '/profile',
        name: 'Profile',
        component: () => import('@/views/patient/ProfileView.vue'),
        meta: { requiresAuth: true },
    },
    // Step 6: Emergency routes
    // {
    //   path: '/emergency',
    //   name: 'Emergency',
    //   component: () => import('@/views/emergency/EmergencyView.vue'),
    // },
    // Admin Panel
    // 管理面板
    {
        path: '/admin',
        name: 'Admin',
        component: () => import('@/views/AdminView.vue'),
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// 路由守卫 - 检查认证状态
// Route guard - Check authentication status
router.beforeEach(async (to, from, next) => {
    // 延迟导入以避免循环依赖
    // Lazy import to avoid circular dependency
    const { useAuthStore } = await import('@/stores/auth')
    const authStore = useAuthStore()

    // 如果有token但没有用户信息，尝试获取
    // If has token but no user info, try to fetch
    if (authStore.accessToken && !authStore.user) {
        try {
            await authStore.fetchCurrentUser()
        } catch {
            // 令牌无效，继续
            // Token invalid, continue
        }
    }

    // 需要认证的路由
    // Routes requiring authentication
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next({ name: 'Login', query: { redirect: to.fullPath } })
        return
    }

    // 访客专用路由（已登录用户重定向）
    // Guest-only routes (redirect authenticated users)
    if (to.meta.guest && authStore.isAuthenticated) {
        next({ name: 'Home' })
        return
    }

    // 需要填写个人资料的路由
    // Routes requiring profile completion
    if (to.meta.requiresProfile && authStore.isAuthenticated) {
        // 检查用户是否已填写个人资料
        // Check if user has completed profile
        try {
            const { default: http } = await import('@/api/http')
            const res = await http.get('/patients/profile')
            // If has profile data, continue navigation
            if (res.data && res.data.id) {
                next()
                return
            }
            // 有响应但没有有效 profile，重定向到 /profile
            // Response but no valid profile, redirect to /profile
            if (to.name !== 'Profile') {
                next({ name: 'Profile' })
                return
            }
        } catch (err) {
            // 404 或其他错误意味着没有 profile
            // 404 or other error means no profile exists
            if (to.name !== 'Profile') {
                next({ name: 'Profile' })
                return
            }
        }
    }

    next()
})

export default router
