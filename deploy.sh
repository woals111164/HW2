#!/bin/bash

# 에러 발생 시 즉시 스크립트 중단
set -e

# 환경 변수 DOCKERHUB_USERNAME은 배포 환경이나 GitHub Actions에서 전달됩니다.
if [ -z "$DOCKERHUB_USERNAME" ]; then
  echo "Error: DOCKERHUB_USERNAME 환경 변수가 설정되지 않았습니다."
  exit 1
fi

IMAGE_NAME="$DOCKERHUB_USERNAME/hw2:latest"
CONTAINER_NAME="ocr-calendar-api"

echo "1. Docker Hub에서 최신 이미지 Pull: $IMAGE_NAME"
docker pull $IMAGE_NAME

echo "2. 기존 컨테이너가 실행 중이라면 중지"
# || true 덕분에 컨테이너가 없어도 스크립트가 실패(exit)하지 않고 tiếp tục chạy
docker stop $CONTAINER_NAME || true

echo "3. 기존 컨테이너가 존재한다면 삭제"
docker rm $CONTAINER_NAME || true

echo "4. 새 컨테이너를 -d 옵션으로 백그라운드 실행"
# 8000포트를 호스트 머신의 8000포트에 연결
docker run -d --name $CONTAINER_NAME -p 8000:8000 $IMAGE_NAME

echo "5. 앱이 시작될 때까지 5초 대기..."
sleep 5

echo "6. /health 엔드포인트로 정상 동작 확인"
# -f 옵션: HTTP 에러 발생 시 curl 명령어 실패 처리
curl -f http://localhost:8000/health

echo -e "\n=== 🚀 배포 성공적으로 완료! ==="
