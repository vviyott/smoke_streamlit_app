# -*- coding: utf-8 -*-  
# utils/naver_api_shop.py
# 프로그램 설명: 네이버 쇼핑 API를 사용하여 쇼핑 목록을 가져오고, 엑셀 파일에 저장하는 유틸리티 함수들

import pandas as pd
import json
import os
import urllib.request
import urllib.parse
import datetime
from pathlib import Path

# 네이버 API 클라이언트 정보
CLIENT_ID = "qUdRFUYQv27dI6GZr4Wz"
CLIENT_SECRET = "HWYWOFBEYH"

def get_naver_shopping_data(search_query, display=100, sort='date'):
    """
    네이버 쇼핑 API를 사용하여 상품 목록을 가져오는 함수
    
    Args:
        search_query (str): 검색할 상품명
        display (int): 가져올 상품 개수 (최대 100개)
        sort (str): 정렬 방식 ('date', 'sim', 'asc', 'dsc')
    
    Returns:
        str: JSON 형태의 응답 데이터
    """
    try:
        # 검색어 URL 인코딩
        enc_text = urllib.parse.quote(search_query)
        
        # API URL 구성
        url = f"https://openapi.naver.com/v1/search/shop?sort={sort}&display={display}&query={enc_text}"
        
        # HTTP 요청 생성
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", CLIENT_ID)
        request.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
        
        # API 호출
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        
        if rescode == 200:
            response_body = response.read()
            result = response_body.decode('utf-8')
            return result
        else:
            raise Exception(f"API 호출 실패 - Error Code: {rescode}")
            
    except Exception as e:
        raise Exception(f"네이버 쇼핑 API 호출 중 오류 발생: {str(e)}")

def convert_json_to_dataframe(json_result):
    """
    JSON 결과를 pandas DataFrame으로 변환하는 함수
    
    Args:
        json_result (str or dict): JSON 형태의 쇼핑 데이터
    
    Returns:
        pd.DataFrame: 상품 정보가 담긴 DataFrame (순위 열 포함)
    """
    try:
        # 문자열인 경우 딕셔너리로 변환
        if isinstance(json_result, str):
            json_result = json.loads(json_result)
        
        # items 데이터 추출
        items = json_result.get('items', [])
        
        if not items:
            return pd.DataFrame()  # 빈 DataFrame 반환
        
        # DataFrame 생성
        df = pd.DataFrame(items)
        
        # 순위 열 추가 (1부터 시작)
        df.insert(0, "순위", range(1, len(df) + 1))
        
        # 순위를 인덱스로 설정
        df.set_index("순위", inplace=True)
        
        return df
        
    except Exception as e:
        raise Exception(f"JSON to DataFrame 변환 중 오류 발생: {str(e)}")

def clean_and_process_shopping_data(df):
    """
    쇼핑 데이터를 정제하고 가공하는 함수
    
    Args:
        df (pd.DataFrame): 원본 쇼핑 데이터
    
    Returns:
        pd.DataFrame: 정제된 쇼핑 데이터
    """
    if df.empty:
        return df
    
    try:
        # 데이터 복사본 생성
        df_processed = df.copy()
        
        # HTML 태그 제거 (title 컬럼)
        if 'title' in df_processed.columns:
            df_processed['title'] = df_processed['title'].str.replace('<[^<]+?>', '', regex=True)
        
        # 가격 정보 처리 (lprice, hprice)
        price_columns = ['lprice', 'hprice']
        for col in price_columns:
            if col in df_processed.columns:
                df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
        
        # 가격 정보 추가 (포맷팅된 가격)
        if 'lprice' in df_processed.columns:
            df_processed['가격_포맷'] = df_processed['lprice'].apply(
                lambda x: f"{x:,}원" if pd.notna(x) and x > 0 else "가격정보없음"
            )
        
        # 쇼핑몰 정보 정리
        if 'mallName' in df_processed.columns:
            df_processed['쇼핑몰'] = df_processed['mallName'].fillna('정보없음')
        
        return df_processed
        
    except Exception as e:
        raise Exception(f"데이터 정제 중 오류 발생: {str(e)}")

def save_to_csv(df, search_query, save_dir="data"):
    """
    DataFrame을 CSV 파일로 저장하는 함수
    
    Args:
        df (pd.DataFrame): 저장할 데이터
        search_query (str): 검색어 (파일명에 사용)
        save_dir (str): 저장할 디렉토리
    
    Returns:
        str: 저장된 파일 경로
    """
    try:
        # 저장 디렉토리 생성
        save_path = Path(save_dir)
        save_path.mkdir(exist_ok=True)
        
        # 파일명 생성 (검색어 + 타임스탬프)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_query = "".join(c for c in search_query if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"naver_shopping_{safe_query}_{timestamp}.csv"
        file_path = save_path / filename
        
        # CSV 파일로 저장 (UTF-8 인코딩, 인덱스 포함)
        df.to_csv(file_path, encoding='utf-8-sig', index=True)
        
        return str(file_path)
        
    except Exception as e:
        raise Exception(f"CSV 파일 저장 중 오류 발생: {str(e)}")

def get_shopping_data_summary(df):
    """
    쇼핑 데이터의 요약 정보를 생성하는 함수
    
    Args:
        df (pd.DataFrame): 쇼핑 데이터
    
    Returns:
        dict: 요약 정보
    """
    if df.empty:
        return {
            "총_상품수": 0,
            "평균가격": 0,
            "최저가": 0,
            "최고가": 0,
            "쇼핑몰수": 0
        }
    
    try:
        summary = {}
        
        # 기본 정보
        summary["총_상품수"] = len(df)
        
        # 가격 정보 (lprice 컬럼 기준)
        if 'lprice' in df.columns:
            price_data = df['lprice'].dropna()
            price_data = price_data[price_data > 0]  # 0원 제외
            
            if len(price_data) > 0:
                summary["평균가격"] = int(price_data.mean())
                summary["최저가"] = int(price_data.min())
                summary["최고가"] = int(price_data.max())
            else:
                summary["평균가격"] = 0
                summary["최저가"] = 0
                summary["최고가"] = 0
        
        # 쇼핑몰 정보
        if 'mallName' in df.columns:
            summary["쇼핑몰수"] = df['mallName'].nunique()
        else:
            summary["쇼핑몰수"] = 0
        
        return summary
        
    except Exception as e:
        return {
            "총_상품수": len(df) if not df.empty else 0,
            "평균가격": 0,
            "최저가": 0,
            "최고가": 0,
            "쇼핑몰수": 0,
            "오류": str(e)
        }

def search_and_save_shopping_data(search_query, display=100, sort='date', save_dir="data"):
    """
    검색부터 저장까지 전체 프로세스를 수행하는 통합 함수
    
    Args:
        search_query (str): 검색할 상품명
        display (int): 가져올 상품 개수
        sort (str): 정렬 방식
        save_dir (str): 저장 디렉토리
    
    Returns:
        tuple: (DataFrame, 파일경로, 요약정보)
    """
    try:
        # 1. API 호출
        json_result = get_naver_shopping_data(search_query, display, sort)
        
        # 2. DataFrame 변환
        df_raw = convert_json_to_dataframe(json_result)
        
        # 3. 데이터 정제
        df_processed = clean_and_process_shopping_data(df_raw)
        
        # 4. CSV 저장
        file_path = save_to_csv(df_processed, search_query, save_dir)
        
        # 5. 요약 정보 생성
        summary = get_shopping_data_summary(df_processed)
        
        return df_processed, file_path, summary
        
    except Exception as e:
        raise Exception(f"쇼핑 데이터 처리 중 오류 발생: {str(e)}")