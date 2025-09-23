# components/tab_dash.py

import streamlit as st
import streamlit.components.v1 as components

def _embed_tableau_responsive(
    url: str,
    ratio: str = "16:9",     # "4:3", "1:1" 등 필요에 맞게
    min_height: int = 360,   # 너무 낮아지지 않도록 안전장치
    max_height: int = 1200,  # 데스크톱에서 과도하게 길어지지 않도록 상한
    scrolling: bool = False,
    toolbar: str = "yes",    # "yes" | "no" | "top" | "bottom"
):
    """
    반응형 Tableau 임베드 (iframe + aspect-ratio padding box)
    - 컬럼 너비(=화면 너비 변화)에 따라 높이가 자동으로 변합니다.
    - url에는 Tableau Public 뷰 링크를 넣고, 아래에서 embed 옵션을 붙여 사용합니다.
    """
    w, h = map(float, ratio.split(":"))
    padding_top = (h / w) * 100  # ex) 9/16*100 = 56.25%

    # URL에 깔끔한 임베드 옵션 추가
    join_char = "&" if "?" in url else "?"
    final_url = (
        f"{url}{join_char}:showVizHome=no&:embed=y&:toolbar={toolbar}"
    )

    html = f"""
    <div style="position:relative;width:100%;border:1px solid #e1e5e9;border-radius:8px;background:white;overflow:hidden;">
      <!-- 비율 박스 -->
      <div style="position:relative;width:100%;padding-top:{padding_top}%;
                  min-height:{min_height}px;max-height:{max_height}px;">
        <iframe
          src="{final_url}"
          style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"
          frameborder="0"
          allowfullscreen
          scrolling={"yes" if scrolling else "no"}>
        </iframe>
      </div>
    </div>
    """
    # components.html의 height는 컨테이너 최대 높이로 맞춰 잘리지 않게 함
    components.html(html, height=max_height, scrolling=scrolling)


def seoul_smoking_rate_2022():
    st.markdown("## 서울시민 흡연율 시각화📈")
    st.markdown(
        """
        2022년 서울시 자치구별 흡연율 데이터를 시각화한 자료입니다.  
        자치구별 흡연율 순위와 흡연 현황 지도, 성별 흡연율 통계를 함께 확인해보세요.
        """
    )

    # 2열: 화면 너비를 1:1로 나눔 → 각 차트가 항상 화면의 절반 너비를 사용 (반응형)
    viz_col1, viz_col2 = st.columns(2)

    with viz_col1:
        # Tableau Public 뷰 링크 (시트 경로만 바꿔도 동일 동작)
        url_2022 = "https://public.tableau.com/views/SmokingrateinSeoul2022/1"
        _embed_tableau_responsive(
            url=url_2022,
            ratio="16:9",        # 필요 시 "4:3"으로 바꾸면 세로가 조금 더 확보됨
            min_height=420,
            max_height=1100,
            toolbar="yes",       # "no"로 숨길 수도 있음
            scrolling=False,
        )
        st.caption("출처: [서울 열린데이터 광장](https://data.seoul.go.kr/dataList/10668/S/2/datasetView.do#)")

    with viz_col2:
        url_2023 = "https://public.tableau.com/views/SmokingrateinSeoul2023/1"
        _embed_tableau_responsive(
            url=url_2023,
            ratio="16:9",
            min_height=420,
            max_height=1100,
            toolbar="yes",
            scrolling=False,
        )
        st.caption("출처: Tableau Public · Smoking rate in Seoul 2023")
