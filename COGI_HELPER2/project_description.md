# COGI Helper 프로그램 명세서

## 목차
- [1. 프로그램 개요](#1-프로그램-개요)
- [2. 기능 명세](#2-기능-명세)
- [3. 기술 스택](#3-기술-스택)
- [4. 구현 세부사항](#4-구현-세부사항)
- [5. 데이터 구조](#5-데이터-구조)
- [6. 오류 처리](#6-오류-처리)
- [7. 성능 최적화](#7-성능-최적화)
- [8. 향후 계획](#8-향후-계획)

## 1. 프로그램 개요

### 1.1 목적
의료/병원 관련 주요 웹사이트들의 게시물을 자동으로 수집하여 모니터링하는 프로그램 개발

### 1.2 주요 기능
- 다중 사이트 게시물 수집
- 기간별 조회 기능
- 통합 모니터링 인터페이스

## 2. 기능 명세

### 2.1 게시물 수집 기능
- 일일 수집 (당일 게시물)
- 주간 수집 (최근 7일)
- 월간 수집 (한 달 기준)
- 사용자 지정 기간 수집

### 2.2 데이터 표시
- 게시물 제목
- 게시 날짜
- 원문 링크
- 게시물 분류

### 2.3 사용자 인터페이스
```python
UI_COMPONENTS = {
    "navigation": {
        "type": "NavigationRail",
        "items": ["사이트별 탭"]
    },
    "main_content": {
        "type": "Column",
        "components": [
            "날짜 선택기",
            "검색 버튼",
            "결과 목록"
        ]
    },
    "status_bar": {
        "type": "AppBar",
        "info": ["상태 메시지", "진행률"]
    }
}
```

## 3. 기술 스택

### 3.1 개발 환경
- Python 3.x
- Flet (GUI 프레임워크)
- requests (웹 요청)
- BeautifulSoup4 (HTML 파싱)

### 3.2 대상 웹사이트
```python
WEBSITES = {
    "KOPS": {
        "공지사항": "https://www.kops.or.kr/portal/board/kopsNotice/boardList.do",
        "정보제공지": "https://www.kops.or.kr/portal/ifm/infoProvdStdrList.do"
    },
    "대한병원협회": {
        "공지사항": "https://www.kha.or.kr/impart/notice/list"
    },
    # ... 기타 사이트들
}
```

## 4. 구현 세부사항

### 4.1 클래스 구조
```python
class WebsiteScraper:
    """기본 스크래퍼 클래스"""
    def __init__(self, base_url, site_config)
    def extract_posts(self, start_date, end_date)
    def parse_date(self, date_string)

class SiteSpecificScraper(WebsiteScraper):
    """사이트별 특화 스크래퍼"""
    def parse_page(self, html_content)
    def get_next_page_url(self, current_page)
```

## 5. 데이터 구조
```python
Post = {
    'title': str,      # 게시물 제목
    'date': datetime,  # 게시 날짜
    'link': str,      # 원문 링크
    'category': str,  # 게시물 분류
    'site': str       # 출처 사이트
}
```

## 6. 오류 처리
1. 네트워크 오류
2. 파싱 오류
3. 날짜 형식 오류
4. 페이지 접근 제한

## 7. 성능 최적화
1. 동시 요청 제한
2. 요청 간 시간 간격
3. 타임아웃 설정
4. 메모리 사용량 관리

## 8. 향후 계획
- [ ] 데이터 저장 기능
- [ ] 키워드 필터링
- [ ] 알림 기능
- [ ] 엑셀 출력 기능
- [ ] 자동 실행 스케줄링
