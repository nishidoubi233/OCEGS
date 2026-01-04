<template>
  <div class="chat-display" ref="chatContainer">
    <div class="message-list">
      <div 
        v-for="msg in messages" 
        :key="msg.id" 
        :class="['message-item', msg.sender_type]"
      >
        <!-- 系统消息 -->
        <!-- System Message -->
        <template v-if="msg.sender_type === 'system'">
          <div class="system-message">
            <span class="system-icon">⚙️</span>
            {{ msg.content }}
          </div>
        </template>

        <!-- 角色对话 (患者/医生) -->
        <!-- Role Dialogue (Patient/Doctor) -->
        <template v-else>
          <div class="msg-avatar">
            {{ msg.sender_type === 'patient' ? '👤' : (msg.doctor_avatar || '🩺') }}
          </div>
          <div class="msg-bubble-container">
            <div class="msg-info">
              <span class="msg-author">{{ msg.sender_type === 'patient' ? 'You' : msg.doctor_name }}</span>
              <span class="msg-time">{{ formatTime(msg.created_at) }}</span>
            </div>
            <div class="msg-bubble">
              <div class="msg-content markdown-body" v-html="renderMarkdown(msg.content)"></div>
            </div>
          </div>
        </template>
      </div>

      <!-- 加载提示/打字机占位 -->
      <!-- Loading indicator -->
      <div v-if="loading" class="message-item system">
        <div class="system-message typing">
          <a-spin size="small" />
          <span>Doctor team is investigating...</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * 问诊对话展示组件 (复用自参考项目)
 * Consultation chat display component (Reused from reference)
 */
import { ref, watch, onMounted, nextTick } from 'vue'
import { marked } from 'marked'
import dayjs from 'dayjs'

const props = defineProps({
  messages: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const chatContainer = ref(null)

// 渲染 Markdown 内容
// Render Markdown content
const renderMarkdown = (text) => {
  if (!text) return ''
  return marked(text)
}

// 格式化时间
// Format time
const formatTime = (time) => {
  if (!time) return ''
  return dayjs(time).format('HH:mm')
}

// 自动滚动到底部
// Auto scroll to bottom
const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

// 监听消息变化自动滚动
// Watch for new messages to scroll
watch(() => props.messages.length, scrollToBottom)
watch(() => props.loading, (val) => {
  if (val) scrollToBottom()
})

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.chat-display {
  height: 100%;
  overflow-y: auto;
  padding: 20px;
  background-color: #f5f7f9;
  border-radius: 8px;
  scroll-behavior: smooth;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message-item {
  display: flex;
  width: 100%;
}

/* 系统消息样式 */
/* System message styles */
.system-message {
  margin: 0 auto;
  padding: 6px 16px;
  background-color: #e6f7f7;
  color: #008c8c;
  border-radius: 20px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 8px;
  border: 1px solid #c7ecee;
}

/* 气泡对话样式 */
/* Bubble dialogue styles */
.msg-avatar {
  width: 40px;
  height: 40px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  margin-right: 12px;
  flex-shrink: 0;
}

.msg-bubble-container {
  max-width: 80%;
}

.msg-info {
  margin-bottom: 4px;
  font-size: 0.8rem;
  color: #888;
}

.msg-author {
  font-weight: 600;
  margin-right: 8px;
  color: #444;
}

.msg-bubble {
  padding: 12px 16px;
  border-radius: 4px 16px 16px 16px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  border: 1px solid #eee;
}

/* 患者消息靠右 */
/* Patient message aligned right */
.patient {
  flex-direction: row-reverse;
}

.patient .msg-avatar {
  margin-right: 0;
  margin-left: 12px;
  background-color: #12c6c6;
  color: white;
  border: none;
}

.patient .msg-bubble-container {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.patient .msg-bubble {
  background-color: #12c6c6;
  color: white;
  border: none;
  border-radius: 16px 4px 16px 16px;
}

.patient .msg-author {
  color: #12c6c6;
}

.msg-content {
  line-height: 1.6;
  word-break: break-word;
}

.msg-content :deep(p) { margin: 0; }

.typing {
  background-color: #fff;
  border: 1px solid #12c6c6;
}
</style>
