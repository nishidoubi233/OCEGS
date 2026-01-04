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
          <a-tab-pane key="config" tab="AI Configuration">
            <div class="settings-section">
              <h3>Global AI Settings (OpenAI Compatible)</h3>
              <p class="section-desc">Configure your AI endpoint. Supports any OpenAI-compatible API (official, third-party proxies, etc.).</p>
              
              <a-form layout="vertical">
                <a-form-item label="Default API Key">
                  <a-input-password 
                    v-model:value="settingValues.default_api_key" 
                    placeholder="sk-..."
                    size="large"
                  />
                </a-form-item>
                
                <a-form-item label="Default Base URL">
                  <a-input 
                    v-model:value="settingValues.default_base_url" 
                    placeholder="https://api.openai.com/v1/chat/completions"
                    size="large"
                  />
                  <div class="hint">Leave empty for official OpenAI. Use your proxy URL for third-party services.</div>
                </a-form-item>
                
                <a-form-item label="Default Model">
                  <div class="model-selector">
                    <a-auto-complete
                      v-model:value="settingValues.default_model"
                      :options="availableModels"
                      placeholder="Select or type model name..."
                      style="flex: 1"
                      size="large"
                      :filter-option="filterModelOption"
                    />
                    <a-button @click="loadModels" :loading="loadingModels" size="large">
                      Load Models
                    </a-button>
                  </div>
                  <div class="hint">Click "Load Models" to fetch available models from your API, or type manually.</div>
                </a-form-item>
                
                <a-button type="primary" @click="saveGlobalConfig" size="large">Save Global Configuration</a-button>
              </a-form>
            </div>
          </a-tab-pane>

          <a-tab-pane key="triage" tab="Triage Settings">
            <div class="settings-section">
              <h3>Triage AI Configuration (Optional)</h3>
              <p class="section-desc">Separate AI settings for triage. Leave empty to use global defaults.</p>
              
              <a-form layout="vertical">
                <a-form-item label="Triage API Key">
                  <a-input-password 
                    v-model:value="settingValues.triage_api_key" 
                    placeholder="Leave empty to use global"
                    size="large"
                  />
                </a-form-item>
                
                <a-form-item label="Triage Base URL">
                  <a-input 
                    v-model:value="settingValues.triage_base_url" 
                    placeholder="Leave empty to use global"
                    size="large"
                  />
                </a-form-item>
                
                <a-form-item label="Triage Model">
                  <div class="model-selector">
                    <a-auto-complete
                      v-model:value="settingValues.triage_model"
                      :options="availableModels"
                      placeholder="Leave empty to use global"
                      style="flex: 1"
                      size="large"
                      :filter-option="filterModelOption"
                    />
                    <a-button @click="loadModels" :loading="loadingModels" size="large">
                      Load Models
                    </a-button>
                  </div>
                </a-form-item>
                
                <a-button type="primary" @click="saveTriageConfig" size="large">Save Triage Configuration</a-button>
              </a-form>
            </div>
          </a-tab-pane>

          <a-tab-pane key="doctors" tab="Doctor Team">
            <div class="settings-section">
              <h3>AI Doctor Team Configuration</h3>
              <p class="section-desc">Each doctor can have custom API Key, Base URL, and Model. Leave empty to use global defaults.</p>
              
              <div class="doctors-list">
                <div 
                  v-for="(doc, index) in doctorsConfig" 
                  :key="doc.id" 
                  class="doctor-config-item"
                >
                  <div class="doc-header">
                    <div class="doc-identity">
                      <span class="doc-name">{{ doc.name }}</span>
                      <span class="doc-name-cn">{{ doc.name_cn }}</span>
                    </div>
                    <a-switch 
                      v-model:checked="doc.status" 
                      :checked-value="'active'" 
                      :un-checked-value="'inactive'" 
                      checked-children="Active"
                      un-checked-children="Off"
                    />
                  </div>
                  <div class="doc-settings-grid">
                    <div class="setting-field">
                      <label>API Key</label>
                      <a-input-password 
                        v-model:value="doc.api_key" 
                        placeholder="Use global default" 
                        size="small"
                      />
                    </div>
                    <div class="setting-field">
                      <label>Base URL</label>
                      <a-input 
                        v-model:value="doc.base_url" 
                        placeholder="Use global default" 
                        size="small"
                      />
                    </div>
                    <div class="setting-field">
                      <label>Model</label>
                      <a-input 
                        v-model:value="doc.model" 
                        placeholder="gpt-4, claude-3-opus..."
                        size="small"
                      />
                    </div>
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
const activeTab = ref('config')

