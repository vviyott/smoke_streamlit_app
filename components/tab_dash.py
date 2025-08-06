import streamlit as st
import streamlit.components.v1 as components

def seoul_smoking_rate_2022():
    st.markdown("## 서울시민 흡연율 시각화📈")
    st.markdown("""
    2022년 서울시 자치구별 흡연율 데이터를 시각화한 자료입니다.  
    자치구별 흡연율 순위와 흡연 현황 지도, 성별 흡연율 통계를 함께 확인해보세요.
    """)
    
    # Tableau 공식 내장 코드 사용 + 반응형 개선
    components.html(
        """
        <div class='tableauPlaceholder' id='viz1754442554050' style='position: relative; width: 100%;'>
            <noscript>
                <a href='#'>
                    <img alt='대시보드 1' 
                         src='https://public.tableau.com/static/images/Sm/SmokingrateinSeoul2022/1/1_rss.png' 
                         style='border: none' />
                </a>
            </noscript>
            <object class='tableauViz' style='display:none;'>
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
            function initTableauViz() {
                var divElement = document.getElementById('viz1754442554050');
                if (!divElement) {
                    console.log('Tableau div not found');
                    return;
                }
                
                var vizElement = divElement.getElementsByTagName('object')[0];
                if (!vizElement) {
                    console.log('Tableau object not found');
                    return;
                }
                
                // 반응형 크기 조정 로직 개선
                var containerWidth = divElement.offsetWidth;
                console.log('Container width:', containerWidth);
                
                if (containerWidth > 1200) {
                    // 큰 화면: 고정 크기로 가로 레이아웃 보장
                    vizElement.style.width = '1400px';
                    vizElement.style.height = '900px';
                } else if (containerWidth > 800) {
                    // 중간 화면: 적당한 고정 크기
                    vizElement.style.width = '1200px';
                    vizElement.style.height = '800px';
                } else if (containerWidth > 500) {
                    // 작은 화면: 여전히 데스크톱 레이아웃 유지
                    vizElement.style.width = '1000px';
                    vizElement.style.height = '700px';
                } else {
                    // 매우 작은 화면: 최소 크기
                    vizElement.style.width = '800px';
                    vizElement.style.height = '600px';
                }
                
                // Tableau API 스크립트 로드
                if (!document.querySelector('script[src*="viz_v1.js"]')) {
                    var scriptElement = document.createElement('script');
                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
                    scriptElement.onload = function() {
                        console.log('Tableau API loaded successfully');
                    };
                    scriptElement.onerror = function() {
                        console.log('Failed to load Tableau API');
                    };
                    vizElement.parentNode.insertBefore(scriptElement, vizElement);
                }
            }
            
            // 초기화 및 리사이즈 이벤트
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initTableauViz);
            } else {
                initTableauViz();
            }
            
            window.addEventListener('resize', initTableauViz);
            
            // 보험용 지연 실행
            setTimeout(initTableauViz, 1000);
        </script>
        """,
        height=950,  # Streamlit 컨테이너 높이
        scrolling=False
    )
    
    st.caption("출처: [서울 열린데이터 광장](https://data.seoul.go.kr/dataList/10668/S/2/datasetView.do#)")
