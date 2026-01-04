<template>
  <div class="admin-view">
    <!-- Login Screen -->
    <div v-if="!isLoggedIn" class="admin-login">
      <div class="login-card">
        <div class="login-header">
          <span class="icon">🔐</span>
          <h1>Admin Panel</h1>
          <p>Enter administrator password to continue</p>
        </div>
        <a-form layout="vertical" @submit.prevent="handleLogin">
          <a-form-item label="Password">
            <a-input-password 
              v-model:value="password" 
              placeholder="Enter admin password"
              size="large"
            />
          </a-form-item>
          <a-button type="primary" html-type="submit" block size="large" :loading="loading">
            Login
          </a-button>
        </a-form>
        <div class="login-footer">
          <router-link to="/">← Back to Home</router-link>
        </div>
      </div>
    </div>

    <!-- Admin Dashboard -->
    <div v-else class="admin-dashboard">
      <div class="admin-header">
        <div class="header-left">
          <span class="icon">⚙️</span>
          <h1>OCEGS Admin Panel</h1>
        </div>
        <a-button @click="handleLogout">Logout</a-button>
      </div>

      <div class="admin-content">
        <!-- Status Cards -->
        <div class="status-grid">
          <div class="status-card">
            <div class="stat-value">{{ status.total_users }}</div>
            <div class="stat-label">Total Users</div>
          </div>
          <div class="status-card">
            <div class="stat-value">{{ status.total_consultations }}</div>
            <div class="stat-label">Consultations</div>
          </div>
          <div class="status-card">
            <div class="stat-value">{{ status.active_consultations }}</div>
            <div class="stat-label">Active Sessions</div>
          </div>
          <div class="status-card highlight">
            <div class="stat-value">{{ status.default_provider }}</div>
            <div class="stat-label">AI Provider</div>
          </div>
        </div>

        <!-- Settings Tabs -->
        <a-tabs v-model:activeKey="activeTab" class="settings-tabs">
          <a-tab-pane key="providers" tab="AI Providers">
            <div class="settings-section">
              <h3>API Keys Configuration</h3>
              <p class="section-desc">Configure your AI provider API keys. These are stored securely in the database.</p>
              
              <div class="setting-form">
                <div class="setting-item" v-for="provider in providers" :key="provider.key">
                  <div class="setting-header">
                    <span class="provider-name">{{ provider.label }}</span>
                    <a-tag v-if="getSettingValue(provider.key)" color="green">Configured</a-tag>
                    <a-tag v-else color="orange">Not Set</a-tag>
                  </div>
                  <a-input-group compact>
                    <a-input 
                      v-model:value="settingValues[provider.key]" 
                      :placeholder="provider.placeholder"
                      type="password"
                      style="width: calc(100% - 80px)"
                    />
                    <a-button type="primary" @click="saveSetting(provider.key)">Save</a-button>
                  </a-input-group>
                </div>
              </div>
            </div>
          </a-tab-pane>

          <a-tab-pane key="model" tab="Default Model">
            <div class="settings-section">
              <h3>Default AI Model</h3>
              <p class="section-desc">Set the default AI provider and model for all consultations.</p>
              
              <a-form layout="vertical">
                <a-form-item label="Default Provider">
                  <a-select v-model:value="settingValues.default_provider" style="width: 300px">
                    <a-select-option value="openai">OpenAI</a-select-option>
                    <a-select-option value="anthropic">Anthropic</a-select-option>
                    <a-select-option value="gemini">Google Gemini</a-select-option>
                    <a-select-option value="siliconflow">SiliconFlow (硅基流动)</a-select-option>
                  </a-select>
                </a-form-item>
                <a-form-item label="Default Model Name">
                  <a-input 
                    v-model:value="settingValues.default_model" 
                    placeholder="e.g., gpt-4, claude-3-opus, Pro/THUDM/glm-4-9b-chat"
                    style="width: 400px"
                  />
                </a-form-item>
                <a-button type="primary" @click="saveModelConfig">Save Model Configuration</a-button>
              </a-form>
            </div>
          </a-tab-pane>

          <a-tab-pane key="doctors" tab="Doctor Team">
            <div class="settings-section">
              <h3>AI Doctor Team Configuration</h3>
              <p class="section-desc">Manage the team of AI doctors participating in consultations.</p>
              
              <div class="doctors-list">
                <div 
                  v-for="(doc, index) in doctorsConfig" 
                  :key="doc.id" 
                  class="doctor-config-item"
                >
                  <div class="doc-header">
                    <span class="doc-name">{{ doc.name }}</span>
                    <span class="doc-name-cn">{{ doc.name_cn }}</span>
                    <a-tag :color="doc.status === 'active' ? 'green' : 'default'">
                      {{ doc.status === 'active' ? 'Active' : 'Inactive' }}
                    </a-tag>
                  </div>
                  <div class="doc-settings">
                    <a-select v-model:value="doc.provider" style="width: 150px" size="small">
                      <a-select-option value="openai">OpenAI</a-select-option>
                      <a-select-option value="anthropic">Anthropic</a-select-option>
                      <a-select-option value="siliconflow">SiliconFlow</a-select-option>
                    </a-select>
                    <a-input v-model:value="doc.model" placeholder="Model" size="small" style="width: 200px" />
                    <a-switch 
                      v-model:checked="doc.status" 
                      :checked-value="'active'" 
                      :un-checked-value="'inactive'" 
                      size="small"
                    />
                  </div>
                </div>
              </div>
              <a-button type="primary" @click="saveDoctorsConfig" style="margin-top: 16px">
                Save Doctor Team
              </a-button>
            </div>
          </a-tab-pane>
        </a-tabs>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import adminApi from '@/api/admin'

