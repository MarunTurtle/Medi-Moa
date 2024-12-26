# COGI Helper 프로그램 명세서

## 목차
- [COGI Helper 프로그램 명세서](#cogi-helper-프로그램-명세서)
  - [목차](#목차)
  - [1. 프로그램 개요](#1-프로그램-개요)
    - [1.1 목적](#11-목적)
    - [1.2 주요 기능](#12-주요-기능)
  - [2. 기능 명세](#2-기능-명세)
    - [2.1 게시물 수집 기능](#21-게시물-수집-기능)
    - [2.2 데이터 표시](#22-데이터-표시)
    - [2.3 사용자 인터페이스](#23-사용자-인터페이스)
  - [3. 기술 스택](#3-기술-스택)
    - [3.1 개발 환경](#31-개발-환경)
    - [3.2 대상 웹사이트](#32-대상-웹사이트)
  - [4. 구현 세부사항](#4-구현-세부사항)
    - [4.1 클래스 구조](#41-클래스-구조)
    - [4.1 프로그램 구조](#41-프로그램-구조)
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
1. 사이트 선택 영역
   - 3열 그리드 형태로 사이트 버튼 배치
   - 각 버튼은 사이트명 표시
   - 선택된 사이트는 시각적으로 구분되도록 강조

2. 검색 제어 영역
   - 날짜 입력 필드: 시작일과 종료일
   - 날짜 범위 선택 탭
     * 날짜 선택 (커스텀)
     * 오늘
     * 일주일
   - 검색 버튼

3. 결과 표시 영역
   - 4개 열로 구성된 데이터 테이블
     * 번호
     * 제목 (말줄임 처리)
     * 날짜
     * 링크 (클릭 가능한 버튼)
   - 검색 결과 수 표시
   - 결과 없을 경우 안내 메시지 표시

## 3. 기술 스택

### 3.1 개발 환경
- Python 3.x
- Flet (GUI 프레임워크)
- pandas (데이터 처리 및 날짜 검증)
- datetime (날짜 범위 계산)

### 3.2 대상 웹사이트
1. KOPS(환자안전보고학습시스템) (2개)
   - 공지사항: https://www.kops.or.kr/portal/board/kopsNotice/boardList.do
   - 정보제공지: https://www.kops.or.kr/portal/ifm/infoProvdStdrList.do

2. 대한병원협회 (1개)
   - 공지사항: https://www.kha.or.kr/impart/notice/list

3. 대한환자안전학회 (1개)
   - 공지사항: http://www.patientsafety.kr/index.php?hCode=BOARD&bo_idx=5

4. 한국의료질향상학회 (1개)
   - 공지사항: https://www.kosqua.net/

5. 대한간호협회 지역환자안전센터 (3개)
   - 공지: http://patientsafety.koreanurse.or.kr/announcement
   - 소식지: http://patientsafety.koreanurse.or.kr/news
   - 교육행사: http://patientsafety.koreanurse.or.kr/promotion

6. 대한병원협회교육센터 (1개)
   - 공지사항: https://khaedu.or.kr/board/cha_notice

7. 정신간호사회 (2개)
   - 공지사항: https://www.kpmhna.or.kr/sub5/5_1.php
   - 자료실: https://www.kpmhna.or.kr/sub6/6_1.php

8. 의료&복지 뉴스 (1개)
   - http://www.mediwelfare.com/news/articleList.html

9. 질병관리청 (2개)
   - 공지사항: https://www.kdca.go.kr/board/board.es?mid=a20504000000&bid=0014
   - 보도자료: https://www.kdca.go.kr/board/board.es?mid=a20501010000&bid=0015

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

### 4.1 프로그램 구조
1. 메인 애플리케이션
   - 윈도우 크기: 1000 x 800
   - 라이트 테마 모드
   - 자동 스크롤 지원

2. 핵심 기능
   - 날짜 유효성 검증
   - 날짜 범위 자동 계산 (오늘/일주일)
   - 동적 웹사이트 모듈 로딩
   - 검색 결과 실시간 표시

3. 오류 처리
   - 날짜 형식 검증
   - 스크래핑 실패 시 오류 메시지
   - 결과 없음 처리

## 5. 데이터 구조
1. 검색 결과 형식
   - 번호 (정수)
   - 제목 (문자열)
   - 날짜 (문자열, YYYY-MM-DD)
   - URL (문자열)

2. 사이트 정보
   - 사이트명과 스크래퍼 모듈 매핑
   - 총 14개 사이트 지원

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
