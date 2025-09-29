from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # API 설정
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "StudyMind"
    
    # CORS 설정
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:8501",  # Streamlit 기본 포트
        "http://localhost:3000",
    ]
    
    # OpenAI 설정
    # OPENAI_API_KEY: str
    
    # Claude 설정 (선택)
    ANTHROPIC_API_KEY: str = ""
    
    # 데이터베이스 설정
    DATABASE_URL: str = "sqlite:///./studymind.db"
    
    # FAISS 설정
    FAISS_INDEX_PATH: str = "./db/notion_faiss"
    
    class Config:
        env_file = "../.env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """설정 싱글톤 인스턴스 반환"""
    return Settings()