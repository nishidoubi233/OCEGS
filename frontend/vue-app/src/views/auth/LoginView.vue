<template>
  <div class="auth-view">
    <!-- Logo & Title -->
    <div class="auth-header">
      <div class="logo-circle">🩺</div>
      <h1>OCEGS</h1>
      <p class="tagline">Online Consultation and Emergency Guidance System</p>
    </div>

    <!-- Auth Card -->
    <div class="auth-card card">
      <!-- Tab Switcher -->
      <div class="tab-switcher">
        <button 
          :class="['tab', { active: mode === 'login' }]"
          @click="mode = 'login'"
        >
          Sign In
        </button>
        <button 
          :class="['tab', { active: mode === 'register' }]"
          @click="mode = 'register'"
        >
          Sign Up
        </button>
      </div>

      <!-- Login Form -->
      <a-form
        v-if="mode === 'login'"
        :model="loginForm"
        @finish="handleLogin"
        layout="vertical"
        class="auth-form"
      >
        <a-form-item
          name="email"
          :rules="[
            { required: true, message: 'Please enter your email' },
            { type: 'email', message: 'Please enter a valid email' }
          ]"
        >
          <a-input
            v-model:value="loginForm.email"
            size="large"
            placeholder="Email address"
          >
            <template #prefix>📧</template>
          </a-input>
        </a-form-item>

        <a-form-item
          name="password"
          :rules="[{ required: true, message: 'Please enter your password' }]"
        >
          <a-input-password
            v-model:value="loginForm.password"
            size="large"
            placeholder="Password"
          >
            <template #prefix>🔒</template>
          </a-input-password>
        </a-form-item>

        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            size="large"
            block
            :loading="authStore.loading"
          >
            Sign In
          </a-button>
        </a-form-item>
      </a-form>

      <!-- Register Form -->
      <a-form
        v-else
        :model="registerForm"
        @finish="handleRegister"
        layout="vertical"
        class="auth-form"
      >
        <a-form-item
          name="email"
          :rules="[
            { required: true, message: 'Please enter your email' },
            { type: 'email', message: 'Please enter a valid email' }
          ]"
        >
          <a-input
            v-model:value="registerForm.email"
            size="large"
            placeholder="Email address"
          >
            <template #prefix>📧</template>
          </a-input>
        </a-form-item>

        <a-form-item
          name="password"
          :rules="[
            { required: true, message: 'Please enter a password' },
            { min: 8, message: 'Password must be at least 8 characters' }
          ]"
        >
          <a-input-password
            v-model:value="registerForm.password"
            size="large"
            placeholder="Password (min 8 characters)"
          >
            <template #prefix>🔒</template>
          </a-input-password>
        </a-form-item>

        <a-form-item
          name="confirmPassword"
          :rules="[
            { required: true, message: 'Please confirm your password' },
            { validator: validateConfirmPassword }
          ]"
        >
          <a-input-password
            v-model:value="registerForm.confirmPassword"
            size="large"
            placeholder="Confirm password"
          >
            <template #prefix>🔒</template>
          </a-input-password>
        </a-form-item>

        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            size="large"
            block
            :loading="authStore.loading"
          >
            Create Account
          </a-button>
        </a-form-item>
      </a-form>

      <!-- Error Display -->
      <a-alert
        v-if="authStore.error"
        :message="authStore.error"
        type="error"
        show-icon
        closable
        class="error-alert"
        @close="authStore.error = null"
      />
    </div>

    <!-- Disclaimer -->
    <p class="disclaimer">
      By signing in, you agree to our Terms of Service and Privacy Policy.
      This system provides health guidance only, not medical diagnosis.
    </p>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// 当前模式：login 或 register
// Current mode: login or register
const mode = ref('login')

// 登录表单
// Login form
const loginForm = reactive({
  email: '',
  password: ''
})

// 注册表单
// Register form
const registerForm = reactive({
  email: '',
  password: '',
  confirmPassword: ''
})

/**
 * 验证确认密码
 * Validate confirm password
 */
const validateConfirmPassword = async (rule, value) => {
  if (value !== registerForm.password) {
    throw new Error('Passwords do not match')
  }
}

/**
 * 处理登录
 * Handle login
 */
async function handleLogin() {
  try {
    await authStore.login(loginForm.email, loginForm.password)
    message.success('Welcome back!')
    router.push('/')
  } catch (err) {
    // 错误已在store中处理
    // Error already handled in store
  }
}

/**
 * 处理注册
 * Handle registration
 */
async function handleRegister() {
  try {
    await authStore.register(registerForm.email, registerForm.password)
    message.success('Account created successfully!')
    router.push('/')
  } catch (err) {
    // 错误已在store中处理
    // Error already handled in store
  }
}
</script>

<style scoped>
.auth-view {
  min-height: calc(100vh - 160px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  background: linear-gradient(135deg, var(--primary), #29d3d3);
  margin: 0 auto 16px;
  box-shadow: 0 8px 24px rgba(18, 198, 198, 0.3);
}

.auth-header h1 {
  margin: 0;
  font-size: 32px;
  color: var(--primary);
}

.tagline {
  color: var(--muted);
  margin: 8px 0 0;
}

.auth-card {
  width: 100%;
  max-width: 400px;
  padding: 32px;
}

.tab-switcher {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}

.tab {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid var(--line);
  background: transparent;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  color: var(--muted);
  cursor: pointer;
  transition: all 0.2s;
}

.tab:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.tab.active {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.auth-form {
  margin-top: 16px;
}

.error-alert {
  margin-top: 16px;
}

.disclaimer {
  max-width: 400px;
  text-align: center;
  font-size: 12px;
  color: var(--muted);
  margin-top: 24px;
  line-height: 1.5;
}
</style>
