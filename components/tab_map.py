# components/tab_map.py
import os
import streamlit as st
import pandas as pd
import pydeck as pdk

mapbox_token = st.secrets["MAPBOX_API_KEY"]  # 또는 os.environ.get("MAPBOX_API_KEY")
pdk.settings.mapbox_api_key = mapbox_token

def smoking_zone_map():
    # 제목 + 설명
    st.markdown("## 서울시 흡연구역 지도🗺️")
    st.markdown("""
    서울시 각 자치구별로 설치된 공공 흡연구역 위치를 지도에 시각화한 자료입니다.  
    선택한 자치구를 기준으로 흡연구역의 분포를 확인할 수 있으며, 총 설치 수 또한 함께 표시됩니다.
    """)
    st.markdown("""
    본 서비스는 정보의 **정확성**이나 **최신성**은 완벽히 **보장되지 않으며**, 실제와 다를 수 있습니다.
    현장 상황에 따라 흡연이 제한될 수 있으므로, 이용 전 참고하시기 바랍니다.
    """)

    # 데이터 로드
    data = pd.read_csv('data/smoking_areas.csv', encoding='cp949')
    data = data.rename(columns={'자치구명': '자치구', '시설구분': '장소', '위도': 'latitude', '경도': 'longitude'})
    data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce')
    data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')

    # 본문 영역에 selectbox 넣기
    districts = ['전체 보기'] + sorted(data['자치구'].dropna().unique().tolist())
    selected_district = st.selectbox("자치구를 선택하세요", districts)

    # 색상 강조 컬럼 추가
    if selected_district == "전체 보기":
        # 모두 빨간색
        data['color'] = [[255, 0, 0, 160]] * len(data)
    else:
        # 선택된 자치구는 파랑, 나머지는 회색
        data['color'] = data['자치구'].apply(
            lambda gu: [0, 102, 255, 200] if gu == selected_district else [140, 140, 140, 120])

    # 필터링 이후에도 color 컬럼 포함
    filtered_data = data if selected_district == '전체 보기' else data[data['자치구'] == selected_district]

    # 흡연구역 수 표시
    num_zones = len(filtered_data)
    if selected_district == "전체 보기":
        st.markdown(f"#### 서울시 전체 흡연구역 수: **{num_zones}곳**")
    else:
        st.markdown(f"#### **{selected_district}**의 흡연구역 수: **{num_zones}곳**")

    # 지도 중심 좌표 계산
    if selected_district == "전체 보기":
        center_lat = data['latitude'].mean()
        center_lon = data['longitude'].mean()
    else:
        center_lat = data[data['자치구'] == selected_district]['latitude'].mean()
        center_lon = data[data['자치구'] == selected_district]['longitude'].mean()

    # 지도 출력
    if not data.empty:
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/streets-v11',
            initial_view_state=pdk.ViewState(
                latitude=center_lat,
                longitude=center_lon,
                zoom=12,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=data,  # 전체 데이터 사용
                    get_position='[longitude, latitude]',
                    get_color='color',
                    get_radius=40,
                    pickable=True,
                ),
            ],
            tooltip={"text": "{장소}\n{주소}"}
        ),
        use_container_width=True,
        height=750)
    else:
        st.warning("선택한 자치구에는 흡연구역 데이터가 없습니다.")
