from PIL import Image
import io

class OCRService:
    def __init__(self):
        """
        초기화 시 필요한 모델 서빙 서버 주소, Google Cloud 인증 키 등을 로드합니다.
        (현재는 더미 모듈로 운영)
        """
        pass

    def extract_text(self, image_bytes: bytes) -> str:
        """
        주어진 이미지 바이트 데이터에서 텍스트를 추출합니다.
        실제 MLOps 파이프라인 연동 시 이 메서드를 Google Cloud Vision API 연동 코드나,
        내부적으로 띄운 Tesseract/TrOCR API 호출 코드 등으로 교체합니다.
        
        Args:
            image_bytes (bytes): 업로드된 이미지 파일의 바이트 스트림
            
        Returns:
            str: OCR로 추출된 텍스트. 
                 (테스트용 텍스트 반환)
        """
        # (과제 시연용) 입력 이미지를 검증하는 로직 흉내
        try:
            image = Image.open(io.BytesIO(image_bytes))
            # image.verify()
        except Exception as e:
            raise ValueError("유효하지 않은 이미지 형식입니다.") from e

        # [TODO: 실제 OCR 호출 로직 추가]
        # 임시로 시연용 더미 데이터 반환
        dummy_text = """
        2024년 2학기 데이터베이스 과제 안내
        날짜: 2024-11-20
        시간: 14:00
        장소: 제1공학관 101호
        과목명: 데이터베이스
        제출기한: 2024-11-20 23:59 까지
        """
        return dummy_text.strip()

# 싱글톤처럼 하나만 생성하여 서비스 통일
ocr_service_instance = OCRService()
