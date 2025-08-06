
import streamlit as st
import streamlit.components.v1 as components

# 방법 1: iframe 사용 (가장 안정적)
def seoul_smoking_rate_2022():
    # 페이지 레이아웃을 wide로 설정 (main.py에서 설정 필요)
    st.markdown("## 서울시민 흡연율 시각화📈")
    st.markdown("""
    2022년 서울시 자치구별 흡연율 데이터를 시각화한 자료입니다.  
    자치구별 흡연율 순위와 흡연 현황 지도, 성별 흡연율 통계를 함께 확인해보세요.
    """)
    
    # 전체 너비를 활용하여 표시
    components.html(
        """
        <style>
        .tableau-wide {
            width: 100vw;
            position: relative;
            left: 50%;
            right: 50%;
            margin-left: -50vw;
            margin-right: -50vw;
            max-width: none;
        }
        </style>
        
        <div class="tableau-wide">
            <iframe src="https://public.tableau.com/views/SmokingrateinSeoul2022/1?:language=ko-KR&:display_count=n&:origin=viz_share_link&:embed=y&:showVizHome=no&:toolbar=top&:device=desktop" 
                    width="100%" 
                    height="900" 
                    frameborder="0"
                    allowtransparency="true"
                    allowfullscreen="true"
                    style="border: none;">
            </iframe>
        </div>
        """,
        height=920
    )
    st.caption("출처: [서울 열린데이터 광장](https://data.seoul.go.kr/dataList/10668/S/2/datasetView.do#)")
