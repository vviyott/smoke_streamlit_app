# components/tab_dash.py

import streamlit as st
import streamlit.components.v1 as components

def seoul_smoking_rate_2022():
    st.markdown("## 서울시민 흡연율 시각화📈")
    st.markdown("""
    2022년 서울시 자치구별 흡연율 데이터를 시각화한 자료입니다.  
    자치구별 흡연율 순위와 흡연 현황 지도, 성별 흡연율 통계를 함께 확인해보세요.
    """)

    # 2행: 두 개의 태블로 시각화 (좌: 2022, 우: 2023)
    viz_col1, viz_col2 = st.columns(2)

    with viz_col1:
        components.html(
            """
            <div style="width: 100%; overflow-x: auto; overflow-y: hidden; border: 1px solid #e1e5e9; border-radius: 8px; background: white;">
                <div class='tableauPlaceholder' id='viz1754442554050' style='position: relative; min-width: 1200px;'>
                    <noscript>
                        <a href='#'>
                            <img alt='대시보드 1' src='https://public.tableau.com/static/images/Sm/SmokingrateinSeoul2022/1/1_rss.png' style='border: none' />
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
            </div>

            <script type='text/javascript'>
                var divElement = document.getElementById('viz1754442554050');
                var vizElement = divElement.getElementsByTagName('object')[0];
                vizElement.style.width = '1200px';
                vizElement.style.height = '900px';
                var scriptElement = document.createElement('script');
                scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
                vizElement.parentNode.insertBefore(scriptElement, vizElement);
            </script>
            """,
            width=1250,
            height=950,
            scrolling=False
        )
        st.caption("출처: [서울 열린데이터 광장](https://data.seoul.go.kr/dataList/10668/S/2/datasetView.do#)")

    with viz_col2:
        components.html(
            """
            <div style="width: 100%; overflow-x: auto; overflow-y: hidden; border: 1px solid #e1e5e9; border-radius: 8px; background: white;">
                <div class='tableauPlaceholder' id='viz2023' style='position: relative; min-width: 1200px;'>
                    <noscript>
                        <a href='#'>
                            <img alt='대시보드 2' src='https://public.tableau.com/static/images/Sm/SmokingrateinSeoul2023/1/1_rss.png' style='border: none' />
                        </a>
                    </noscript>
                    <object class='tableauViz' style='display:none;'>
                        <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
                        <param name='embed_code_version' value='3' />
                        <param name='site_root' value='' />
                        <param name='name' value='SmokingrateinSeoul2023/1' />
                        <param name='tabs' value='no' />
                        <param name='toolbar' value='yes' />
                        <param name='static_image' value='https://public.tableau.com/static/images/Sm/SmokingrateinSeoul2023/1/1.png' />
                        <param name='animate_transition' value='yes' />
                        <param name='display_static_image' value='yes' />
                        <param name='display_spinner' value='yes' />
                        <param name='display_overlay' value='yes' />
                        <param name='display_count' value='yes' />
                        <param name='language' value='ko-KR' />
                    </object>
                </div>
            </div>

            <script type='text/javascript'>
                var divElement = document.getElementById('viz2023');
                var vizElement = divElement.getElementsByTagName('object')[0];
                vizElement.style.width = '1200px';
                vizElement.style.height = '900px';
                var scriptElement = document.createElement('script');
                scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
                vizElement.parentNode.insertBefore(scriptElement, vizElement);
            </script>
            """,
            width=1250,
            height=950,
            scrolling=False
        )
        st.caption("출처: Tableau Public · Smoking rate in Seoul 2023")
