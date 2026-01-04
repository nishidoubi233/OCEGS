<template>
  <div class="consultation-view">
    <!-- Header -->
    <div class="chat-header card">
      <div class="welcome">
        <div class="avatar">🩺</div>
        <div class="texts">
          <h1>AI Medical Consultation 👋</h1>
          <p class="sub">I'm your health assistant. Ask me anything about health—I'll provide guidance based on medical knowledge.</p>
        </div>
      </div>
    </div>

    <!-- Chat Area -->
    <div class="chat-area card">
      <!-- Messages -->
      <div class="messages" ref="messagesContainer">
        <!-- Welcome message -->
        <div v-if="messages.length === 0" class="prompt-box">
          <p class="prompt-header">✨ Quick start prompts:</p>
          <div class="starter-prompts">
            <button 
              v-for="prompt in starterPrompts" 
              :key="prompt"
              class="prompt-btn"
              @click="sendMessage(prompt)"
            >
              {{ prompt }}
            </button>
          </div>
        </div>

        <!-- Chat messages -->
        <div 
          v-for="(msg, index) in messages" 
          :key="index"
          :class="['message', msg.role]"
        >
          <div class="bubble">
            <div v-if="msg.role === 'assistant' && msg.loading" class="loading">
              Thinking...
            </div>
            <template v-else>{{ msg.content }}</template>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="input-area">
        <div class="input-row">
          <label class="deep-think-toggle">
            <input type="checkbox" v-model="deepThink" />
            <span>Deep Thinking</span>
          </label>
          <form class="composer" @submit.prevent="handleSend">
            <input 
              v-model="inputText"
              type="text"
              placeholder="Ask me anything about health..."
              :disabled="isLoading"
            />
            <a-button 
              type="primary" 
              html-type="submit"
              :loading="isLoading"
              :disabled="!inputText.trim() || isLoading"
            >
              Send
            </a-button>
          </form>
        </div>
      </div>
    </div>

    <!-- Disclaimer -->
    <div class="disclaimer-box">
      <a-alert
        type="warning"
        show-icon
        message="Medical Disclaimer"
        description="This AI assistant provides general health information only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a healthcare provider for medical concerns."
      />
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import http from '@/api/http'

const messages = ref([])
const inputText = ref('')
const deepThink = ref(false)
const isLoading = ref(false)
const messagesContainer = ref(null)

const starterPrompts = [
  'What are the symptoms of kidney stones?',
  'What medicine helps with eczema?',
  'What are the side effects of aspirin?',
]

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const sendMessage = async (text) => {
  const messageText = text || inputText.value.trim()
  if (!messageText) return

  // Clear input
  inputText.value = ''

  // Add user message
  messages.value.push({
    role: 'user',
    content: messageText,
  })

  // Add loading message
  const loadingIndex = messages.value.length
  messages.value.push({
    role: 'assistant',
    content: '',
    loading: true,
  })

  scrollToBottom()
  isLoading.value = true

  try {
    const response = await http.post('/chat', {
      message: messageText,
      deepThink: deepThink.value,
    })

    // Update with actual response
    messages.value[loadingIndex] = {
      role: 'assistant',
      content: response.data.reply,
      loading: false,
    }
  } catch (error) {
    messages.value[loadingIndex] = {
      role: 'assistant',
      content: `Error: ${error.message || 'Failed to get response'}`,
      loading: false,
    }
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

const handleSend = () => {
  sendMessage()
}
</script>

<style scoped>
.consultation-view {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: calc(100vh - 160px);
}

.chat-header {
  padding: 16px 20px;
  flex-shrink: 0;
}

.welcome {
  display: flex;
  gap: 12px;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 22px;
  background: linear-gradient(135deg, var(--primary), #29d3d3);
}

.texts h1 {
  margin: 0;
  font-size: 18px;
}

.texts .sub {
  margin: 4px 0 0;
  color: var(--muted);
  font-size: 14px;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 0;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.prompt-box {
  background: var(--primary-weak);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 16px;
}

.prompt-header {
  margin: 0 0 12px;
  color: var(--muted);
  font-weight: 600;
}

.starter-prompts {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.prompt-btn {
  text-align: left;
  padding: 12px 14px;
  border-radius: 10px;
  border: 1px solid var(--line);
  background: white;
  color: var(--text);
  cursor: pointer;
  transition: transform 0.12s, box-shadow 0.12s;
}

.prompt-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(18, 198, 198, 0.18);
}

.message {
  max-width: 75%;
  margin: 8px 0;
}

.message.user {
  margin-left: auto;
}

.message .bubble {
  padding: 12px 16px;
  border-radius: 16px;
  background: #f7fafc;
  border: 1px solid var(--line);
}

.message.user .bubble {
  background: #e8fff9;
  border-color: #c9f1e8;
}

.message.assistant .bubble {
  background: #f1fbff;
  border-color: #cceef3;
}

.loading {
  color: var(--muted);
  font-style: italic;
}

.input-area {
  padding: 12px 16px;
  border-top: 1px solid var(--line);
  flex-shrink: 0;
}

.input-row {
  display: flex;
  gap: 12px;
  align-items: center;
}

.deep-think-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #eef5ff;
  border: 1px solid var(--line);
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  white-space: nowrap;
  font-size: 13px;
  color: var(--muted);
}

.deep-think-toggle input {
  accent-color: var(--primary);
}

.composer {
  flex: 1;
  display: flex;
  gap: 8px;
  background: #f7f9fc;
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 8px;
}

.composer input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 14px;
  color: var(--text);
}

.disclaimer-box {
  flex-shrink: 0;
}
</style>
