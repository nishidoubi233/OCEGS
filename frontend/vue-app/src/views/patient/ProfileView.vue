<template>
  <div class="profile-view">
    <!-- Page Header -->
    <div class="page-header card">
      <h1>👤 Health Profile</h1>
      <p class="subtitle">Manage your personal information, medical history, and emergency contacts</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <a-spin size="large" />
      <p>Loading your profile...</p>
    </div>

    <!-- Profile Not Found - Create Form -->
    <div v-else-if="!hasProfile" class="create-profile-section">
      <div class="card create-card">
        <h2>📋 Create Your Health Profile</h2>
        <p>Please fill in your basic information to get started.</p>
        
        <a-form
          :model="createForm"
          @finish="handleCreateProfile"
          layout="vertical"
          class="profile-form"
        >
          <a-row :gutter="16">
            <a-col :span="12">
              <a-form-item
                name="full_name"
                label="Full Name"
                :rules="[{ required: true, message: 'Please enter your name' }]"
              >
                <a-input v-model:value="createForm.full_name" placeholder="John Doe" size="large" />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item name="gender" label="Gender">
                <a-select v-model:value="createForm.gender" placeholder="Select gender" size="large">
                  <a-select-option value="male">Male</a-select-option>
                  <a-select-option value="female">Female</a-select-option>
                  <a-select-option value="other">Other</a-select-option>
                  <a-select-option value="prefer_not_to_say">Prefer not to say</a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
          </a-row>

          <a-row :gutter="16">
            <a-col :span="12">
              <a-form-item name="date_of_birth" label="Date of Birth">
                <a-date-picker v-model:value="createForm.date_of_birth" style="width: 100%" size="large" />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item name="phone" label="Phone Number">
                <a-input v-model:value="createForm.phone" placeholder="+1 234 567 8900" size="large" />
              </a-form-item>
            </a-col>
          </a-row>

          <a-form-item name="address" label="Address">
            <a-textarea v-model:value="createForm.address" placeholder="Your address" :rows="2" />
          </a-form-item>

          <a-form-item>
            <a-button type="primary" html-type="submit" size="large" :loading="saving">
              Create Profile
            </a-button>
          </a-form-item>
        </a-form>
      </div>
    </div>

    <!-- Profile Content -->
    <div v-else class="profile-content">
      <!-- Basic Information -->
      <div class="section card">
        <div class="section-header">
          <h2>📝 Basic Information</h2>
          <a-button type="link" @click="showEditProfile = true">Edit</a-button>
        </div>
        <a-descriptions :column="2" bordered size="small">
          <a-descriptions-item label="Full Name">{{ profile.full_name }}</a-descriptions-item>
          <a-descriptions-item label="Gender">{{ formatGender(profile.gender) }}</a-descriptions-item>
          <a-descriptions-item label="Date of Birth">{{ formatDate(profile.date_of_birth) }}</a-descriptions-item>
          <a-descriptions-item label="Phone">{{ profile.phone || 'Not provided' }}</a-descriptions-item>
          <a-descriptions-item label="Address" :span="2">{{ profile.address || 'Not provided' }}</a-descriptions-item>
        </a-descriptions>
      </div>

      <!-- Medical History -->
      <div class="section card">
        <div class="section-header">
          <h2>🏥 Medical History</h2>
          <a-button type="primary" size="small" @click="showAddHistory = true">+ Add</a-button>
        </div>
        
        <a-empty v-if="!profile.medical_histories?.length" description="No medical history recorded" />
        
        <div v-else class="history-list">
          <div v-for="history in profile.medical_histories" :key="history.id" class="history-item">
            <div class="history-info">
              <div class="history-condition">{{ history.condition }}</div>
              <div class="history-meta">
                <a-tag :color="getStatusColor(history.status)">{{ formatStatus(history.status) }}</a-tag>
                <span v-if="history.diagnosis_date">Diagnosed: {{ formatDate(history.diagnosis_date) }}</span>
              </div>
              <div v-if="history.notes" class="history-notes">{{ history.notes }}</div>
            </div>
            <div class="history-actions">
              <a-button type="link" size="small" @click="editHistory(history)">Edit</a-button>
              <a-popconfirm
                title="Delete this record?"
                @confirm="handleDeleteHistory(history.id)"
              >
                <a-button type="link" danger size="small">Delete</a-button>
              </a-popconfirm>
            </div>
          </div>
        </div>
      </div>

      <!-- Emergency Contacts -->
      <div class="section card">
        <div class="section-header">
          <h2>📞 Emergency Contacts</h2>
          <a-button type="primary" size="small" @click="showAddContact = true">+ Add</a-button>
        </div>
        
        <a-empty v-if="!profile.emergency_contacts?.length" description="No emergency contacts added" />
        
        <div v-else class="contacts-list">
          <div v-for="contact in profile.emergency_contacts" :key="contact.id" class="contact-item">
            <div class="contact-info">
              <div class="contact-name">
                {{ contact.name }}
                <a-tag v-if="contact.is_caretaker" color="green" size="small">Caretaker</a-tag>
              </div>
              <div class="contact-meta">
                <span>{{ contact.relationship }}</span>
                <span>📱 {{ contact.phone }}</span>
              </div>
            </div>
            <div class="contact-actions">
              <a-button type="link" size="small" @click="editContact(contact)">Edit</a-button>
              <a-popconfirm
                title="Delete this contact?"
                @confirm="handleDeleteContact(contact.id)"
              >
                <a-button type="link" danger size="small">Delete</a-button>
              </a-popconfirm>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <a-modal
      v-model:open="showEditProfile"
      title="Edit Profile"
      @ok="handleUpdateProfile"
      :confirmLoading="saving"
    >
      <a-form :model="editForm" layout="vertical">
        <a-form-item label="Full Name">
          <a-input v-model:value="editForm.full_name" />
        </a-form-item>
        <a-form-item label="Gender">
          <a-select v-model:value="editForm.gender">
            <a-select-option value="male">Male</a-select-option>
            <a-select-option value="female">Female</a-select-option>
            <a-select-option value="other">Other</a-select-option>
            <a-select-option value="prefer_not_to_say">Prefer not to say</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="Date of Birth">
          <a-date-picker v-model:value="editForm.date_of_birth" style="width: 100%" />
        </a-form-item>
        <a-form-item label="Phone">
          <a-input v-model:value="editForm.phone" />
        </a-form-item>
        <a-form-item label="Address">
          <a-textarea v-model:value="editForm.address" :rows="2" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- Add/Edit Medical History Modal -->
    <a-modal
      v-model:open="showHistoryModal"
      :title="editingHistory ? 'Edit Medical History' : 'Add Medical History'"
      @ok="handleSaveHistory"
      :confirmLoading="saving"
    >
      <a-form :model="historyForm" layout="vertical">
        <a-form-item label="Condition Name" required>
          <a-input v-model:value="historyForm.condition" placeholder="e.g., Hypertension, Diabetes" />
        </a-form-item>
        <a-form-item label="Diagnosis Date">
          <a-date-picker v-model:value="historyForm.diagnosis_date" style="width: 100%" />
        </a-form-item>
        <a-form-item label="Status">
          <a-select v-model:value="historyForm.status">
            <a-select-option value="active">Active</a-select-option>
            <a-select-option value="chronic">Chronic</a-select-option>
            <a-select-option value="managed">Managed</a-select-option>
            <a-select-option value="resolved">Resolved</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="Notes">
          <a-textarea v-model:value="historyForm.notes" :rows="3" placeholder="Additional information about this condition" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- Add/Edit Emergency Contact Modal -->
    <a-modal
      v-model:open="showContactModal"
      :title="editingContact ? 'Edit Emergency Contact' : 'Add Emergency Contact'"
      @ok="handleSaveContact"
      :confirmLoading="saving"
    >
      <a-form :model="contactForm" layout="vertical">
        <a-form-item label="Contact Name" required>
          <a-input v-model:value="contactForm.name" placeholder="Contact's full name" />
        </a-form-item>
        <a-form-item label="Relationship" required>
          <a-input v-model:value="contactForm.relationship" placeholder="e.g., Spouse, Parent, Sibling" />
        </a-form-item>
        <a-form-item label="Phone Number" required>
          <a-input v-model:value="contactForm.phone" placeholder="+1 234 567 8900" />
        </a-form-item>
        <a-form-item>
          <a-checkbox v-model:checked="contactForm.is_caretaker">
            This contact is my caretaker (will receive health alerts)
          </a-checkbox>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import dayjs from 'dayjs'