const status = reactive({
  total_users: 0,
  total_consultations: 0,
  active_consultations: 0,
  default_model: ''
})

// 统一 AI 配置
// Unified AI Config
const settingValues = reactive({
  default_api_key: '',
  default_base_url: '',
  default_model: '',
  triage_api_key: '',
  triage_base_url: '',
  triage_model: ''
})

const settingsFromServer = ref([])
const doctorsConfig = ref([])

// 模型加载
// Model loading
const availableModels = ref([])
const loadingModels = ref(false)

const loadModels = async () => {
  if (!settingValues.default_api_key) {
    message.warning('Please enter API Key first')
    return
  }
  loadingModels.value = true
  try {
    const res = await adminApi.fetchModels(settingValues.default_api_key, settingValues.default_base_url)
    const data = res.data
    if (data.success && data.models) {
      availableModels.value = data.models.map(m => ({ value: m.id, label: m.name }))
      message.success(`Loaded ${data.models.length} models`)
    } else {
      message.error(data.error || 'Failed to load models')
    }
  } catch (err) {
    message.error('Failed to fetch models from API')
  } finally {
    loadingModels.value = false
  }
}

const filterModelOption = (inputValue, option) => {
  return option.value.toLowerCase().includes(inputValue.toLowerCase())
}

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
    const data = res.data
    if (data.success) {
      localStorage.setItem('admin_token', data.token)
      isLoggedIn.value = true
      message.success('Login successful')
      loadDashboardData()
    } else {
      message.error(data.message || 'Invalid password')
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
    Object.assign(status, statusRes.data)
    
    // 初始化设置
    // Initialize settings
    await adminApi.initSettings()
    
    // 加载设置
    // Load settings
    const settingsRes = await adminApi.getSettings()
    settingsFromServer.value = settingsRes.data
    
    // 填充值 - 不覆盖已有的 secret 值
    // Populate values - don't overwrite existing secret values with empty
    for (const s of settingsRes.data) {
      if (settingValues.hasOwnProperty(s.key)) {
        // 如果是 secret 且后端返回空，保留当前值
        // If secret and backend returns empty, keep current value
        if (s.is_secret && !s.value && settingValues[s.key]) {
          continue
        }
        settingValues[s.key] = s.value || ''
      }
    }
    
    // 加载医生配置
    // Load doctors config
    const doctorsRes = await adminApi.getDoctorsConfig()
    doctorsConfig.value = doctorsRes.data.doctors
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

const saveGlobalConfig = async () => {
  try {
    if (settingValues.default_api_key) {
      await adminApi.updateSetting('default_api_key', settingValues.default_api_key)
    }
    await adminApi.updateSetting('default_base_url', settingValues.default_base_url || '')
    await adminApi.updateSetting('default_model', settingValues.default_model || '')
    message.success('Global AI configuration saved')
    loadDashboardData()
  } catch (err) {
    message.error('Failed to save configuration')
  }
}

const saveTriageConfig = async () => {
  try {
    await adminApi.updateSetting('triage_api_key', settingValues.triage_api_key || '')
    await adminApi.updateSetting('triage_base_url', settingValues.triage_base_url || '')
    await adminApi.updateSetting('triage_model', settingValues.triage_model || '')
    message.success('Triage configuration saved')
    loadDashboardData()
  } catch (err) {
    message.error('Failed to save triage config')
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
  justify-content: space-between;
  margin-bottom: 12px;
}

.doc-identity {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.doc-name {
  font-weight: 600;
}

.doc-name-cn {
  color: #666;
  font-size: 0.9rem;
}

.doc-settings-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.setting-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.setting-field label {
  font-size: 0.8rem;
  color: #666;
}

.hint {
  font-size: 0.8rem;
  color: #888;
  margin-top: 4px;
}

.model-selector {
  display: flex;
  gap: 12px;
  align-items: center;
}

@media (max-width: 900px) {
  .status-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .doc-settings-grid {
    grid-template-columns: 1fr;
  }
}
</style>
