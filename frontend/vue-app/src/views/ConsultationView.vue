<template>
  <div class="consultation-view">
    <!-- Header -->
    <div class="view-header">
      <div class="header-content">
        <span class="header-icon">🩺</span>
        <div class="header-texts">
          <h1>AI Expert Consultation</h1>
          <p>Multi-doctor panel discussion based on your symptoms</p>
        </div>
      </div>
      <div v-if="consultStore.currentConsultation" class="status-badge" :class="consultStore.status">
        {{ (consultStore.status || '').toString().toUpperCase() }}
      </div>
    </div>

    <!-- Tab Navigation -->
    <div class="tab-navigation">
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'new' }" 
        @click="activeTab = 'new'"
      >
        ➕ New Consultation
      </button>
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'history' }" 
        @click="activeTab = 'history'; loadHistory()"
      >
        📜 Consultation History
      </button>
    </div>

    <!-- Main Content -->
    <div class="view-body">
      <!-- History Tab -->
      <div v-if="activeTab === 'history'" class="history-tab card">
        <div v-if="loadingHistory" class="loading-state">
          <a-spin />
          <span>Loading consultation history...</span>
        </div>
        
        <div v-else-if="historyList.length === 0" class="empty-state">
          <p>📭 No consultation records yet.</p>
          <a-button type="primary" @click="activeTab = 'new'">Start Your First Consultation</a-button>
        </div>
        
        <div v-else class="history-list">
          <div 
            v-for="item in historyList" 
            :key="item.id" 
            class="history-card clickable"
            @click="loadConsultationDetail(item)"
          >
            <div class="history-card-header">
              <span class="history-date">{{ formatHistoryDate(item.created_at) }}</span>
              <a-tag :color="getStatusColor(item.status)">{{ item.status }}</a-tag>
            </div>
            <div class="history-card-body">
              <div class="history-info-row">
                <span class="label">Triage Level:</span>
                <span class="value">{{ item.triage_level || 'N/A' }}</span>
              </div>
              <div class="history-info-row" v-if="item.doctors_config">
                <span class="label">Doctors:</span>
                <span class="value">{{ (item.doctors_config || []).map(d => d.name).join(', ') || 'N/A' }}</span>
              </div>
            </div>
            <div class="history-card-action">
              <span class="view-detail">Click to view details →</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Consultation Tab (existing content) -->
      <div v-else class="consultation-container card">
        <template v-if="currentPhase === 'input'">
          <!-- 初始输入表单 -->
          <!-- Initial Input Form -->
          <div class="case-form">
            <div class="form-header">
              <h2>Describe Your Condition</h2>
              <p>Please provide as much detail as possible for accurate analysis.</p>
            </div>
            <a-form layout="vertical" :model="caseForm">
              <a-form-item label="Primary Symptom / Question">
                <a-textarea 
                  v-model:value="caseForm.initial_problem" 
                  placeholder="e.g. I've had a persistent dry cough for 3 weeks..." 
                  :rows="6"
                />
              </a-form-item>
              
              <div class="form-tips">
                <p><strong>Tips for better results:</strong></p>
                <ul>
                  <li>Mention when the symptoms started.</li>
                  <li>Describe the frequency and intensity.</li>
                  <li>Include any medications you're currently taking.</li>
                </ul>
              </div>

              <div class="form-actions">
                <a-button 
                  type="primary" 
                  size="large" 
                  block 
                  :loading="consultStore.loading"
                  @click="handlePreTriage"
                  :disabled="!caseForm.initial_problem.trim()"
                >
                  🔍 Pre-Triage Assessment
                </a-button>
              </div>
            </a-form>
          </div>
        </template>

        <template v-else-if="currentPhase === 'triage'">
          <!-- 分诊结果展示 -->
          <!-- Triage Result Display -->
          <div class="triage-result-overlay">
            <div class="triage-card">
              <div class="triage-header" :class="'level-' + consultStore.triageResult?.severity">
                <div class="severity-badge">
                  Level {{ consultStore.triageResult?.severity }}
                </div>
                <h3>AI Triage Report</h3>
              </div>
              
              <div class="triage-content">
                <div class="triage-section">
                  <label>Summary</label>
                  <p class="summary-text">{{ consultStore.triageResult?.summary }}</p>
                </div>
                
                <div class="triage-grid">
                  <div class="grid-item">
                    <label>Recommended Dept.</label>
                    <div class="value">{{ consultStore.triageResult?.department }}</div>
                  </div>
                  <div class="grid-item">
                    <label>Emergency Status</label>
                    <div class="value" :class="{ 'text-danger': consultStore.triageResult?.is_emergency }">
                      {{ consultStore.triageResult?.is_emergency ? '🚩 EMERGENCY' : '✅ Stable' }}
                    </div>
                  </div>
                </div>

                <div v-if="consultStore.triageResult?.is_emergency" class="emergency-advice">
                  <label>⚠️ Emergency Advice</label>
                  <p>{{ consultStore.triageResult?.emergency_advice }}</p>
                </div>

                <div class="risks-section">
                  <label>Potential Risks</label>
                  <div class="risk-tags">
                    <a-tag v-for="risk in consultStore.triageResult?.risks" :key="risk" color="red">
                      {{ risk }}
                    </a-tag>
                  </div>
                </div>
              </div>

              <div class="triage-footer">
                <a-button @click="currentPhase = 'input'">Back to Edit</a-button>
                <a-button 
                  v-if="consultStore.triageResult?.severity === 5" 
                  type="primary" 
                  danger 
                  :loading="consultStore.loading"
                  @click="handleGetEmergencyGuide"
                >
                  🆘 Get Emergency Guidance
                </a-button>
                <a-button type="primary" :loading="consultStore.loading" @click="handleConfirmStart">
                  Confirm & Start Consultation
                </a-button>
              </div>
            </div>
          </div>
        </template>

        <template v-else-if="currentPhase === 'emergency'">
          <!-- 急救指导展示 -->
          <!-- Emergency Guidance Display -->
          <EmergencyGuide 
            :guide="consultStore.emergencyGuide" 
            @back="currentPhase = 'triage'" 
          />
        </template>

        <template v-else>
          <!-- 聊天展示 -->
          <!-- Chat Display -->
          <div class="consultation-active">
            <ChatDisplay 
              :messages="consultStore.messages" 
              :loading="consultStore.isAdvancing" 
            />
            
            <!-- 底部状态提示 -->
            <!-- Bottom status info -->
            <div class="consultation-footer" v-if="!consultStore.isCompleted">
              <div class="step-progress">
                <a-spin size="small" v-if="consultStore.isAdvancing" />
                <span>{{ currentStatusText }}</span>
              </div>
            </div>

            <!-- Follow-up Input Section (shows when completed or discussing) -->
            <div class="follow-up-section" v-if="!consultStore.isAdvancing">
              <div class="follow-up-input">
                <a-textarea 
                  v-model:value="followUpMessage" 
                  placeholder="Ask a follow-up question or provide more information..."
                  :rows="2"
                  :disabled="sendingFollowUp"
                />
                <a-button 
                  type="primary"
                  :loading="sendingFollowUp"
                  :disabled="!followUpMessage.trim()"
                  @click="handleSendFollowUp"
                >
                  📤 Send
                </a-button>
              </div>
              <p class="follow-up-hint">You can ask follow-up questions and the doctors will respond.</p>
            </div>

            <!-- 最终总结展示 -->
            <!-- Final Summary Display -->
            <div v-if="consultStore.isCompleted && consultStore.summary" class="summary-card">
              <div class="summary-header">
                <span class="icon">📜</span>
                <h3>Final Diagnostic Summary</h3>
                <a-tag color="cyan">By {{ consultStore.summary.best_doctor_name }}</a-tag>
              </div>
              <div class="summary-content markdown-body" v-html="renderMarkdown(consultStore.summary.content)"></div>
              <div class="summary-footer">
                <a-button type="primary" @click="resetConsultation">New Consultation</a-button>
              </div>
            </div>
          </div>
        </template>
      </div>

      <!-- 右侧边栏: 情况摘要 & 统计 -->
      <!-- Sidebar: Case summary & Stats -->
      <div class="view-sidebar" v-if="consultStore.currentConsultation">
        <div class="sidebar-card card">
          <h3>Panel of Doctors</h3>
          <div class="doctor-list">
            <div 
              v-for="doc in consultStore.currentConsultation.doctors_config" 
              :key="doc.id"
              class="doctor-item"
              :class="{ eliminated: doc.status === 'eliminated' }"
            >
              <div class="doc-icon">👨‍⚕️</div>
              <div class="doc-info">
                <span class="doc-name">{{ doc.name }}</span>
                <span class="doc-specialty">{{ doc.name_cn }}</span>
              </div>
              <div v-if="doc.status === 'eliminated'" class="elim-tag">Paused</div>
            </div>
          </div>
        </div>

        <div class="sidebar-card card disclaimer-sidebar">
          <h3>Medical Disclaimer</h3>
          <p>Information provided is AI-generated and for reference only. <strong>In case of emergency, call local emergency services immediately.</strong></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * 核心问诊页面 (复用逻辑)
 * Core Consultation View (Reused logic)
 */
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useConsultationStore } from '@/stores/consultation'
import ChatDisplay from '@/components/consultation/ChatDisplay.vue'
import EmergencyGuide from '@/components/consultation/EmergencyGuide.vue'
import { marked } from 'marked'
import { message } from 'ant-design-vue'
import aiDoctorApi from '@/api/aiDoctor'

