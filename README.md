# OCR Event Extractor API

이 프로젝트는 공지사항이나 안내 이미지를 업로드하여 OCR로 텍스트를 추출하고, 
일정 정보(과목, 날짜, 시간, 장소 등)를 구조화한 뒤 향후 Google Calendar에 
쉽게 추가할 수 있도록 변환해 주는 FastAPI 기반 백엔드 과제/MLOps 서비스입니다.

## 🚀 프로젝트 목표 빛 MLOps/서비스 파이프라인 관점 특징

이 서비스는 **요청 수신 $\to$ OCR 추론 $\to$ 정규식 후처리 $\to$ 정형 파싱 $\to$ 캘린더 매핑** 이라는 일련의 
파이프라인을 구축한 마이크로서비스 설계 예시입니다. 

- **확장성 보장 (Interface Design)**: `services/ocr_service.py`와 `services/calendar_service.py`를 인터페이스화하여, 추후 무거운 OCR 딥러닝 모델(TrOCR 등)이나 상용 API(Google Cloud Vision)를 손쉽게 교체할 수 있습니다.
- **RESTful API**: FastAPI를 사용해 빠르고 명확하게 정의된 라우터 구조. Pydantic을 이용한 스키마 검증으로 API의 입력/출력 불량 형태를 방지합니다.
- **로깅 (Monitoring/Observability 준비)**: `app/core/logger.py`에 별도 채널을 둠으로써 향후 MLOps 파이프라인에서의 디버깅과 로깅(Logstash/Kibana 등) 확장이 수월합니다.
- **Containerization**: `Dockerfile`을 통해 모델과 서버를 한 번에 패키징하여, 쿠버네티스(K8s)나 컨테이너 플랫폼 위에 쉽게 배포할 수 있도록 구성했습니다.

## 📁 프로젝트 구조

```text
ocr_calendar_api/
├── app/
│   ├── main.py                 # FastAPI Application (Entry point)
│   ├── api/
│   │   └── routes.py           # API 라우팅 모음 (/health, /extract, /preview-event)
│   ├── core/
│   │   └── logger.py           # 로깅 유틸
│   ├── models/
│   │   └── schemas.py          # Request, Response 데이터 스키마 (Pydantic)
│   └── services/
│       ├── ocr_service.py      # 이미지 텍스트 추출 서비스 (현재 인터페이스/Mock)
│       ├── parser_service.py   # OCR 추출 텍스트에서 정규식으로 일정 파싱
│       └── calendar_service.py # Google Calendar 데이터 형태 매핑 및 연동 골격
├── Dockerfile                  # 도커 이미지 빌드 파일
├── requirements.txt            # 파이썬 의존성 목록
└── README.md                   # 본 설명서
```

## 🛠️ 실행 방법

### 로컬 환경 (Local)
1. 의존성 설치: `pip install -r requirements.txt`
2. 서버 실행: `uvicorn app.main:app --reload`
3. Swagger UI 확인: 브라우저에서 `http://127.0.0.0:8000/docs` 접속

### Docker 환경
1. 빌드: `docker build -t ocr-calendar-api .`
2. 실행: `docker run -d -p 8000:8000 ocr-calendar-api`

## ✨ 샘플 요청 및 응답 예시

### 1. 일정 추출 (Extract)
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@sample_image.png;type=image/png'
```

**응답 예시 (JSON)**:
```json
{
  "title": "2024년 2학기 데이터베이스 과제 안내",
  "course_name": "데이터베이스",
  "date": "2024-11-20",
  "time": "14:00",
  "deadline": "2024-11-20 23:59 까지",
  "location": "제1공학관 101호",
  "raw_text": "...",
  "parsing_status": "SUCCESS",
  "confidence": 0.95
}
```

### 2. 구글 캘린더 형태 변환 (Preview-Event)
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/preview-event' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "데이터베이스 특강",
  "date": "2024-11-20",
  "time": "14:00",
  "location": "제1공학관 101호"
}'
```

**응답 예시 (JSON)**:
```json
{
  "summary": "데이터베이스 특강",
  "location": "제1공학관 101호",
  "description": "OCR로 추출 및 등록된 자동 일정",
  "start": {
    "dateTime": "2024-11-20T14:00:00",
    "timeZone": "Asia/Seoul"
  },
  "end": {
    "dateTime": "2024-11-20T15:00:00",
    "timeZone": "Asia/Seoul"
  }
}
```
