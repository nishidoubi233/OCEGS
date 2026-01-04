# 智能体 · AI问诊前端

这是一个简洁的对话页面前端，包含：
- 顶部欢迎与示例问题卡片
- 中部聊天气泡区
- 底部输入框与“深度思考”开关
- 预留后端对接的 `POST /api/chat` 接口

## 本地运行

Windows/PowerShell 可用任一方式：

1. Python（若已安装）：
```powershell
cd j:\code\304\frontend
python -m http.server 5500
```
打开浏览器访问 http://localhost:5500 ，点击 `index.html`。

2. Node（若已安装）：
```powershell
cd j:\code\304\frontend
npx serve . -p 5500
```

也可以直接双击 `index.html` 打开（不支持跨域接口调用时请使用本地服务）。

## 后端对接
将 `script.js` 中 `BACKEND_URL` 修改为真实地址，返回格式示例：
```json
{ "reply": "医生建议：多喝水并就医检查…" }
```
如需流式输出，可改为 `fetch` + `ReadableStream` 读取并逐段更新气泡文本。
