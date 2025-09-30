# -*- coding: utf-8 -*-
# components/tab_shopping_compare.py
# 네이버 쇼핑 API 기반 상품 가격 비교 시스템

import streamlit as st
import plotly.express as px
import pandas as pd
from pathlib import Path
import sys

# 상위 디렉토리의 utils 모듈 import를 위한 경로 추가
sys.path.append(str(Path(__file__).parent.parent))
from utils.naver_api_shop import search_and_save_shopping_data, get_shopping_data_summary

def shopping_compare():
    """네이버 쇼핑 가격 비교 탭 내용"""
    # 쇼핑 탭 전용 버튼 색상 스타일
    st.markdown("""
    <style>
    /* 쇼핑 탭의 primary 버튼들만 타겟팅 */
    .stButton > button[kind="primary"] {
        background-color: #5DADE2 !important;
        border-color: #5DADE2 !important;
        color: white !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #357ABD !important;
        border-color: #357ABD !important;
        color: white !important;
    }

    .stButton > button[kind="primary"]:active {
        background-color: #2E5A87 !important;
        border-color: #2E5A87 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 제목 및 설명
    st.markdown("## 🛍️ 네이버 쇼핑 가격비교")
    st.markdown("""
    네이버 쇼핑에서 다양한 상품의 가격 정보를 검색해 비교해보세요.  
    원하는 상품명을 입력하거나, 이전에 저장한 파일을 불러와 쇼핑몰별 가격 차이를 시각적으로 확인할 수 있습니다.
    """)

    # 상품 검색 섹션
    st.markdown("<p style='font-size:20px; font-weight:600;'>🔍 상품 검색</p>", unsafe_allow_html=True)
    
    # 검색 옵션
    col1, col2 = st.columns(2)
    
    with col1:
        display_count = st.selectbox(
            "가져올 상품 수",
            options=[20, 50, 100],
            index=1,
            help="API에서 가져올 상품 개수 (최대 100개)"
        )
    
    with col2:
        sort_options = {
            "최신순": "date",
            "정확도순": "sim", 
            "가격낮은순": "asc",
            "가격높은순": "dsc"
        }
        
        sort_display = st.selectbox(
            "정렬 방식",
            options=list(sort_options.keys()),
            index=0
        )
        
        # 선택된 표시명을 API 값으로 변환
        sort_option = sort_options[sort_display]
    
    # 검색 입력력
    col1, col2 = st.columns(2)
    
    with col1:
        search_query = st.text_input("검색어",
            placeholder="예: 액상형 전자담배, 블루투스 이어폰, 스마트폰 등 원하시는 물건을 입력해주세요.",
            help="네이버 쇼핑에서 검색할 상품명을 입력하세요",
            label_visibility="collapsed"  # 라벨을 숨김
        )

    with col2:
        search_button = st.button("🔍 검색 실행", type="primary", use_container_width=True)

    if search_button and not search_query.strip():
        st.warning("⚠️ 검색어를 입력해주세요!")
    
    # 기존 CSV 파일 로드 옵션
    st.markdown("---")
    st.markdown("<p style='font-size:20px; font-weight:600;'>📁 저장된 데이터 불러오기</p>", unsafe_allow_html=True)
    
    data_dir = Path("data")
    if data_dir.exists():
        csv_files = list(data_dir.glob("naver_shopping_*.csv"))
        if csv_files:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                selected_file = st.selectbox(
                    "불러올 파일 선택",
                    options=["선택안함"] + [f.name for f in csv_files],
                    help="이전에 저장된 검색 결과를 불러올 수 있습니다"
                    ,label_visibility="collapsed"  # 라벨을 숨김
                )
            
            with col2:
                if selected_file != "선택안함":
                    load_button = st.button("📂 파일 불러오기", type="primary", use_container_width=True)
                    if load_button:
                        try:
                            file_path = data_dir / selected_file
                            st.session_state['shopping_df'] = pd.read_csv(file_path, index_col=0)
                            st.session_state['file_loaded'] = True
                            st.success(f"✅ {selected_file} 파일을 불러왔습니다!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ 파일 로드 중 오류: {str(e)}")
        else:
            st.info("💡 저장된 검색 결과가 없습니다. 먼저 상품을 검색해보세요!")
    
    # 검색 실행
    if search_button and search_query.strip():
        with st.spinner(f"🔍 '{search_query}' 검색 중..."):
            try:
                # 네이버 API 호출 및 데이터 저장
                df, file_path, summary = search_and_save_shopping_data(
                    search_query=search_query.strip(),
                    display=display_count,
                    sort=sort_option,
                    save_dir="data"
                )
                
                # 세션 상태에 저장
                st.session_state['shopping_df'] = df
                st.session_state['shopping_summary'] = summary
                st.session_state['file_path'] = file_path
                st.session_state['search_query'] = search_query.strip()
                
                st.success(f"✅ 검색 완료! {summary['총_상품수']}개 상품을 찾았습니다.")
                st.info(f"💾 데이터가 저장되었습니다: `{file_path}`")
                
            except Exception as e:
                st.error(f"❌ 검색 중 오류가 발생했습니다: {str(e)}")
                return
    
    # 데이터 시각화 및 분석
    if 'shopping_df' in st.session_state and not st.session_state['shopping_df'].empty:
        df = st.session_state['shopping_df']
        
        # 요약 정보 표시
        if 'shopping_summary' in st.session_state:
            summary = st.session_state['shopping_summary']
            
            # 요약 메트릭 표시
            col1, col2, col3= st.columns(3)
            
            with col1:
                st.metric("총 상품수", f"{summary['총_상품수']:,}개")
            
            with col2:
                if summary['평균가격'] > 0:
                    st.metric("평균 가격", f"{summary['평균가격']:,}원")
                else:
                    st.metric("평균 가격", "정보없음")
            
            with col3:
                if summary['최저가'] > 0:
                    st.metric("최저가", f"{summary['최저가']:,}원")
                else:
                    st.metric("최저가", "정보없음")
            
            # with col4:
            #     st.metric("쇼핑몰 수", f"{summary['쇼핑몰수']:,}개")
        
        # 데이터 미리보기
        with st.expander("🔍 선택된 파일의 상품 데이터 미리보기", expanded=False):
            # 주요 컬럼만 표시
            display_columns = []
            for col in ['title', 'lprice', 'mallName', 'link']:
                if col in df.columns:
                    display_columns.append(col)
            
            if display_columns:
                st.dataframe(
                    df[display_columns].head(10),
                    use_container_width=True,
                    height=300
                )
            else:
                st.dataframe(df.head(10), use_container_width=True, height=300)
        
        # 가격 분석을 위한 데이터 전처리
        if 'lprice' in df.columns and 'mallName' in df.columns:
            # 가격이 0보다 큰 데이터만 필터링
            price_df = df[df['lprice'] > 0].copy()
            
            if len(price_df) > 0:
                # 쇼핑몰별 통계 계산
                mall_stats = price_df.groupby('mallName').agg({
                    'lprice': ['mean', 'min', 'max', 'count']
                }).round(0)
                
                mall_stats.columns = ['평균가격', '최저가', '최고가', '상품수']
                mall_stats = mall_stats.reset_index()
                mall_stats = mall_stats[mall_stats['상품수'] >= 1]  # 최소 1개 이상 상품
                
                if len(mall_stats) > 0:
                    # 시각화 옵션
                    col1, col2 = st.columns([3, 1])
                    
                    with col2:
                        st.markdown("**차트 설정**")
                        
                        # 분석 기준 선택
                        analysis_type = st.radio(
                            "분석 기준",
                            options=["평균가격", "최저가", "최고가", "상품수"],
                            index=0
                        )
                        
                        # 정렬 방식
                        sort_order = st.radio(
                            "가격 정렬 방식",
                            options=["높은순", "낮은순", "이름순"],
                            index=0
                        )
                        
                        # 색상 선택
                        color_options = {
                            "🔴 빨간색": "#e61813",
                            "🟠 주황색": "#FF7F0E", 
                            "🟡 노란색": "#F0CA4D",
                            "🟢 초록색": "#60BD68",
                            "🔵 파란색": "#5DA5DA",
                            "🟣 보라색": "#B276B2"
                        }
                        selected_color = st.selectbox(
                            "차트 색상",
                            options=list(color_options.keys()),
                            index=2
                        )
                        
                        # 표시할 상위 개수
                        top_n = st.slider(
                            "표시할 쇼핑몰 수",
                            min_value=5,
                            max_value=min(20, len(mall_stats)),
                            value=min(10, len(mall_stats))
                        )
                    
                    with col1:
                        # 데이터 정렬
                        if sort_order == "높은순":
                            mall_stats_sorted = mall_stats.sort_values(by=analysis_type, ascending=False)
                        elif sort_order == "낮은순":
                            mall_stats_sorted = mall_stats.sort_values(by=analysis_type, ascending=True)
                        else:  # 이름순
                            mall_stats_sorted = mall_stats.sort_values(by='mallName')
                        
                        # 상위 N개만 선택
                        mall_stats_top = mall_stats_sorted.head(top_n)
                        
                        # Plotly 막대 그래프 생성
                        fig = px.bar(
                            mall_stats_top,
                            x='mallName',
                            y=analysis_type,
                            title=f'📈 쇼핑몰별 {analysis_type} 비교',
                            color_discrete_sequence=[color_options[selected_color]]
                        )
                        
                        # 그래프 스타일링
                        fig.update_layout(
                            title_font_size=20,
                            title_font_color='black',
                            xaxis_title="쇼핑몰",
                            yaxis_title=analysis_type,
                            yaxis=dict(tickformat=','),
                            plot_bgcolor='white',
                            hoverlabel=dict(
                                bgcolor="white",
                                font_size=14
                            ),
                            height=500
                        )
                        
                        # 호버 템플릿 설정
                        if analysis_type in ['평균가격', '최저가', '최고가']:
                            hover_template = '<b>%{x}</b><br>' + f'{analysis_type}: %{{y:,}}원'
                        else:
                            hover_template = '<b>%{x}</b><br>' + f'{analysis_type}: %{{y:,}}개'
                        
                        fig.update_traces(
                            hovertemplate=hover_template,
                            marker_line_color='rgb(8,48,107)',
                            marker_line_width=1.5,
                            opacity=0.8
                        )
                        
                        # 그리드 추가
                        fig.update_layout(
                            yaxis=dict(
                                showgrid=True,
                                gridwidth=1,
                                gridcolor='rgba(0,0,0,0.1)'
                            )
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
    
    else:
        # 데이터가 없을 때 안내 메시지

        st.warning("🔍 상품을 검색하거나 저장된 파일을 불러와서 가격 비교를 시작하세요!")
