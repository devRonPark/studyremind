from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# 기본 응답 모델
class HealthResponse(BaseModel):
    """헬스체크 응답"""
    status: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)