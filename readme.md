[English](readme.md) · [简体中文](readme_zhcn.md)

---

# OCEGS Project & Deployment Guide

This document provides a summary of the current development progress for the OCEGS project, along with a step-by-step guide for deploying the system from scratch on Windows 11.

---

## 1. Project Overview
**OCEGS (Online Consultation and Emergency Guidance System)** is an online medical assistance platform integrating intelligent triage, expert consultation, and emergency guidance.

### Current Features:
1.  **User Account System**: Supports user registration, login, and personal profile management.
2.  **Health Records Management**: Allows maintenance of basic health information, medical history, allergy history, and emergency contacts.
3.  **AI Triage**:
    - Automatically analyzes chief complaints and assigns severity levels (1-5).
    - Provides preliminary diagnostic suggestions and recommended departments.
    - Identifies emergencies and provides automatic guidance.
4.  **AI Expert Panel**:
    - Automatically matches AI experts from 12 departments (Cardiology, Neurology, Pediatrics, etc.).
    - The expert team engages in multi-round discussions, mutual error correction, and voting.
    - Automatically generates a structured final diagnosis report.
5.  **Emergency Guide Module**:
    - Generates immediate rescue instructions for Severity 5 emergencies.
    - Automatically matches local emergency numbers (e.g., 911, 120) based on user's geographic location (IP).
    - Supports one-click calling and alerts.
6.  **Admin Panel**:
    - Access the admin interface via `/admin`.
    - Supports configuration of AI provider API Keys, default models, and doctor teams.

---

## 2. Prerequisites
Even if you are not a developer, you can follow these steps to deploy the system.

### Hardware & System Requirements:
- Operating System: Windows 11 (or Windows 10)
- Network: Access to external AI services (OpenAI or SiliconFlow)

### Software Installation Checklist:
1.  **Node.js (for Frontend)**: [Download Here](https://nodejs.org/) -> Select the "LTS" version.
2.  **Python 3.10+ (for Backend)**: [Download Here](https://www.python.org/) -> Make sure to check **"Add Python to PATH"** during installation.
3.  **PostgreSQL (Database)**: [Download Here](https://www.postgresql.org/download/windows/) -> Install and set the superuser password.

---

## 3. Setup Guide

### Step 1: Database Setup
1. Open the PostgreSQL management tool **pgAdmin 4**.
2. After logging in, right-click "Databases" -> "Create" -> "Database...".
3. Enter `ocegs` as the database name and click Save.

### Step 2: Backend Setup
1.  **Open a terminal (CMD or PowerShell)**.
2.  Navigate to the backend directory: `cd backend`
3.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```
4.  **Activate the virtual environment** (Windows):
    ```bash
    .\venv\Scripts\activate
    ```
5.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
6.  **Configuration file**:
    - Find `.env.example` in the `backend` folder.
    - **Copy** it and rename the copy to `.env`.
    - Open `.env` with a text editor and modify the following:
      - `DATABASE_URL`: `postgresql+asyncpg://username:password@localhost:5432/ocegs`
      - `SILICONFLOW_API_KEY`: Enter your API Key. (Optional, you can configure a custom API key in the /admin panel)
      - `ADMIN_PASSWORD`: Be sure to change your admin password (default is ocegs-admin-2026; please change it in production environments).
7.  **Start the backend** (using uvicorn):
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    Once started successfully, you can view the API documentation at `http://localhost:8000/docs` in your browser.

### Step 3: Frontend Setup
1.  **Open a new terminal window**.
2.  Navigate to the frontend directory: `cd frontend/vue-app`
3.  **Install dependencies**:
    ```bash
    npm install
    ```
4.  **Start the frontend**:
    ```bash
    npm run dev
    ```
5.  **Access the system**: After starting, the terminal will display an address (usually `http://localhost:5173`). Open it in your browser.

---

## 4. Configuration Tips

### API Configuration
Currently, the system defaults to using **SiliconFlow** models because of their speed and affordability (OpenAI API compatible).
- You can also switch to the official OpenAI service by modifying `OPENAI_API_KEY` in `.env`.
- More flexible configurations can be made through the **Admin Panel**.

### Common URLs (localhost is only for local development; replace it with your server IP or domain after deployment)
- **Admin Panel**: `http://localhost:5173/admin`
- **User Login**: `http://localhost:5173/login`
- **User Registration**: `http://localhost:5173/register`
- **API Documentation**: `http://localhost:8000/docs`


### Testing Recommendations
If you just want to test quickly, try the following two extreme cases in the `initial_problem` input:
1.  "Slight cold, sore throat" -> Observe triage to a general department.
2.  "Sudden severe chest pain just now, having trouble breathing" -> Observe system triggering a red emergency alert.

---

## 5. Admin Panel

### Access
Enter in the browser address bar: `http://localhost:5173/admin`

### Default Password
- Password: `ocegs-admin-2024` (can be changed in `.env` via `ADMIN_PASSWORD`)

### Admin Functions
| Function | Description |
|----------|-------------|
| **System Status** | View total users, consultations, active sessions |
| **AI Provider Configuration** | Configure API Keys for OpenAI / Anthropic / Gemini / SiliconFlow |
| **Default Model Settings** | Select the default AI provider and model for the system |
| **Doctor Team Management** | Enable/disable AI doctors, configure different models for each doctor |

---
*Note: This project is still being updated. If you have any questions, please contact the developer. If you like it, please give it a star to support the author ❤*
