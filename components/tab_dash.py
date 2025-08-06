import streamlit as st
import streamlit.components.v1 as components

def seoul_smoking_rate_2022():
    # 📍 제목 + 설명
    st.markdown("## 서울시민 흡연율 시각화📈")
    st.markdown("""
    2022년 서울시 자치구별 흡연율 데이터를 시각화한 자료입니다.  
    자치구별 흡연율 순위와 흡연 현황 지도, 성별 흡연율 통계를 함께 확인해보세요.
    """)

    # ✅ Tableau Public iframe 임베딩
    components.html(
        """
        <iframe 
            src="https://public.tableau.com/views/SmokingrateinSeoul2022/1?:language=ko-KR&:display_count=y&:origin=viz_share_link"
            width="1000" 
            height="700" 
            style="border:none;" 
            frameborder="0" 
            allowfullscreen>
        </iframe>
        """,
        height=720  # Streamlit 내부에서 공간 확보용
    )

    st.caption("출처: [서울 열린데이터 광장](https://data.seoul.go.kr/dataList/10668/S/2/datasetView.do#)")
