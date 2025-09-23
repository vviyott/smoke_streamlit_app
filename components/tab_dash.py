# components/tab_dash.py (v2)

import streamlit as st
import streamlit.components.v1 as components
import uuid

def embed_tableau_auto(
    url: str,
    ratio: str = "16:9",      # W:H (가로:세로 비율)
    vh_portion: float = 0.85, # 화면 높이의 몇 %까지 사용할지 (0~1)
    min_height: int = 520,    # 너무 낮아지지 않게 하한
    max_height: int = 820,    # 과도하게 길어지지 않게 상한 (Streamlit 예약 높이도 이 값으로)
    toolbar: str = "yes",     # "yes" | "no" | "top" | "bottom"
):
    # 비율 계산 (H/W)
    w, h = map(float, ratio.split(":"))
    r = h / w

    sep = "&" if "?" in url else "?"
    final = f"{url}{sep}:showVizHome=no&:embed=y&:toolbar={toolbar}"
    box_id = f"tbl-{uuid.uuid4().hex}"

    html = f"""
    <div id="{box_id}" style="position:relative;width:100%;
         border:1px solid #e1e5e9;border-radius:8px;background:#fff;overflow:hidden;">
      <iframe id="{box_id}-iframe" src="{final}" style="width:100%;height:100%;border:0;" allowfullscreen></iframe>
    </div>
    <script>
      (function(){{
        const box = document.getElementById("{box_id}");
        const frame = document.getElementById("{box_id}-iframe");
        const RATIO = {r};                 // H/W
        const VH_PORTION = {vh_portion};   // 화면 높이 비율 (0~1)

        function resize() {{
          const w = box.clientWidth;                          // 현재 컬럼 실제 너비
          const hByWidth = Math.round(w * RATIO);             // 비율 기반 높이
          const hByViewport = Math.round(window.innerHeight * VH_PORTION); // 화면 높이 기반
          let target = Math.min(hByWidth, hByViewport);       // 둘 중 작은 값 사용
          target = Math.max({min_height}, Math.min({max_height}, target));  // 하한/상한
          box.style.height = target + "px";
          frame.style.height = target + "px";
        }}
        window.addEventListener("load", resize);
        window.addEventListener("resize", resize);
        setTimeout(resize, 200);  // 초기 렌더 지연 대응
      }})();
    </script>
    """
    # Streamlit이 예약하는 바깥 높이(너무 크면 빈 공간 생김) → max_height로 맞춰 최소화
    components.html(html, height=max_height, scrolling=False)

def seoul_smoking_rate_2022():
    st.markdown("## 서울시민 흡연율 시각화📈")
    st.markdown(
        """
        2022년 서울시 자치구별 흡연율 데이터를 시각화한 자료입니다.  
        자치구별 흡연율 순위와 흡연 현황 지도, 성별 흡연율 통계를 함께 확인해보세요.
        """
    )
    
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<h3 style='text-align: left;'># 2022년</h3>", unsafe_allow_html=True)
        st.caption("데이터 출처: [서울 열린데이터 광장](https://data.seoul.go.kr/dataList/10668/S/2/datasetView.do#)")
        url_2022 = "https://public.tableau.com/views/SmokingrateinSeoul2022/1"
        embed_tableau_auto(
            url=url_2022,
            ratio="4:3",          # 두 컬럼(폭이 줄어듦)에서는 4:3이 시야 확보에 유리
            vh_portion=0.85,      # 화면 높이의 최대 85%까지 사용
            min_height=540,
            max_height=820,       # Streamlit 예약 높이도 동일하게
            toolbar="yes",
        )
        

    with c2:
    
        url_2023 = "https://public.tableau.com/views/SmokingrateinSeoul2023/1"
        embed_tableau_auto(
            url=url_2023,
            ratio="4:3",
            vh_portion=0.85,
            min_height=540,
            max_height=820,
            toolbar="yes",
        )
