import re
from typing import Dict, Any

class ParserService:
    @staticmethod
    def parse_extracted_text(raw_text: str) -> Dict[str, Any]:
        """
        OCR로 추출된 raw 텍스트에서 정규식을 이용해 일정 정보를 파싱합니다.
        
        Args:
            raw_text (str): 메타데이터를 추출할 원본 텍스트
            
        Returns:
            dict: 추출된 제목, 과목, 날짜, 시간, 장소, 마감일 정보 맵(map)
        """
        parsed_data = {
            "title": None,
            "course_name": None,
            "date": None,
            "time": None,
            "deadline": None,
            "location": None
        }
        
        # 간단한 정규식 패턴들 (과제용)
        # 예: "날짜: 2024-11-20" 또는 "일시: 24.11.20"
        date_pattern = re.compile(r"(?:날짜|일시|Date)[\s:]*([0-9]{4}[-/.][0-9]{2}[-/.][0-9]{2})")
        time_pattern = re.compile(r"(?:시간|Time)[\s:]*([0-9]{2}:[0-9]{2})")
        course_pattern = re.compile(r"(?:과목|과목명|Course)[\s:]*([^\n]+)")
        loc_pattern = re.compile(r"(?:장소|위치|Location)[\s:]*([^\n]+)")
        deadline_pattern = re.compile(r"(?:기한|마감|제출기한)[\s:]*([^\n]+)")
        
        # 제목의 경우 보통 첫 줄이라고 가정 (휴리스틱)
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
        if lines:
            parsed_data["title"] = lines[0]
            
        m_date = date_pattern.search(raw_text)
        if m_date:
            parsed_data["date"] = m_date.group(1).strip()
            
        m_time = time_pattern.search(raw_text)
        if m_time:
            parsed_data["time"] = m_time.group(1).strip()
            
        m_course = course_pattern.search(raw_text)
        if m_course:
            parsed_data["course_name"] = m_course.group(1).strip()
            
        m_loc = loc_pattern.search(raw_text)
        if m_loc:
            parsed_data["location"] = m_loc.group(1).strip()
            
        m_deadline = deadline_pattern.search(raw_text)
        if m_deadline:
            parsed_data["deadline"] = m_deadline.group(1).strip()
            
        return parsed_data
