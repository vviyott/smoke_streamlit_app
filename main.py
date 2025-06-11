# main.py
import streamlit as st
from components.tab_dash import seoul_smoking_rate_2022
from components.tab_map import smoking_zone_map
from components.tab_ai_news import news_chatbot
from components.tab_shopping_compare import shopping_compare

# ChromaDB 의존성 처리
try:
    from components.tab_ai_news import news_chatbot
    AI_NEWS_AVAILABLE = True
except ImportError as e:
    AI_NEWS_AVAILABLE = False
    print(f"AI News feature unavailable: {e}")

# 페이지 설정
st.set_page_config(page_title="Tobacco Data Hub", page_icon="🚬", layout = "wide")

# 전체 앱 스타일링
st.markdown("""
<style>
/* 헤더 영역 스타일링 */
.main-header {
    text-align: center;
    padding: 20px 0;
    margin-bottom: 30px;
    background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 10px;
    border: 1px solid #dee2e6;
}

.main-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 10px;
}

.main-subtitle {
    font-size: 1.1rem;
    color: #6c757d;
    font-weight: 400;
}

/* 선택된 탭 스타일 */
.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    border-bottom: 3px solid #555555 !important;
    color: #555555 !important;
    font-weight: bold;
}

/* 탭 호버 효과 */
.stTabs [data-baseweb="tab-list"] button:hover {
    color: #333333 !important;
    background-color: #f8f9fa !important;
}

/* 움직이는 강조 바 색상 탭 색상과 통일 */
[data-baseweb="tab-highlight"] {
    background-color: #555555 !important;
}

/* 전체 앱 패딩(상하여백) 조정 */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* 푸터 스타일 */
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f8f9fa;
    color: #6c757d;
    text-align: center;
    padding: 10px 0;
    font-size: 0.85rem;
    border-top: 1px solid #dee2e6;
    z-index: 999;
}
</style>
""", unsafe_allow_html=True)

# 메인 헤더
st.markdown("""
<div class="main-header">
    <div class="main-title">🚬 Tobacco Data Hub</div>
    <div class="main-subtitle">Comprehensive tobacco data analysis platform for Seoul</div>
</div>
""", unsafe_allow_html=True)

# 탭 생성 (ChromaDB 가용성에 따라 조건부)
if AI_NEWS_AVAILABLE:
    tabs = st.tabs([
        "📊 Smoking Data Statistics", 
        "🗺️ Seoul Smoking Zone",
        "📰 News Feed Chat",
        "🛍️ Shopping Price Compare"
    ])
else:
    tabs = st.tabs([
        "📊 Smoking Data Statistics", 
        "🗺️ Seoul Smoking Zone",
        "🛍️ Shopping Price Compare"
    ])

# 탭 내용
with tabs[0]:
    seoul_smoking_rate_2022()

with tabs[1]:
    smoking_zone_map()

if AI_NEWS_AVAILABLE:
    with tabs[2]:
        news_chatbot()
    
    with tabs[3]:
        shopping_compare()
else:
    with tabs[2]:
        shopping_compare()
    
    # AI 뉴스 준비 중 메시지 (별도 공간에 표시)
    st.info("📰 News Feed Chat 기능은 현재 업그레이드 중입니다. 곧 만나보실 수 있습니다!")

# 푸터
st.markdown("""
<div class="footer">
    💡 Tobacco Data Hub v1.0 | Built with Streamlit | © 2025
</div>
""", unsafe_allow_html=True)
