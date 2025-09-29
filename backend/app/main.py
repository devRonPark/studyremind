from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.routes import health

settings = get_settings()

# FastAPI 앱 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["health"])
app.include_router(health.router, tags=["root"])  # 루트 경로용


@app.on_event("startup")
async def startup_event():
    """앱 시작 시 실행"""
    print(f"🚀 {settings.PROJECT_NAME} API Starting...")
    print(f"📝 Docs: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """앱 종료 시 실행"""
    print(f"👋 {settings.PROJECT_NAME} API Shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )