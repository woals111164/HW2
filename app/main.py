from fastapi import FastAPI
from app.api.routes import router
from app.utils.logger import logger

app = FastAPI(
    title="OCR Event Extractor API",
    description="이미지에서 핵심 일정 정보를 추출하여 Google Calendar에 등록할 수 있도록 돕는 서비스",
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    logger.info("OCR Event Extractor API Server is starting up.")

@app.get("/")
def read_root():
    return {"message": "Welcome to OCR Event Extractor API. Visit /docs for Swagger UI."}

@app.get("/health")
def health_check():
    return {"status": "ok"}