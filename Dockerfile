# Python 3.11 slim 이미지를 베이스로 사용합니다. (가볍고 빠른 배포를 위함)
FROM python:3.11-slim

# 도커 컨테이너 내 작업 디렉토리를 /app으로 설정합니다.
WORKDIR /app

# 파이썬 출력 버퍼링을 비활성화하여 로그를 즉시 볼 수 있게 합니다.
ENV PYTHONUNBUFFERED=1

# (선택) OCR에 필요한 시스템 패키지가 있다면 주석을 해제하고 추가하세요. (예: tesseract, opencv 의존성 등)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     tesseract-ocr \
#     libgl1-mesa-glx \
#     && rm -rf /var/lib/apt/lists/*

# requirements.txt를 먼저 복사합니다. (Docker 레이어 캐시를 활용하여 빌드 속도 향상)
COPY requirements.txt .

# 파일에 명시된 파이썬 의존성 패키지들을 설치합니다.
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 애플리케이션 코드를 /app 디렉토리로 복사합니다.
COPY . .

# FastAPI 서버가 사용할 8000 포트를 노출합니다.
EXPOSE 8000

# 컨테이너 실행 시 uvicorn을 사용하여 서버를 시작합니다.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