const consultStore = useConsultationStore()
const route = useRoute()

// Tab state: 'new' or 'history'
const activeTab = ref(route.query.tab === 'history' ? 'history' : 'new')

// History list
const historyList = ref([])
const loadingHistory = ref(false)

// Load history function
async function loadHistory() {
  if (loadingHistory.value) return
  loadingHistory.value = true
  try {
    const res = await aiDoctorApi.getMyHistory()
    historyList.value = res.data || []
  } catch (err) {
    console.error('Failed to load history:', err)
  } finally {
    loadingHistory.value = false
  }
}

// Format date for history display
function formatHistoryDate(dateStr) {
  if (!dateStr) return 'N/A'
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Get status color
function getStatusColor(status) {
  const colors = {
    'COMPLETED': 'success',
    'DISCUSSING': 'processing',
    'VOTING': 'warning',
    'SUMMARIZING': 'cyan',
    'FAILED': 'error'
  }
  return colors[status] || 'default'
}

// 视图状态: 'input', 'triage', 'chat', 'emergency'
// View phase: 'input', 'triage', 'chat', 'emergency'
const currentPhase = ref('input')

// 病例输入表单
// Case input form
const caseForm = reactive({
  initial_problem: ''
})

// 追问相关状态
// Follow-up related state
const followUpMessage = ref('')
const sendingFollowUp = ref(false)

// 处理追问
// Handle follow-up submission
async function handleSendFollowUp() {
  if (!followUpMessage.value.trim()) return
  
  const consultationId = consultStore.currentConsultation?.id
  if (!consultationId) {
    message.error('No active consultation')
    return
  }
  
  sendingFollowUp.value = true
  try {
    // Send follow-up to backend
    await consultStore.sendFollowUp(consultationId, followUpMessage.value.trim())
    followUpMessage.value = ''
    message.success('Follow-up sent. Doctors are responding...')
    
    // Wait a moment for backend to process
    await new Promise(r => setTimeout(r, 500))
    
    // Force reset isAdvancing flag
    consultStore.isAdvancing = false
    
    // Run consultation again to get doctor responses
    // Note: Don't call loadConsultation here as runConsultation will update messages
    await consultStore.runConsultation(consultationId)
  } catch (err) {
    console.error('Failed to send follow-up:', err)
    message.error('Failed to send follow-up')
  } finally {
    sendingFollowUp.value = false
  }
}

// Load history on mount if tab is history
onMounted(() => {
  if (activeTab.value === 'history') {
    loadHistory()
  }
})

// Load consultation detail and switch to chat view
async function loadConsultationDetail(item) {
  try {
    // Fetch full consultation data
    const res = await aiDoctorApi.getConsultation(item.id)
    const consultation = res.data
    
    // Update store with fetched consultation
    consultStore.currentConsultation = consultation
    consultStore.messages = consultation.messages || []
    
    // Switch to chat phase to display the conversation
    activeTab.value = 'new'
    currentPhase.value = 'chat'
    
    message.success('Consultation loaded successfully')
  } catch (err) {
    console.error('Failed to load consultation:', err)
    message.error('Failed to load consultation details')
  }
}

// 当前状态文本
// Current status text
const currentStatusText = computed(() => {
  if (consultStore.isAdvancing) return 'Experts are analyzing...'
  if (consultStore.status === 'voting') return 'Panel is evaluating options...'
  if (consultStore.status === 'summarizing') return 'Synthesizing final diagnosis...'
  return 'Awaiting next step...'
})

// 渲染 Markdown
// Render Markdown
const renderMarkdown = (text) => {
  if (!text) return ''
  return marked(text)
}

// 1. 进行预检分诊
// 1. Perform pre-triage
const handlePreTriage = async () => {
  try {
    await consultStore.triageSymptom(caseForm.initial_problem)
    currentPhase.value = 'triage'
    message.info('AI Preliminary Triage complete.')
  } catch (err) {
    message.error('Failed to perform triage.')
  }
}

// 2. 确认并正式开始会诊
// 2. Confirm and officially start consultation
const handleConfirmStart = async () => {
  try {
    const res = await consultStore.startNewConsultation(caseForm.initial_problem)
    const consultationId = res.data?.id || consultStore.currentConsultation?.id
    if (!consultationId) {
      message.error('Failed to get consultation ID.')
      return
    }
    currentPhase.value = 'chat'
    message.success('Consultation session created. Discussion starting...')
    // 异步运行整个流程
    // Run full process asynchronously
    consultStore.runConsultation(consultationId)
  } catch (err) {
    message.error('Failed to start consultation.')
  }
}

// 3. 获取急救指导 (仅限 Severity 5)
// 3. Get emergency guidance (Severity 5 only)
const handleGetEmergencyGuide = async () => {
  try {
    // 首先发起会诊以获取 ID
    // First start consultation to get ID
    const res = await consultStore.startNewConsultation(caseForm.initial_problem)
    const consultationId = res.data?.id || consultStore.currentConsultation?.id
    if (!consultationId) {
      message.error('Failed to get consultation ID.')
      return
    }
    // 然后获取急救指南
    // Then fetch emergency guide
    await consultStore.fetchEmergencyGuide(consultationId)
    currentPhase.value = 'emergency'
    message.warning('Entering Emergency Guidance Mode.')
  } catch (err) {
    message.error('Failed to load emergency guidance.')
  }
}

// 重置问诊
// Reset consultation
const resetConsultation = () => {
  consultStore.currentConsultation = null
  consultStore.messages = []
  consultStore.summary = null
  consultStore.triageResult = null
  caseForm.initial_problem = ''
  currentPhase.value = 'input'
}
</script>

<style scoped>
.consultation-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: calc(100vh - 120px);
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  font-size: 2.5rem;
  background: white;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(18, 198, 198, 0.15);
}