import * as patientApi from '@/api/patient'

// 状态
// State
const loading = ref(true)
const saving = ref(false)
const profile = ref(null)
const hasProfile = computed(() => !!profile.value)

// 模态框显示状态
// Modal visibility state
const showEditProfile = ref(false)
const showAddHistory = ref(false)
const showAddContact = ref(false)
const showHistoryModal = computed(() => showAddHistory.value || !!editingHistory.value)
const showContactModal = computed(() => showAddContact.value || !!editingContact.value)

// 编辑中的条目
// Items being edited
const editingHistory = ref(null)
const editingContact = ref(null)

// 表单数据
// Form data
const createForm = reactive({
  full_name: '',
  gender: null,
  date_of_birth: null,
  phone: '',
  address: ''
})

const editForm = reactive({
  full_name: '',
  gender: null,
  date_of_birth: null,
  phone: '',
  address: ''
})

const historyForm = reactive({
  condition: '',
  diagnosis_date: null,
  status: 'active',
  notes: ''
})

const contactForm = reactive({
  name: '',
  relationship: '',
  phone: '',
  is_caretaker: false
})

// 加载患者档案
// Load patient profile
async function loadProfile() {
  loading.value = true
  try {
    profile.value = await patientApi.getMyProfile()
  } catch (err) {
    if (err.response?.status === 404) {
      profile.value = null
    } else {
      message.error('Failed to load profile')
    }
  } finally {
    loading.value = false
  }
}

