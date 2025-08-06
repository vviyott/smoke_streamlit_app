# components/tab_dash.py (v0)
import streamlit as st
import streamlit.components.v1 as components

def seoul_smoking_rate_2022():
    # 📍 제목 + 설명
    st.markdown("## 서울시민 흡연율 시각화📈")
    st.markdown("""
    2022년 서울시 자치구별 흡연율 데이터를 시각화한 자료입니다.  
    자치구별 흡연율 순위와 흡연 현황 지도, 성별 흡연율 통계를 함께 확인해보세요.
    """)
    # st.markdown("---")

    components.html(
        """
        <div id='vizSmoking' class='tableauPlaceholder' style='width:100%;'>
          <noscript>
            <a href='#'>
              <img alt='흡연율 시각화'
                  src='https://public.tableau.com/static/images/Sm/SmokingrateinSeoul2022/1/1.png'
                  style='border: none' />
            </a>
          </noscript>

          <object class='tableauViz' style='display:none;'>
            <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F'/>
            <param name='embed_code_version' value='3'/>
            <param name='site_root' value=''/>
            <param name='name' value='SmokingrateinSeoul2022/1'/>
            <param name='tabs' value='no'/>
            <param name='toolbar' value='yes'/>
            <param name='language' value='ko-KR'/>
          </object>
        </div>

        <script src='https://public.tableau.com/javascripts/api/viz_v1.js'></script>
        <script>
          const div = document.getElementById('vizSmoking');
          const viz = div.getElementsByTagName('object')[0];
          viz.style.width = '100%';
          viz.style.height = (div.offsetWidth * 1.6) + 'px';
          window.addEventListener('resize', () => {
          viz.style.height = (div.offsetWidth * 1.4) + 'px';
          });
        </script>

        """,
        height=900,  # 첫 로딩 때 공간 확보용 (JS가 재조정하긴 함)
        scrolling=False
    )

    st.caption("출처: [서울 열린데이터 광장](https://data.seoul.go.kr/dataList/10668/S/2/datasetView.do#)")
