
import streamlit as st
import streamlit.components.v1 as components

# 방법 1: iframe 사용 (가장 안정적)
def seoul_smoking_rate_2022():
    st.markdown("## 서울시민 흡연율 시각화📈")
    st.markdown("""
    2022년 서울시 자치구별 흡연율 데이터를 시각화한 자료입니다.  
    자치구별 흡연율 순위와 흡연 현황 지도, 성별 흡연율 통계를 함께 확인해보세요.
    """)
    
    components.html(
        """
        <div class='tableauPlaceholder' id='viz1754439309658' style='position: relative; width: 100%; margin: 0 auto;'>
          <noscript>
            <a href='#'>
              <img alt='대시보드 1 '
                   src='https://public.tableau.com/static/images/Sm/SmokingrateinSeoul2022/1/1_rss.png'
                   style='border: none; width: 100%; height: auto;' />
            </a>
          </noscript>
          <object class='tableauViz' style='display:none; width: 100%; height: 1200px;'>
            <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
            <param name='embed_code_version' value='3' />
            <param name='site_root' value='' />
            <param name='name' value='SmokingrateinSeoul2022/1' />
            <param name='tabs' value='no' />
            <param name='toolbar' value='yes' />
            <param name='static_image' value='https://public.tableau.com/static/images/Sm/SmokingrateinSeoul2022/1/1.png' />
            <param name='animate_transition' value='yes' />
            <param name='display_static_image' value='yes' />
            <param name='display_spinner' value='yes' />
            <param name='display_overlay' value='yes' />
            <param name='display_count' value='yes' />
            <param name='language' value='ko-KR' />
          </object>
        </div>
        <script type='text/javascript'>
          console.log('Script started');
          
          function initTableau() {
            var divElement = document.getElementById('viz1754439309658');
            if (!divElement) {
              console.log('Div element not found');
              return;
            }
            
            var vizElement = divElement.getElementsByTagName('object')[0];
            if (!vizElement) {
              console.log('Viz element not found');
              return;
            }
            
            console.log('Container width:', divElement.offsetWidth);
            
            // 크기 설정
            vizElement.style.width = '100%';
            vizElement.style.height = '1200px';
            vizElement.style.display = 'block';
            
            console.log('Size set, loading script');
            
            // Tableau API 스크립트 로드
            if (!document.querySelector('script[src*="viz_v1.js"]')) {
              var scriptElement = document.createElement('script');
              scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
              scriptElement.onload = function() {
                console.log('Tableau script loaded');
              };
              scriptElement.onerror = function() {
                console.log('Failed to load Tableau script');
              };
              vizElement.parentNode.insertBefore(scriptElement, vizElement);
            }
          }
          
          // DOM이 준비되면 실행
          if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initTableau);
          } else {
            initTableau();
          }
          
          // 추가 보험으로 setTimeout도 사용
          setTimeout(initTableau, 1000);
        </script>
        """,
        height=1220
    )
    st.caption("출처: [서울 열린데이터 광장](https://data.seoul.go.kr/dataList/10668/S/2/datasetView.do#)")
