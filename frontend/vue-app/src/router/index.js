/**
 * OCEGS Vue Router Configuration
 */
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('@/views/HomeView.vue'),
    },
    {
        path: '/consultation',
        name: 'Consultation',
        component: () => import('@/views/ConsultationView.vue'),
        // meta: { requiresAuth: true }, // Enable in Step 2
    },
    // Step 2: Auth routes
    // {
    //   path: '/login',
    //   name: 'Login',
    //   component: () => import('@/views/auth/LoginView.vue'),
    // },
    // {
    //   path: '/register',
    //   name: 'Register',
    //   component: () => import('@/views/auth/RegisterView.vue'),
    // },
    // Step 3: Patient routes
    // {
    //   path: '/profile',
    //   name: 'Profile',
    //   component: () => import('@/views/patient/ProfileView.vue'),
    //   meta: { requiresAuth: true },
    // },
    // Step 6: Emergency routes
    // {
    //   path: '/emergency',
    //   name: 'Emergency',
    //   component: () => import('@/views/emergency/EmergencyView.vue'),
    // },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// Route guard (enable in Step 2)
// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()
//   if (to.meta.requiresAuth && !authStore.isAuthenticated) {
//     next({ name: 'Login' })
//   } else {
//     next()
//   }
// })

export default router
