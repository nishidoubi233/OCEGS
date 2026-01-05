<template>
  <div class="home-view">
    <!-- Hero Section -->
    <div class="hero card">
      <div class="welcome">
        <div class="avatar">🩺</div>
        <div class="texts">
          <h1>Welcome to OCEGS 👋</h1>
          <p class="sub">Your AI-powered health assistant. Get medical guidance, manage your health profile, and receive emergency support.</p>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="actions-grid">
      <router-link to="/consultation" class="action-card card">
        <span class="action-icon">💬</span>
        <h3>Start Consultation</h3>
        <p>Chat with our AI medical assistant for health guidance</p>
      </router-link>

      <!-- Health Profile - Step 3 已完成 / Implemented -->
      <router-link to="/profile" class="action-card card">
        <span class="action-icon">📋</span>
        <h3>Health Profile</h3>
        <p>Manage your medical history and health records</p>
      </router-link>

      <!-- Emergency Guidance - Step 6 已完成 / Implemented -->
      <router-link to="/consultation" class="action-card card">
        <span class="action-icon">🚨</span>
        <h3>Emergency Guidance</h3>
        <p>Get immediate first-aid instructions</p>
        <span class="feature-hint">Via Consultation Triage</span>
      </router-link>

      <!-- Caretaker Connect - Step 8 未完成 / Not Implemented -->
      <div class="action-card card disabled">
        <span class="action-icon">👥</span>
        <h3>Caretaker Connect</h3>
        <p>Link with family members for emergency alerts</p>
        <span class="coming-soon">Coming Soon</span>
      </div>
    </div>

    <!-- Consultation History -->
    <div class="history-section card" v-if="isLoggedIn">
      <div class="section-header">
        <h2 class="section-title">📜 Consultation History</h2>
        <router-link to="/consultation?tab=history" class="view-all" v-if="consultationHistory.length > 0">View All →</router-link>
      </div>
      
      <div v-if="loadingHistory" class="loading-state">
        <a-spin />
        <span>Loading history...</span>
      </div>
      
      <div v-else-if="consultationHistory.length === 0" class="empty-state">
        <p>No consultation records yet.</p>
        <router-link to="/consultation" class="start-link">Start your first consultation →</router-link>
      </div>
      
      <div v-else class="history-list">
        <div 
          v-for="item in consultationHistory.slice(0, 5)" 
          :key="item.id" 
          class="history-item"
        >
          <div class="history-info">
            <span class="history-date">{{ formatDate(item.created_at) }}</span>
            <a-tag :color="getStatusColor(item.status)">{{ item.status }}</a-tag>
          </div>
          <div class="history-triage">
            Triage Level: {{ item.triage_level || 'N/A' }}
          </div>
        </div>
      </div>
    </div>

    <!-- System Status -->
    <div class="status-section card">
      <h2 class="section-title">System Status</h2>
      <a-descriptions :column="2" bordered size="small">
        <a-descriptions-item label="Frontend">
          <a-tag color="success">Running</a-tag>
        </a-descriptions-item>
        <a-descriptions-item label="Backend">
          <a-tag :color="backendStatus === 'healthy' ? 'success' : 'error'">
            {{ backendStatus === 'healthy' ? 'Connected' : 'Disconnected' }}
          </a-tag>
        </a-descriptions-item>
        <a-descriptions-item label="Version">V1.1.4</a-descriptions-item>
      </a-descriptions>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import aiDoctorApi from '@/api/aiDoctor'

const authStore = useAuthStore()
const backendStatus = ref('checking')
const consultationHistory = ref([])
const loadingHistory = ref(false)

const isLoggedIn = computed(() => authStore.isAuthenticated)

onMounted(async () => {
  // Check backend health
  try {
    const response = await axios.get('/health')
    backendStatus.value = response.data.status
  } catch (error) {
    backendStatus.value = 'error'
  }
  
  // Load consultation history if logged in
  if (isLoggedIn.value) {
    loadingHistory.value = true
    try {
      const res = await aiDoctorApi.getMyHistory()
      consultationHistory.value = res.data || []
    } catch (err) {
      console.error('Failed to load history:', err)
    } finally {
      loadingHistory.value = false
    }
  }
})

function formatDate(dateStr) {
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
</script>

<style scoped>
.home-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.hero {
  padding: 24px;
}

.welcome {
  display: flex;
  gap: 16px;
  align-items: center;
}

.avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 28px;
  background: linear-gradient(135deg, var(--primary), #29d3d3);
}

.texts h1 {
  margin: 0;
  font-size: 24px;
}

.texts .sub {
  margin: 8px 0 0;
  color: var(--muted);
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.action-card {
  text-decoration: none;
  color: var(--text);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  position: relative;
}

.action-card:hover:not(.disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(18, 198, 198, 0.15);
}

.action-card.disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.action-icon {
  font-size: 32px;
  display: block;
  margin-bottom: 12px;
}

.action-card h3 {
  margin: 0 0 8px;
  font-size: 16px;
}

.action-card p {
  margin: 0;
  font-size: 14px;
  color: var(--muted);
}

.coming-soon {
  position: absolute;
  top: 12px;
  right: 12px;
  font-size: 11px;
  background: #fff3e0;
  color: #e65100;
  padding: 2px 8px;
  border-radius: 4px;
}

.feature-hint {
  position: absolute;
  top: 12px;
  right: 12px;
  font-size: 11px;
  background: var(--primary-weak);
  color: var(--primary);
  padding: 2px 8px;
  border-radius: 4px;
}

.status-section {
  margin-top: 8px;
}

/* History Section Styles */
.history-section {
  margin-top: 8px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.view-all {
  color: var(--primary);
  text-decoration: none;
  font-size: 14px;
}

.view-all:hover {
  text-decoration: underline;
}

.loading-state {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 24px;
  justify-content: center;
  color: var(--muted);
}

.empty-state {
  text-align: center;
  padding: 32px;
  color: var(--muted);
}

.empty-state p {
  margin: 0 0 12px;
}

.start-link {
  color: var(--primary);
  text-decoration: none;
}

.start-link:hover {
  text-decoration: underline;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--bg);
  border-radius: 8px;
  transition: background 0.2s;
}

.history-item:hover {
  background: var(--primary-weak);
}

.history-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.history-date {
  font-size: 14px;
  color: var(--text);
}

.history-triage {
  font-size: 13px;
  color: var(--muted);
}
</style>