const password = ref('')
const isLoggedIn = ref(false)
const loading = ref(false)
const activeTab = ref('providers')

const status = reactive({
  total_users: 0,
  total_consultations: 0,
  active_consultations: 0,
  default_provider: 'siliconflow',
  default_model: 'Pro/THUDM/glm-4-9b-chat'
})

const providers = [
  { key: 'openai_api_key', label: 'OpenAI', placeholder: 'sk-...' },
  { key: 'anthropic_api_key', label: 'Anthropic', placeholder: 'sk-ant-...' },
  { key: 'gemini_api_key', label: 'Google Gemini', placeholder: 'AIza...' },
  { key: 'siliconflow_api_key', label: 'SiliconFlow', placeholder: 'sk-...' }
]

const settingValues = reactive({
  openai_api_key: '',
  anthropic_api_key: '',
  gemini_api_key: '',
  siliconflow_api_key: '',
  default_provider: 'siliconflow',
  default_model: 'Pro/THUDM/glm-4-9b-chat'
})

const settingsFromServer = ref([])
const doctorsConfig = ref([])

// 检查本地存储的 token
// Check local storage for token
onMounted(() => {
  const token = localStorage.getItem('admin_token')
  if (token) {
    isLoggedIn.value = true
    loadDashboardData()
  }
})

const handleLogin = async () => {
  if (!password.value) {
    message.warning('Please enter password')
    return
  }
  loading.value = true
  try {
    const res = await adminApi.login(password.value)
    if (res.success) {
      localStorage.setItem('admin_token', res.token)
      isLoggedIn.value = true
      message.success('Login successful')
      loadDashboardData()
    } else {
      message.error(res.message || 'Invalid password')
    }
  } catch (err) {
    message.error('Login failed')
  } finally {
    loading.value = false
  }
}

const handleLogout = () => {
  localStorage.removeItem('admin_token')
  isLoggedIn.value = false
  password.value = ''
}

const loadDashboardData = async () => {
  try {
    // 加载状态
    // Load status
    const statusRes = await adminApi.getStatus()
    Object.assign(status, statusRes)
    
    // 初始化设置
    // Initialize settings
    await adminApi.initSettings()
    
    // 加载设置
    // Load settings
    const settingsRes = await adminApi.getSettings()
    settingsFromServer.value = settingsRes
    
    // 填充值
    // Populate values
    for (const s of settingsRes) {
      if (settingValues.hasOwnProperty(s.key)) {
        settingValues[s.key] = s.value || ''
      }
    }
    
    // 加载医生配置
    // Load doctors config
    const doctorsRes = await adminApi.getDoctorsConfig()
    doctorsConfig.value = doctorsRes.doctors
  } catch (err) {
    console.error('Failed to load dashboard data', err)
  }
}

const getSettingValue = (key) => {
  const s = settingsFromServer.value.find(x => x.key === key)
  return s && s.display_value && s.display_value !== '****'
}

const saveSetting = async (key) => {
  const value = settingValues[key]
  if (!value) {
    message.warning('Please enter a value')
    return
  }
  try {
    await adminApi.updateSetting(key, value)
    message.success(`${key} saved successfully`)
    loadDashboardData()
  } catch (err) {
    message.error('Failed to save setting')
  }
}

const saveModelConfig = async () => {
  try {
    await adminApi.updateSetting('default_provider', settingValues.default_provider)
    await adminApi.updateSetting('default_model', settingValues.default_model)
    message.success('Model configuration saved')
    loadDashboardData()
  } catch (err) {
    message.error('Failed to save model config')
  }
}

const saveDoctorsConfig = async () => {
  try {
    await adminApi.updateDoctorsConfig(doctorsConfig.value)
    message.success('Doctor team configuration saved')
  } catch (err) {
    message.error('Failed to save doctors config')
  }
}
</script>

<style scoped>
.admin-view {
  min-height: 100vh;
  background: #f5f7f9;
}

.admin-login {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0a2540 0%, #12c6c6 100%);
}

.login-card {
  width: 400px;
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header .icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 16px;
}

.login-header h1 {
  margin: 0;
  color: #333;
}

.login-header p {
  color: #666;
  margin-top: 8px;
}

.login-footer {
  text-align: center;
  margin-top: 20px;
}

.login-footer a {
  color: #12c6c6;
}

.admin-dashboard {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-left .icon {
  font-size: 2rem;
}

.header-left h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.status-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.status-card.highlight {
  background: linear-gradient(135deg, #12c6c6 0%, #0a8a8a 100%);
  color: white;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-top: 4px;
}

.settings-tabs {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.settings-section h3 {
  margin: 0 0 8px 0;
  color: #333;
}

.section-desc {
  color: #666;
  margin-bottom: 24px;
}

.setting-item {
  margin-bottom: 20px;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
}

.setting-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.provider-name {
  font-weight: 600;
  font-size: 1rem;
}

.doctors-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.doctor-config-item {
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #eee;
}

.doc-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.doc-name {
  font-weight: 600;
}

.doc-name-cn {
  color: #666;
  font-size: 0.9rem;
}

.doc-settings {
  display: flex;
  gap: 12px;
  align-items: center;
}

@media (max-width: 900px) {
  .status-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
