from pydantic import BaseModel, Field
from typing import Optional

class ScheduleExtractorResponse(BaseModel):
    title: Optional[str] = Field(None, description="추출된 이벤트 제목")
    course_name: Optional[str] = Field(None, description="과목명 또는 관련 기관")
    date: Optional[str] = Field(None, description="추출된 날짜 (YYYY-MM-DD 형식)")
    time: Optional[str] = Field(None, description="추출된 시간 (HH:MM 형식)")
    deadline: Optional[str] = Field(None, description="마감일 (존재 시)")
    location: Optional[str] = Field(None, description="장소 정보")
    raw_text: str = Field(..., description="OCR로 추출된 원본 텍스트 전체")
    parsing_status: str = Field(..., description="파싱 상태 (SUCCESS, PARTIAL, FAILED)")
    confidence: float = Field(..., description="OCR 신뢰도 또는 정확도 (0.0 ~ 1.0)")

class CalendarEventRequest(BaseModel):
    title: str = Field(..., description="이벤트 제목")
    date: str = Field(..., description="이벤트 날짜 (YYYY-MM-DD)")
    time: str = Field(..., description="이벤트 시간 (HH:MM)")
    location: Optional[str] = Field(None, description="이벤트 장소")
    description: Optional[str] = Field(None, description="이벤트 설명 및 메모")

class CalendarPreviewResponse(BaseModel):
    summary: str
    location: Optional[str]
    description: Optional[str]
    start: dict
    end: dict