// 创建档案
// Create profile
async function handleCreateProfile() {
  saving.value = true
  try {
    const data = {
      ...createForm,
      date_of_birth: createForm.date_of_birth?.format('YYYY-MM-DD')
    }
    await patientApi.createProfile(data)
    message.success('Profile created successfully!')
    await loadProfile()
  } catch (err) {
    message.error(err.response?.data?.detail || 'Failed to create profile')
  } finally {
    saving.value = false
  }
}

// 更新档案
// Update profile
async function handleUpdateProfile() {
  saving.value = true
  try {
    const data = {
      ...editForm,
      date_of_birth: editForm.date_of_birth?.format?.('YYYY-MM-DD') || editForm.date_of_birth
    }
    await patientApi.updateProfile(data)
    message.success('Profile updated!')
    showEditProfile.value = false
    await loadProfile()
  } catch (err) {
    message.error('Failed to update profile')
  } finally {
    saving.value = false
  }
}

// 打开编辑档案模态框
// Open edit profile modal
function openEditProfile() {
  Object.assign(editForm, {
    full_name: profile.value.full_name,
    gender: profile.value.gender,
    date_of_birth: profile.value.date_of_birth ? dayjs(profile.value.date_of_birth) : null,
    phone: profile.value.phone,
    address: profile.value.address
  })
  showEditProfile.value = true
}

// 病史操作
// Medical history operations
function editHistory(history) {
  editingHistory.value = history
  Object.assign(historyForm, {
    condition: history.condition,
    diagnosis_date: history.diagnosis_date ? dayjs(history.diagnosis_date) : null,
    status: history.status,
    notes: history.notes
  })
}

async function handleSaveHistory() {
  if (!historyForm.condition) {
    message.error('Please enter condition name')
    return
  }
  
  saving.value = true
  try {
    const data = {
      ...historyForm,
      diagnosis_date: historyForm.diagnosis_date?.format?.('YYYY-MM-DD') || historyForm.diagnosis_date
    }
    
    if (editingHistory.value) {
      await patientApi.updateMedicalHistory(editingHistory.value.id, data)
      message.success('Medical history updated!')
    } else {
      await patientApi.addMedicalHistory(data)
      message.success('Medical history added!')
    }
    
    resetHistoryForm()
    await loadProfile()
  } catch (err) {
    message.error('Failed to save medical history')
  } finally {
    saving.value = false
  }
}