.header-texts h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.header-texts p {
  margin: 4px 0 0;
  color: #666;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  background: #eee;
}

.status-badge.discussing { background: #e3f2fd; color: #1976d2; }
.status-badge.voting { background: #fff3e0; color: #f57c00; }
.status-badge.summarizing { background: #f3e5f5; color: #7b1fa2; }
.status-badge.completed { background: #e8f5e9; color: #388e3c; }

/* Tab Navigation */
.tab-navigation {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.tab-btn {
  padding: 10px 20px;
  border: 2px solid #eee;
  background: white;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:hover {
  border-color: #12c6c6;
  color: #12c6c6;
}

.tab-btn.active {
  background: #12c6c6;
  border-color: #12c6c6;
  color: white;
}

/* History Tab */
.history-tab {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.history-card {
  background: #f9fafb;
  border-radius: 12px;
  padding: 16px 20px;
  border: 1px solid #eee;
  transition: all 0.2s;
}

.history-card.clickable {
  cursor: pointer;
}

.history-card:hover {
  border-color: #12c6c6;
  box-shadow: 0 4px 12px rgba(18, 198, 198, 0.1);
}

.history-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.history-date {
  font-weight: 600;
  color: #333;
}

.history-card-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.history-card-action {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #eee;
}

.view-detail {
  font-size: 13px;
  color: #12c6c6;
  font-weight: 500;
}

.history-info-row {
  display: flex;
  gap: 8px;
  font-size: 14px;
}

.history-info-row .label {
  color: #888;
}

.history-info-row .value {
  color: #333;
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 48px;
  color: #888;
}

.empty-state {
  text-align: center;
  padding: 48px;
  color: #888;
}

.empty-state p {
  font-size: 18px;
  margin-bottom: 16px;
}

/* Follow-up Section */
.follow-up-section {
  padding: 16px 20px;
  background: #f9fafb;
  border-top: 1px solid #eee;
}

.follow-up-input {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.follow-up-input .ant-input {
  flex: 1;
}

.follow-up-hint {
  margin: 8px 0 0;
  font-size: 12px;
  color: #888;
}

.view-body {
  display: flex;
  gap: 20px;
  flex: 1;
  overflow: hidden;
}

.consultation-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.consultation-active {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.case-form {
  padding: 40px;
  max-width: 800px;
  margin: 0 auto;
}

.form-header {
  margin-bottom: 30px;
  text-align: center;
}

.form-header h2 {
  font-size: 1.8rem;
  color: #12c6c6;
  margin-bottom: 8px;
}

.form-tips {
  background: #f0fdfa;
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid #12c6c6;
  margin: 20px 0;
}

.form-tips p { margin-bottom: 8px; }
.form-tips ul { padding-left: 20px; margin: 0; }

.consultation-footer {
  padding: 12px 20px;
  background: white;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: center;
}

.step-progress {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #12c6c6;
  font-weight: 600;
}

.summary-card {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  max-width: 800px;
  max-height: 80%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.15);
  border: 2px solid #12c6c6;
  z-index: 100;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.summary-header {
  padding: 16px 20px;
  background: #f0fdfa;
  border-bottom: 1px solid #c7ecee;
  display: flex;
  align-items: center;
  gap: 12px;
}

.summary-header .icon { font-size: 1.5rem; }
.summary-header h3 { margin: 0; flex: 1; color: #008c8c; }

.summary-content {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
  line-height: 1.8;
}

.summary-footer {
  padding: 16px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
}

/* Sidebar styles */
.view-sidebar {
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-card h3 {
  font-size: 1rem;
  margin-bottom: 16px;
  color: #333;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.doctor-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.doctor-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border-radius: 6px;
  background: #f9f9f9;
  border: 1px solid #eee;
}

.doctor-item.eliminated {
  opacity: 0.5;
  filter: grayscale(1);
  background: #f0f0f0;
}

.doc-icon {
  width: 32px;
  height: 32px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ddd;
}

.doc-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.doc-name { font-weight: 600; font-size: 0.9rem; }
.doc-specialty { font-size: 0.75rem; color: #888; }

.elim-tag {
  font-size: 0.7rem;
  padding: 2px 6px;
  background: #999;
  color: white;
  border-radius: 4px;
}

.disclaimer-sidebar p {
  font-size: 0.8rem;
  color: #666;
  line-height: 1.5;
}

.disclaimer-sidebar strong { color: #f5222d; }

.triage-result-overlay {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background-color: #f5f7f9;
}

.triage-card {
  width: 100%;
  max-width: 650px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  overflow: hidden;
  border: 1px solid #eee;
}

.triage-header {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  color: white;
}

/* Severity Colors */
.level-1 { background: #52c41a; } /* Success/Green */
.level-2 { background: #722ed1; } /* Purple */
.level-3 { background: #1890ff; } /* primary/blue */
.level-4 { background: #faad14; } /* Warning/Orange */
.level-5 { background: #f5222d; } /* Danger/Red */

.severity-badge {
  display: inline-block;
  padding: 2px 10px;
  background: rgba(255,255,255,0.2);
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
  width: fit-content;
}

.triage-header h3 {
  margin: 0;
  color: white;
  font-size: 1.4rem;
}

.triage-content {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.triage-section label,
.triage-grid .grid-item label,
.risks-section label,
.emergency-advice label {
  display: block;
  font-size: 0.8rem;
  text-transform: uppercase;
  color: #888;
  margin-bottom: 6px;
  font-weight: 600;
  letter-spacing: 0.05em;
}

.summary-text {
  font-size: 1.1rem;
  color: #333;
  margin: 0;
  line-height: 1.6;
}

.triage-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
}

.grid-item .value {
  font-weight: 700;
  font-size: 1.1rem;
  color: #222;
}

.emergency-advice {
  background: #fff1f0;
  border: 1px solid #ffa39e;
  padding: 16px;
  border-radius: 8px;
}

.emergency-advice p {
  margin: 0;
  color: #cf1322;
  font-weight: 500;
}

.risk-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.triage-footer {
  padding: 16px 24px;
  background: #f9f9f9;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.text-danger { color: #f5222d; }
</style>
