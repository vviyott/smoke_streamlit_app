
import streamlit as st
import streamlit.components.v1 as components

# 방법 1: iframe 사용 (가장 안정적)
def seoul_smoking_rate_2022():
    st.markdown("## 서울시민 흡연율 시각화📈")
    st.markdown("""
    2022년 서울시 자치구별 흡연율 데이터를 시각화한 자료입니다.  
    자치구별 흡연율 순위와 흡연 현황 지도, 성별 흡연율 통계를 함께 확인해보세요.
    """)
    
    # 정적 이미지 표시
    st.image(
        "https://public.tableau.com/static/images/Sm/SmokingrateinSeoul2022/1/1.png",
        caption="서울시 2022년 흡연율 데이터 시각화",
        use_column_width=True
    )
    
    # 인터랙티브 버전 링크
    st.markdown("""
    **📊 [인터랙티브 버전 보기](https://public.tableau.com/views/SmokingrateinSeoul2022/1?:language=ko-KR&:display_count=n&:origin=viz_share_link)**
    
    *위 링크를 클릭하면 Tableau Public에서 전체 대시보드를 인터랙티브하게 이용할 수 있습니다.*
    """)
    
    st.caption("출처: [서울 열린데이터 광장](https://data.seoul.go.kr/dataList/10668/S/2/datasetView.do#)")