async function handleDeleteHistory(historyId) {
  try {
    await patientApi.deleteMedicalHistory(historyId)
    message.success('Medical history deleted')
    await loadProfile()
  } catch (err) {
    message.error('Failed to delete')
  }
}

function resetHistoryForm() {
  showAddHistory.value = false
  editingHistory.value = null
  Object.assign(historyForm, {
    condition: '',
    diagnosis_date: null,
    status: 'active',
    notes: ''
  })
}

// 紧急联系人操作
// Emergency contact operations
function editContact(contact) {
  editingContact.value = contact
  Object.assign(contactForm, {
    name: contact.name,
    relationship: contact.relationship,
    phone: contact.phone,
    is_caretaker: contact.is_caretaker
  })
}

async function handleSaveContact() {
  if (!contactForm.name || !contactForm.phone) {
    message.error('Please fill in required fields')
    return
  }
  
  saving.value = true
  try {
    if (editingContact.value) {
      await patientApi.updateEmergencyContact(editingContact.value.id, contactForm)
      message.success('Contact updated!')
    } else {
      await patientApi.addEmergencyContact(contactForm)
      message.success('Contact added!')
    }
    
    resetContactForm()
    await loadProfile()
  } catch (err) {
    message.error('Failed to save contact')
  } finally {
    saving.value = false
  }
}

async function handleDeleteContact(contactId) {
  try {
    await patientApi.deleteEmergencyContact(contactId)
    message.success('Contact deleted')
    await loadProfile()
  } catch (err) {
    message.error('Failed to delete')
  }
}

function resetContactForm() {
  showAddContact.value = false
  editingContact.value = null
  Object.assign(contactForm, {
    name: '',
    relationship: '',
    phone: '',
    is_caretaker: false
  })
}

// 格式化函数
// Formatting functions
function formatGender(gender) {
  const map = {
    male: 'Male',
    female: 'Female',
    other: 'Other',
    prefer_not_to_say: 'Prefer not to say'
  }
  return map[gender] || 'Not specified'
}

function formatDate(dateStr) {
  if (!dateStr) return 'Not provided'
  return dayjs(dateStr).format('MMM D, YYYY')
}

function formatStatus(status) {
  const map = {
    active: 'Active',
    chronic: 'Chronic',
    managed: 'Managed',
    resolved: 'Resolved'
  }
  return map[status] || status
}

function getStatusColor(status) {
  const map = {
    active: 'red',
    chronic: 'orange',
    managed: 'blue',
    resolved: 'green'
  }
  return map[status] || 'default'
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.profile-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header {
  padding: 20px 24px;
}

.page-header h1 {
  margin: 0;
  font-size: 24px;
}

.subtitle {
  margin: 8px 0 0;
  color: var(--muted);
}

.loading-container {
  text-align: center;
  padding: 60px;
}

.loading-container p {
  margin-top: 16px;
  color: var(--muted);
}

.create-card {
  max-width: 600px;
  margin: 0 auto;
  padding: 32px;
}

.create-card h2 {
  margin: 0 0 8px;
}

.create-card p {
  color: var(--muted);
  margin-bottom: 24px;
}

.section {
  padding: 20px 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h2 {
  margin: 0;
  font-size: 18px;
}

.history-list,
.contacts-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-item,
.contact-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 12px 16px;
  background: var(--primary-weak);
  border-radius: 8px;
  border: 1px solid var(--line);
}

.history-condition,
.contact-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.history-meta,
.contact-meta {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: var(--muted);
}

.history-notes {
  margin-top: 8px;
  font-size: 13px;
  color: var(--muted);
}

.history-actions,
.contact-actions {
  display: flex;
  gap: 4px;
}
</style>
