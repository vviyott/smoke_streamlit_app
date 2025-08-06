
import streamlit as st
import streamlit.components.v1 as components

# 방법 1: iframe 사용 (가장 안정적)
def seoul_smoking_rate_2022():
    st.markdown("## 서울시민 흡연율 시각화📈")
    st.markdown("""
    2022년 서울시 자치구별 흡연율 데이터를 시각화한 자료입니다.  
    자치구별 흡연율 순위와 흡연 현황 지도, 성별 흡연율 통계를 함께 확인해보세요.
    """)
    
    # Streamlit의 columns를 사용해서 중앙 정렬
    col1, col2, col3 = st.columns([1, 8, 1])
    
    with col2:
        # 간단한 iframe 방식
        tableau_url = "https://public.tableau.com/views/SmokingrateinSeoul2022/1"
        
        st.components.v1.iframe(
            src=f"{tableau_url}?:language=ko-KR&:display_count=n&:origin=viz_share_link&:embed=y&:showVizHome=no",
            width=None,  # 자동 조정
            height=1200,
            scrolling=False
        )
    
    st.caption("출처: [서울 열린데이터 광장](https://data.seoul.go.kr/dataList/10668/S/2/datasetView.do#)")
