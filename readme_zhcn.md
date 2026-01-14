[English](readme.md) · [简体中文](readme_zhcn.md)

---

# OCEGS 项目与部署指南 (Project Progress & Deployment Guide)

本文件为您提供 OCEGS 项目的当前开发进度汇总，以及在 Windows 11 环境下从零开始部署系统的手把手教学。

---

## 1. 项目汇总 (Project Overview)
**OCEGS (Online Consultation and Emergency Guidance System)** 是一款集智能预检、专家会诊与急救指导于一体的在线医疗辅助平台。

### 目前已上线的功能 (Current Features):
1.  **用户账户系统**: 支持用户注册、登录、个人信息维护。
2.  **健康档案管理**: 支持维护基本健康信息、既往病史、过敏史及紧急联系人。
3.  **智能预检分诊 (AI Triage)**:
    - 自动分析主诉症状分级 (Severity 1-5)。
    - 提供初步诊断建议与推荐科室。
    - 识别紧急情况并自动引导。
4.  **专家协同会诊 (AI Panel)**:
    - 自动匹配 12 个科室的 AI 专家（心血管、神经、儿科等）。
    - 专家团队多轮讨论、相互纠错与投票决策。
    - 自动生成结构化的最终诊疗报告。
5.  **急救指导模块 (Emergency Guide)**:
    - 针对 Severity 5 的紧急情况生成即时抢救指令。
    - 根据用户地理位置 (IP) 自动匹配当地急救电话（如 911, 120）。
    - 支持一键呼叫与报警。
6.  **管理员面板 (Admin Panel)**:
    - 通过 `/admin` 进入管理界面。
    - 支持配置 AI 供应商 API Key、默认模型、医生团队。

---

## 2. 部署环境准备 (Prerequisites)
即便您不是开发人员，只要按照以下步骤操作即可。

### 硬件与系统要求:
- 系统: Windows 11 (或 Windows 10)
- 网络: 能够访问外部 AI 服务（OpenAI 或 SiliconFlow）

### 软件安装清单:
1.  **Node.js (用于前端)**: [下载官网](https://nodejs.org/) -> 选择 "LTS" 版本。
2.  **Python 3.10+ (用于后端)**: [下载官网](https://www.python.org/) -> 安装时务必勾选 **"Add Python to PATH"**。
3.  **PostgreSQL (数据库)**: [下载官网](https://www.postgresql.org/download/windows/) -> 安装并设置超级用户密码。

---

## 3. 手把手部署步骤 (Setup Guide)

### 第一步：数据库配置 (Database Setup)
1. 打开 PostgreSQL 的管理工具 **pgAdmin 4**。
2. 登录后，右键 "Databases" -> "Create" -> "Database..."。
3. 数据库名称输入 `ocegs`，点击保存。

### 第二步：后端部署 (Backend Setup)
1.  **打开终端 (CMD 或 PowerShell)**。
2.  进入后端目录：`cd backend`
3.  **创建虚拟环境**:
    ```bash
    python -m venv venv
    ```
4.  **激活虚拟环境** (Windows):
    ```bash
    .\venv\Scripts\activate
    ```
5.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```
6.  **配置文件**:
    - 在 `backend` 文件夹找到 `.env.example`。
    - 将其**复制**并重命名为 `.env`。
    - 使用记事本打开 `.env`，修改以下内容：
      - `DATABASE_URL`: `postgresql+asyncpg://用户名:密码@localhost:5432/ocegs`
      - `SILICONFLOW_API_KEY`: 填入您的 API Key。(选填，可以在/admin管理面板中配置自定义apikey)
      - `ADMIN_PASSWORD`: 请务必修改您的管理员密码（密码默认为ocegs-admin-2026,在生产环境内请务必修改）。
7.  **启动后端** (使用 uvicorn):
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    启动成功后，您可以在浏览器访问 `http://localhost:8000/docs` 查看 API 文档。

### 第三步：前端部署 (Frontend Setup)
1.  **开启一个新的终端窗口**。
2.  进入前端目录：`cd frontend/vue-app`
3.  **安装依赖**:
    ```bash
    npm install
    ```
4.  **启动前端**:
    ```bash
    npm run dev
    ```
5.  **访问系统**: 启动后，终端会显示一个地址（通常是 `http://localhost:5173`），在浏览器打开即可。

---

## 4. 常见配置说明 (Configuration Tips)

### API 配置
目前系统默认优先使用 **SiliconFlow (硅基流动)** 的模型，因为其速度快且价格亲民（兼容 OpenAI 格式）。
- 您也可以通过修改 `.env` 中的 `OPENAI_API_KEY` 来切换至官方服务。
- 更灵活的配置可以通过 **管理员面板** 进行。

### 常用网址(localhost仅为本地开发部署时链接，如果部署成功后请将localhost替换为您的服务器ip或域名)
- **管理员面板**: `http://localhost:5173/admin`
- **用户登录**: `http://localhost:5173/login`
- **用户注册**: `http://localhost:5173/register`
- **API文档**: `http://localhost:8000/docs`


### 个人测试建议
如果您只想快速测试，建议在 `initial_problem` 输入中尝试以下两种极端情况：
1.  "有点感冒，喉咙痛" -> 观察分诊到普通科室。
2.  "刚才突然胸痛剧烈，呼吸快喘不上来了" -> 观察系统触发红色急救警告。

---

## 5. 管理员面板 (Admin Panel)

### 访问方式
在浏览器地址栏输入：`http://localhost:5173/admin`

### 默认密码
- 密码：`ocegs-admin-2024` (可在 `.env` 中修改 `ADMIN_PASSWORD`)

### 管理功能
| 功能 | 说明 |
|------|------|
| **系统状态** | 查看总用户数、会诊数、活跃会话 |
| **AI 供应商配置** | 配置 OpenAI / Anthropic / Gemini / SiliconFlow 的 API Key |
| **默认模型设置** | 选择系统默认使用的 AI 供应商和模型 |
| **医生团队管理** | 启用/禁用 AI 医生、为每个医生配置不同模型 |

---
*注：本项目仍在更新中，如有问题请联系开发者。喜欢的话不妨点个star支持一下作者❤*
