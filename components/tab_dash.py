
import streamlit as st
import streamlit.components.v1 as components

# 방법 1: iframe 사용 (가장 안정적)
def seoul_smoking_rate_2022():
    st.markdown("## 서울시민 흡연율 시각화📈")
    st.markdown("""
    2022년 서울시 자치구별 흡연율 데이터를 시각화한 자료입니다.  
    자치구별 흡연율 순위와 흡연 현황 지도, 성별 흡연율 통계를 함께 확인해보세요.
    """)
    
    # 데스크톱 레이아웃 강제 + 고정 크기
    tableau_url = "https://public.tableau.com/views/SmokingrateinSeoul2022/1?:language=ko-KR&:display_count=n&:origin=viz_share_link&:embed=y&:showVizHome=no&:toolbar=top&:device=desktop&:render=true"
    
    components.html(
        f"""
        <div style="width: 100%; display: flex; justify-content: center; align-items: center; background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
            <iframe src="{tableau_url}" 
                    width="1400" 
                    height="1200" 
                    frameborder="0"
                    allowtransparency="true"
                    allowfullscreen="true"
                    style="border: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 8px; background: white;">
            </iframe>
        </div>
        """,
        height=850
    )
    st.caption("출처: [서울 열린데이터 광장](https://data.seoul.go.kr/dataList/10668/S/2/datasetView.do#)")

