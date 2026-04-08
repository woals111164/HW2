from app.models.schemas import CalendarEventRequest, CalendarPreviewResponse
from app.utils.logger import logger

class CalendarService:
    @staticmethod
    def generate_calendar_event(request_data: CalendarEventRequest) -> CalendarPreviewResponse:
        """
        FastAPI 클라이언트에서 전송한 정제된 일정 데이터를
        Google Calendar v3 API Event 스키마(RFC3339)에 맞게 매핑하여 리턴합니다.
        
        실제 연동 시에는 여기서 google-api-python-client 를 호출하여
        users().events().insert(...) 메서드를 실행하는 파이프라인으로 확장 가능합니다.
        """
        logger.info(f"Generating calendar event format for: {request_data.title}")
        
        # 시간 문자열 조합 (단순 예시)
        # Google Calendar API는 "2024-11-20T14:00:00" 형태의 ISO 포맷을 권장합니다.
        # 시간대가 생략되었지만, 여기서는 timezone='Asia/Seoul' 이라고 가정합니다.
        start_datetime = f"{request_data.date}T{request_data.time}:00"
        
        # 시작 시간 기준 1시간 뒤를 기본 종료 시간으로 설정한다고 가정 (간략화)
        # 파이썬 datetime 모듈을 쓰면 더욱 정확하지만, 과제 수준의 형태 시연을 위해 간략 처리
        end_time_prefix = request_data.time.split(":")[0]
        end_hour = str(int(end_time_prefix) + 1).zfill(2)
        end_datetime = f"{request_data.date}T{end_hour}:{request_data.time.split(':')[1]}:00"
        
        event_dict = {
            "summary": request_data.title,
            "location": request_data.location or "미정",
            "description": request_data.description or "OCR로 추출 및 등록된 자동 일정",
            "start": {
                "dateTime": start_datetime,
                "timeZone": "Asia/Seoul",
            },
            "end": {
                "dateTime": end_datetime,
                "timeZone": "Asia/Seoul",
            }
        }
        
        # [TODO: 실제 Google OAuth 2.0 및 Token 기반 캘린더 등록 로직 추가 지점]
        # creds = get_credentials()
        # service = build('calendar', 'v3', credentials=creds)
        # event_result = service.events().insert(calendarId='primary', body=event_dict).execute()
        
        return CalendarPreviewResponse(**event_dict)

calendar_service_instance = CalendarService()
