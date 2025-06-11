# 🚬 Smoke Streamlit App

서울시 흡연 현황과 민원 데이터를 시각화하고, 담배 관련 뉴스를 분석하는 AI 챗봇 시스템입니다.  
Streamlit 기반의 웹 앱으로 구성되어 있으며, 사용자는 다양한 시각 자료와 인터랙티브 기능을 통해 정보를 확인할 수 있습니다.

## 📌 주요 기능

- 📊 서울시 자치구별 흡연율 시각화 (Tableau 연동)
- 🗺️ 흡연구역 위치 지도 표시
- 📰 중앙일보 기사 기반 AI 뉴스 챗봇
- 🛒 네이버 쇼핑 API 기반 가격 비교

## 🔗 체험하기

- [실시간 앱 실행 (Streamlit)](https://<your-app-name>.streamlit.app)
- [코드 보기 (GitHub)](https://github.com/vviyot/smoke_streamlit_app)

## 📁 프로젝트 구조
smoke_streamlit_app/
├── main.py			← Streamlit 실행 파일
├── components/
│   ├── __init__.py		                        ← (비워두거나 공통 유틸 함수 작성 가능)
│   ├── tab_dash.py		                        ← 2022년 서울시민 흡연율 시각화 (Tableau)
│   ├── tab_map.py		                        ← 흡연구역 위치 지도 시각화
│   ├── tab_ai_news.py	                        ← 담배 뉴스 기반 AI 챗봇
│   └── tab_shopping_compare.py	← 네이버 쇼핑 가격비교
├── utils/
│   └── naver_api_shop.py      ← 네이버 API 호출 함수
├── data/
│   ├── smoking_areas.csv				   ← 지도용 위치 데이터 (자치구별 흡연구역 주소와 위도, 경도 데이터)
│   ├── chroma_db/컬렉션 'ciga_articles'	   ← 벡터DB 저장 디렉토리 (중앙일보 기사 기반)
│   └── naver_shopping_액상형 전자담배_20250606_183943.csv
└── requirements.txt      ← 패키지 목록 (예정)
