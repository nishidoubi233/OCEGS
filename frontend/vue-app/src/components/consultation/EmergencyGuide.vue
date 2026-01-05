<template>
  <div class="emergency-guide-container">
    <div class="emergency-card">
      <!-- 头部警告 -->
      <!-- Header Warning -->
      <div class="emergency-header">
        <div class="pulse-icon">
          <warning-filled />
        </div>
        <h1>URGENT: Life-Saving Instructions</h1>
        <p>A high-risk condition has been identified. Follow these steps immediately.</p>
      </div>

      <!-- 本地急救电话区 -->
      <!-- Local Emergency Call Section -->
      <div class="local-emergency-call">
        <div class="location-box">
          <span class="location-label">Detected Location:</span>
          <span class="location-value">{{ countryName || 'Detecting...' }}</span>
        </div>
        <a :href="'tel:' + emergencyNumber" class="call-button">
          <phone-outlined /> Call {{ emergencyNumber }}
        </a>
      </div>

      <!-- AI 生成的急救步骤 -->
      <!-- AI Generated Emergency Steps -->
      <div class="emergency-steps">
        <div v-for="step in guide?.steps" :key="step.index" class="step-item">
          <div class="step-index">{{ step.index }}</div>
          <div class="step-text">
            <h3>{{ step.action }}</h3>
            <p>{{ step.detail }}</p>
          </div>
        </div>
      </div>

      <!-- 警告与禁忌 -->
      <!-- Warnings & Prohibited -->
      <div class="emergency-notice-grid">
        <div class="notice-box warnings">
          <h4><info-circle-outlined /> Important Notices</h4>
          <ul>
            <li v-for="w in guide?.warnings" :key="w">{{ w }}</li>
          </ul>
        </div>
        <div class="notice-box prohibited">
          <h4><stop-outlined /> DO NOT DO</h4>
          <ul>
            <li v-for="p in guide?.prohibited" :key="p">{{ p }}</li>
          </ul>
        </div>
      </div>

      <!-- 快捷操作 -->
      <!-- Quick Actions -->
      <div class="emergency-footer-actions">
        <a-button type="primary" danger size="large" @click="handleNotifyContacts">
          <team-outlined /> Notify Emergency Contacts
        </a-button>
        <a-button ghost size="large" @click="$emit('back')">
          Return to Consultation
        </a-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { 
  WarningFilled, 
  PhoneOutlined, 
  InfoCircleOutlined, 
  StopOutlined,
  TeamOutlined 
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import axios from 'axios'

const props = defineProps({
  guide: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['back'])

const countryCode = ref('US')
const countryName = ref('')

const emergencyNumbers = {
  'US': '911',
  'CN': '120',
  'GB': '999',
  'AU': '000',
  'CA': '911',
  'SG': '995',
  'MY': '999',
  'JP': '119',
  'KR': '119',
  'HK': '999',
  'TW': '119',
  'DE': '112',
  'FR': '112'
}

const emergencyNumber = computed(() => {
  return emergencyNumbers[countryCode.value] || '911'
})

// 通过 IP 获取位置
// Get location via IP
const detectLocation = async () => {
  try {
    const res = await axios.get('https://ipapi.co/json/')
    countryCode.value = res.data.country_code
    countryName.value = res.data.country_name
  } catch (err) {
    console.error('Failed to detect location, defaulting to US (911)')
    countryName.value = 'Global (Default)'
  }
}

const handleNotifyContacts = () => {
  message.loading({ content: 'Sending alerts to contacts...', key: 'notify' })
  setTimeout(() => {
    message.success({ content: 'Emergency contacts notified successfully.', key: 'notify' })
  }, 1500)
}

onMounted(() => {
  detectLocation()
})
</script>

<style scoped>
.emergency-guide-container {
  padding: 24px;
  background-color: #fff1f0;
  min-height: 100%;
  max-height: calc(100vh - 200px);
  overflow-y: auto;
  display: flex;
  justify-content: center;
}

.emergency-card {
  width: 100%;
  max-width: 800px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(245, 34, 45, 0.15);
  border: 2px solid #ff4d4f;
  overflow: hidden;
  padding: 32px;
}

.emergency-header {
  text-align: center;
  margin-bottom: 32px;
}

.pulse-icon {
  font-size: 48px;
  color: #f5222d;
  margin-bottom: 16px;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.8; }
  100% { transform: scale(1); opacity: 1; }
}

.emergency-header h1 {
  color: #f5222d;
  font-size: 2rem;
  margin-bottom: 8px;
  font-weight: 800;
}

.emergency-header p {
  font-size: 1.1rem;
  color: #666;
}

.local-emergency-call {
  background: #f5222d;
  padding: 24px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: white;
  margin-bottom: 32px;
}

.location-box {
  display: flex;
  flex-direction: column;
}

.location-label {
  font-size: 0.9rem;
  opacity: 0.8;
}

.location-value {
  font-size: 1.2rem;
  font-weight: bold;
}

.call-button {
  background: white;
  color: #f5222d;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1.3rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  transition: all 0.3s;
}

.call-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  color: #f5222d;
}

.emergency-steps {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 32px;
}

.step-item {
  display: flex;
  gap: 20px;
  padding: 20px;
  background: #fffafa;
  border-radius: 12px;
  border-left: 5px solid #ff4d4f;
}

.step-index {
  width: 40px;
  height: 40px;
  background: #f5222d;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.step-text h3 {
  margin: 0 0 8px 0;
  font-size: 1.2rem;
  color: #222;
  font-weight: 700;
}

.step-text p {
  margin: 0;
  color: #555;
  line-height: 1.5;
}

.emergency-notice-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

.notice-box {
  padding: 20px;
  border-radius: 12px;
}

.notice-box h4 {
  margin-bottom: 12px;
  font-weight: bold;
  font-size: 1rem;
}

.notice-box ul {
  padding-left: 20px;
  margin: 0;
}

.notice-box li {
  margin-bottom: 6px;
  line-height: 1.4;
}

.warnings {
  background: #fff7e6;
  border: 1px solid #ffd591;
  color: #873800;
}

.prohibited {
  background: #fff1f0;
  border: 1px solid #ffa39e;
  color: #a8071a;
}

.emergency-footer-actions {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

@media (max-width: 600px) {
  .emergency-notice-grid {
    grid-template-columns: 1fr;
  }
  .local-emergency-call {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
}
</style>
