from fastapi import APIRouter, File, UploadFile, HTTPException, status
from app.models.schemas import ScheduleExtractorResponse, CalendarEventRequest, CalendarPreviewResponse
from app.services.ocr_service import ocr_service_instance
from app.services.parser_service import ParserService
from app.services.calendar_service import calendar_service_instance
from app.utils.logger import logger

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """서버 상태 확인용 Endpoint"""
    return {"status": "ok"}

@router.post("/extract", response_model=ScheduleExtractorResponse)
async def extract_schedule_from_image(file: UploadFile = File(...)):
    """
    공지 이미지를 업로드받아 OCR 수행 후 일정 정보(JSON)를 추출하여 반환합니다.
    """
    # 1. 파일 검증
    if not file.content_type.startswith("image/"):
        logger.error(f"Invalid file type uploaded: {file.content_type}")
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")
        
    try:
        image_bytes = await file.read()
        logger.info(f"Image received. Filename: {file.filename}, Size: {len(image_bytes)} bytes")
        
        # 2. OCR 모듈 호출 (텍스트 추출)
        raw_target_text = ocr_service_instance.extract_text(image_bytes)
        
        # 3. Parser 로직으로 필요한 필드 추출
        parsed_result = ParserService.parse_extracted_text(raw_target_text)
        
        # 4. 상태/기타 메타데이터 채우기 (confidence 등은 Mock 값)
        resp_data = {
            **parsed_result,
            "raw_text": raw_target_text,
            "parsing_status": "SUCCESS" if parsed_result.get("date") else "PARTIAL",
            "confidence": 0.95
        }
        logger.info("Schedule extraction successful.")
        return ScheduleExtractorResponse(**resp_data)
        
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Error during extraction process: {e}")
        raise HTTPException(status_code=500, detail="서버 내부 처리 중 오류가 발생했습니다.")

@router.post("/preview-event", response_model=CalendarPreviewResponse)
def preview_calendar_event(request_data: CalendarEventRequest):
    """
    추출된 일정 데이터를 구글 캘린더 등록 형태(JSON)로 변환/매핑하여 반환합니다.
    (이 후 클라이언트가 이 데이터를 확인하고 승인하면 실제 Calendar API에 등록하도록 파이프라인 구성 가능)
    """
    try:
        preview_data = calendar_service_instance.generate_calendar_event(request_data)
        return preview_data
    except Exception as e:
        logger.error(f"Error mapping calendar event: {e}")
        raise HTTPException(status_code=500, detail="캘린더 정보 매핑 중 오류가 발생했습니다.")
