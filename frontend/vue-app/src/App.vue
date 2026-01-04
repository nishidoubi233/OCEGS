<template>
  <a-config-provider :theme="themeConfig">
    <a-layout class="app-layout">
      <!-- Header -->
      <a-layout-header class="app-header">
        <div class="header-content">
          <div class="logo-section">
            <router-link to="/" class="logo-link">
              <span class="logo-icon">🩺</span>
              <span class="logo-text">OCEGS</span>
            </router-link>
          </div>
          <nav class="nav-links">
            <router-link to="/" class="nav-link">Home</router-link>
            <router-link to="/consultation" class="nav-link">Consultation</router-link>
            
            <!-- 认证相关链接 -->
            <!-- Auth related links -->
            <template v-if="authStore.isAuthenticated">
              <a-dropdown>
                <a class="user-menu" @click.prevent>
                  <span class="user-avatar">👤</span>
                  <span class="user-email">{{ authStore.user?.email }}</span>
                  <span class="dropdown-arrow">▾</span>
                </a>
                <template #overlay>
                  <a-menu>
                    <a-menu-item key="profile" @click="$router.push('/profile')">
                      <span>👤 Health Profile</span>
                    </a-menu-item>
                    <a-menu-divider />
                    <a-menu-item key="logout" @click="handleLogout">
                      <span>🚪 Sign Out</span>
                    </a-menu-item>
                  </a-menu>
                </template>
              </a-dropdown>
            </template>
            <template v-else>
              <router-link to="/login" class="nav-link auth-link">Sign In</router-link>
            </template>
          </nav>
        </div>
      </a-layout-header>

      <!-- Main Content -->
      <a-layout-content class="app-content">
        <router-view />
      </a-layout-content>

      <!-- Footer -->
      <a-layout-footer class="app-footer">
        <p>OCEGS © 2026 - AI-Powered Medical Consultation</p>
        <p class="disclaimer">⚠️ For informational purposes only. Seek professional medical advice for health concerns.</p>
      </a-layout-footer>
    </a-layout>
  </a-config-provider>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { theme, message } from 'ant-design-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// 主题配置 - 青绿色医疗主题
// Theme config - Cyan/teal medical theme
const themeConfig = {
  algorithm: theme.defaultAlgorithm,
  token: {
    colorPrimary: '#12c6c6',
    borderRadius: 10,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
  },
}

// 初始化认证状态
// Initialize auth state
onMounted(async () => {
  await authStore.initialize()
})

// 处理登出
// Handle logout
async function handleLogout() {
  await authStore.logout()
  message.success('You have been signed out')
  router.push('/')
}
</script>

<style>
/* Global Styles */
:root {
  --bg: #f3f6fb;
  --card: #ffffff;
  --text: #1b2a3b;
  --muted: #6b7785;
  --primary: #12c6c6;
  --primary-weak: #e6f8f8;
  --line: #e9eef5;
}

* {
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  margin: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: var(--text);
  background: var(--bg);
}

.app-layout {
  min-height: 100vh;
}

.app-header {
  background: var(--card) !important;
  border-bottom: 1px solid var(--line);
  padding: 0 24px !important;
  height: 64px !important;
  line-height: 64px !important;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary);
}

.nav-links {
  display: flex;
  gap: 24px;
}

.nav-link {
  color: var(--text);
  text-decoration: none;
  transition: color 0.2s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--primary);
}

.app-content {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.app-footer {
  text-align: center;
  background: var(--card) !important;
  border-top: 1px solid var(--line);
  padding: 16px 24px !important;
}

.app-footer p {
  margin: 0;
}

.disclaimer {
  font-size: 12px;
  color: var(--muted);
  margin-top: 4px !important;
}

/* Logo链接样式 */
/* Logo link styles */
.logo-link {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
}

/* 用户菜单样式 */
/* User menu styles */
.user-menu {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px;
  border-radius: 20px;
  background: var(--primary-weak);
  color: var(--text);
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}

.user-menu:hover {
  background: var(--primary);
  color: white;
}

.user-avatar {
  font-size: 16px;
}

.user-email {
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 13px;
}

.dropdown-arrow {
  font-size: 10px;
  opacity: 0.7;
}

/* 登录链接样式 */
/* Auth link styles */
.auth-link {
  display: inline-block;
  padding: 8px 20px;
  border-radius: 6px;
  background: var(--primary);
  color: white !important;
  font-weight: 500;
  font-size: 14px;
  line-height: 1.4;
  text-decoration: none;
}

.auth-link:hover {
  filter: brightness(1.1);
}
</style>
