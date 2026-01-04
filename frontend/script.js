const els = {
  chat: document.getElementById('chatMessages'),
  input: document.getElementById('userInput'),
  form: document.getElementById('composer'),
  send: document.getElementById('sendBtn'),
  prompts: document.querySelectorAll('.prompt'),
  deepThink: document.getElementById('deepThink')
};

// 可配置的后端地址与路由
const BACKEND_URL = '/api/chat'; // 对接时修改为真实地址

function appendMessage(role, text) {
  const item = document.createElement('div');
  item.className = `message ${role}`;
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  item.appendChild(bubble);
  els.chat.appendChild(item);
  els.chat.scrollTop = els.chat.scrollHeight;
}

async function sendMessage(message) {
  const useDeepThink = !!els.deepThink.checked;

  // 展示用户消息
  appendMessage('me', message);

  // 占位的“思考中”消息
  const thinking = document.createElement('div');
  thinking.className = 'message assistant';
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = 'Thinking…';
  thinking.appendChild(bubble);
  els.chat.appendChild(thinking);
  els.chat.scrollTop = els.chat.scrollHeight;

  try {
    // 预留对接：将用户输入发给后端
    const resp = await fetch(BACKEND_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, deepThink: useDeepThink })
    });

    if (!resp.ok) throw new Error('Network error ' + resp.status);

    const data = await resp.json();
    // Backend returns { reply: 'text' }
    bubble.textContent = data.reply ?? '(Response will appear after backend is connected)';
  } catch (err) {
    bubble.textContent = 'Error: ' + err.message;
  }
}

// 表单提交
els.form.addEventListener('submit', (e) => {
  e.preventDefault();
  const text = (els.input.value || '').trim();
  if (!text) return;
  els.input.value = '';
  sendMessage(text);
});

// 回车发送（移动端兼容保持由表单处理）
els.input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    els.form.requestSubmit();
  }
});

// Example prompts: click to send
els.prompts.forEach(btn => {
  btn.addEventListener('click', () => {
    els.input.value = btn.textContent.trim();
    els.form.requestSubmit();
  });
});

// Optional greeting
appendMessage('assistant', 'Hello! I am your health assistant. Ask me anything about common health questions, and I can provide suggestions.');
