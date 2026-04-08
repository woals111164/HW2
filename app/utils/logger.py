import logging
import sys

def setup_logger(name: str = "ocr_app"):
    """
    MLOps 환경에서 일관된 로깅을 위해 포맷 및 핸들러를 정의합니다.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        # 콘솔 출력을 위한 포맷터 추가
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        
    return logger

logger = setup_logger()
