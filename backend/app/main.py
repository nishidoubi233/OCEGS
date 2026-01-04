"""
OCEGS - Online Consultation and Emergency Guidance System
FastAPI Application Entry Point
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db, close_db
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    - Startup: Initialize database
    - Shutdown: Close connections
    """
    # Startup
    logger.info(f"Starting {settings.app_name} in {settings.app_env} mode")
    await init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    await close_db()
    logger.info("Database connections closed")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Online Consultation and Emergency Guidance System - AI-powered medical consultation platform",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Health Check Endpoints
# ============================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Basic health check endpoint.
    Returns application status and version.
    """
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": "0.1.0",
        "environment": settings.app_env,
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API welcome message"""
    return {
        "message": f"Welcome to {settings.app_name} API",
        "docs": "/docs" if settings.debug else "Disabled in production",
        "health": "/health",
    }


# ============================================================
# API Routers (to be added in subsequent steps)
# API路由（按步骤添加）
# ============================================================

# Step 2: Authentication
# 认证路由
from app.auth.router import router as auth_router
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])

# Step 2: Users
# from app.users.router import router as users_router
# app.include_router(users_router, prefix="/api/users", tags=["Users"])

# Step 3: Patients
# 患者档案路由
from app.patients.router import router as patients_router
app.include_router(patients_router, prefix="/api/patients", tags=["Patients"])

# Step 4: AI Doctor
# from app.ai_doctor.router import router as ai_doctor_router
# app.include_router(ai_doctor_router, prefix="/api/consultation", tags=["AI Consultation"])

# Step 6: Emergency
# from app.emergency.router import router as emergency_router
# app.include_router(emergency_router, prefix="/api/emergency", tags=["Emergency"])

# Step 7: Chat
# from app.chat.router import router as chat_router
# app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])

# Step 8: Notifications
# from app.notifications.router import router as notifications_router
# app.include_router(notifications_router, prefix="/api/notifications", tags=["Notifications"])


# ============================================================
# Temporary Chat Endpoint (for frontend template testing)
# ============================================================

from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    deepThink: bool = False

class ChatResponse(BaseModel):
    reply: str

@app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
async def temporary_chat(request: ChatRequest):
    """
    Temporary chat endpoint for frontend testing.
    Will be replaced by full AI Doctor implementation in Step 4.
    """
    # Simple echo response for now
    if request.deepThink:
        reply = f"[Deep Thinking Mode] I received your question: '{request.message}'. Full AI consultation will be implemented in Step 4."
    else:
        reply = f"I received your question: '{request.message}'. Full AI consultation will be implemented in Step 4."
    
    return ChatResponse(reply=reply)
