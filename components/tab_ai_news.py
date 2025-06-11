# components/tab_ai_news.py
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import chromadb
from openai import OpenAI
import os

# API 키 설정
def get_api_key(key_name):
    """Streamlit secrets 또는 환경변수에서 API 키 가져오기"""
    try:
        return st.secrets[key_name]
    except:
        return os.getenv(key_name)

# API 키 초기화
OPENAI_API_KEY = get_api_key('OPENAI_API_KEY')
PINECONE_API_KEY = get_api_key('PINECONE_API_KEY')

## --- 유틸 함수 ---
@st.cache_resource
def init_chroma_client():
    """ChromaDB 클라이언트 초기화"""
    return chromadb.PersistentClient(path="data/chroma_db")

@st.cache_data(ttl=300)
def get_available_collections():
    """사용 가능한 컬렉션 목록 가져오기"""
    try:
        client = init_chroma_client()
        return [col.name for col in client.list_collections()]
    except Exception as e:
        st.error(f"컬렉션 목록 로드 오류: {e}")
        return []

def get_collection(collection_name):
    """벡터 데이터베이스에서 컬렉션 가져오기"""
    if not collection_name:
        return None
    try:
        client = init_chroma_client()
        collection = client.get_collection(name=collection_name)
        return collection
    except Exception as e:
        st.error(f"컬렉션 가져오기 오류: {e}")
        return None

def search_vector_db(collection, query, n_results=20):
    """벡터 데이터베이스 검색 함수"""
    try:
        if not collection:
            return [{"content": "컬렉션을 불러올 수 없습니다. 컬렉션을 선택해주세요.", "title": "오류", "metadata": {}}]
       
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
       
        documents = []
        for i in range(len(results['documents'][0])):
            document = {
                "content": results['documents'][0][i],
                "title": results['metadatas'][0][i].get('title', '제목 없음'),
                "metadata": results['metadatas'][0][i]
            }
            documents.append(document)
       
        return documents
    except Exception as e:
        st.error(f"검색 오류: {e}")
        return [{"content": f"검색 중 오류 발생: {e}", "title": "오류", "metadata": {}}]

def get_gpt_response(query, search_results, api_key, model="gpt-4o-mini"):
    """OpenAI를 활용한 응답 생성 함수"""
    if not api_key:
        return "OpenAI API 키가 설정되지 않았습니다."

    try:
        # OpenAI 클라이언트 초기화
        api_key = api_key.replace('\ufeff', '')
        client = OpenAI(api_key=api_key)
       
        # 컨텍스트 구성 (문서 번호 제거)
        context = "다음은 중앙일보에서 수집한 담배 관련 데이터입니다:\n\n"
       
        for i, result in enumerate(search_results):
            context += f"기사 제목: {result['title']}\n"
           
            # 메타데이터에서 필요한 정보만 선별적으로 추가
            if result['metadata']:
                metadata = result['metadata']
                # 사용자에게 유용한 메타데이터만 포함
                if 'published_date' in metadata and metadata['published_date']:
                    context += f"작성일: {metadata['published_date']}\n"
                if 'url' in metadata and metadata['url']:
                    context += f"출처: {metadata['url']}\n"
                if 'source' in metadata and metadata['source']:
                    context += f"언론사: {metadata['source']}\n"
                # 문서 번호나 기타 내부 메타데이터는 제외
           
            # 내용 요약 (너무 길면 잘라냄)
            content = result['content']
            if len(content) > 80000:
                content = content[:80000] + "..."
            context += f"내용: {content}\n\n"

        # 개선된 GPT 프롬프트
        system_prompt = """당신은 담배 및 흡연과 관련된 정책, 건강, 사회적 이슈 전반에 대한 전문 분석가입니다.
        제공된 기사나 문서들을 바탕으로 사용자 질문에 적절한 수준의 답변을 제공해주세요.

        ⚠️ **질문 유형 판별이 매우 중요합니다:**
        
        **간단한 질문 유형 (참고 기사 절대 포함 금지):**
        - 사실 확인: "몇 년도인가요?", "올해는 몇 년인가요?"
        - 단순 정보: "담배 가격은?", "흡연율은?"
        - 팁/조언 요청: "금연 팁을 알려주세요", "금연 방법은?", "어떻게 금연하나요?"
        - 일반적 조언: "금연에 좋은 음식은?", "금연 후 주의사항은?"
        
        → 이런 질문들은 간결하고 직접적으로 답변 (2-5문장)
        → 📰 참고 기사 섹션을 절대 포함하지 마세요
        
        **복잡한 질문 유형 (참고 기사 포함 가능):**
        - 정책 분석: "최근 금연 정책의 효과는?", "정책 변화 내용은?"
        - 현황 분석: "지역별 흡연율 비교", "연도별 추이 분석"
        - 데이터 요청: "구체적인 통계나 수치를 묻는 질문"
        - 사회적 영향: "금연 정책이 사회에 미친 영향은?"
        
        → 이런 질문들만 상세한 답변 + 📰 참고 기사 포함
        
        **절대 금지사항:**
        - 답변에 "(문서 1)", "(문서 20)", "(문서 번호)" 같은 표현 사용 금지
        - "문서에 따르면", "xx번 문서에서" 같은 문서 참조 표현 금지
        - 간단한 질문에 "📰 참고 기사" 섹션 포함 절대 금지
        - 팁이나 조언을 묻는 질문에는 기사 링크 절대 포함하지 마세요
        - 참고 기사에 URL이 없는 기사 제목만 나열하는 것은 금지 (반드시 클릭 가능한 링크 형태로 제공)
        
        **기타 주의사항:**
        - 올해는 2025년입니다
        - 질문 유형을 정확히 판별하여 적절한 답변 형식 선택
        - 자연스러운 한국어 문장으로만 답변
        """

        user_prompt = f"""{context}

        사용자 질문: {query}

        위 기사들을 분석하여 사용자 질문에 답변해주세요.

        🔍 **질문 유형을 먼저 판별하세요:**

        만약 질문이 다음과 같은 **간단한 유형**이라면:
        - 팁/조언 요청 ("금연 팁", "금연 방법", "어떻게 금연", "금연에 좋은", "금연 후 주의사항")
        - 사실 확인 ("몇 년도", "올해는", "가격은")
        - 단순 정보 ("흡연율", "통계")
        
        → 2-5문장으로 간결하고 실용적인 답변만 제공
        → 📰 참고 기사 섹션은 절대 포함하지 마세요

        만약 질문이 다음과 같은 **복잡한 유형**이라면:
        - 정책 분석 ("정책 효과", "정책 변화", "법안 내용")
        - 현황 분석 ("지역별 비교", "연도별 추이", "상세한 현황")
        - 데이터 분석 ("구체적인 통계", "수치 분석", "연구 결과")
        
        → 상세한 답변 + 실제로 참조한 기사만 📰 참고 기사 섹션에 포함
        → 참고 기사 형식: "- [기사 제목](URL 링크)" 형태로 클릭 가능한 링크 제공

        ⚠️ **매우 중요:**
        1. 팁/조언/방법을 묻는 질문에는 기사 링크를 절대 포함하지 마세요
        2. "(문서 번호)" 같은 표현은 절대 사용하지 마세요
        3. 질문 유형을 정확히 판별하여 적절한 형식으로 답변하세요
        4. 복잡한 질문의 경우 참고 기사는 반드시 "[제목](URL)" 형태의 클릭 가능한 링크로 제공하세요
        5. URL이 없는 기사는 참고 기사에 포함하지 마세요
        """

        # API 호출
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # 더 일관된 답변을 위해 낮춤
            max_tokens=1500    # 더 긴 답변을 위해 늘림
        )
       
        return response.choices[0].message.content
       
    except Exception as e:
        error_msg = str(e)
        if "auth" in error_msg.lower() or "api key" in error_msg.lower():
            return "OpenAI API 키 인증에 실패했습니다. API 키를 확인해주세요."
        else:
            return f"분석 중 오류가 발생했습니다: {error_msg}"

def get_simple_response(query, search_results):
    """API 키가 없을 때 간단한 응답을 반환하는 함수"""
    if not search_results or search_results[0].get("title") == "오류":
        return "관련 데이터를 찾을 수 없습니다."
   
    result_text = f"'{query}'에 대한 검색 결과:\n\n"
   
    for i, result in enumerate(search_results[:5]):
        result_text += f"**문서 {i+1}:** {result['title']}\n"
       
        # 날짜 정보 추가
        if 'published_date' in result['metadata']:
            result_text += f"**날짜:** {result['metadata']['published_date']}\n"
       
        # 내용 요약 (150자로 제한)
        content = result['content']
        if len(content) > 150:
            content = content[:150] + "..."
        result_text += f"{content}\n\n"
   
    result_text += "더 자세한 분석을 위해서는 OpenAI API 키를 입력해주세요."
    return result_text

def chat_response(question, collection):
    """챗봇 응답 생성 함수"""
    # 벡터 데이터베이스 검색
    search_results = search_vector_db(collection, question)
   
    # ChatGPT API 키가 있으면 GPT 사용, 없으면 간단한 응답
    if OPENAI_API_KEY:
        return get_gpt_response(question, search_results, OPENAI_API_KEY)
    else:
        return get_simple_response(question, search_results)

def news_chatbot():
    """담배 관련 뉴스 챗봇 메인 함수"""
    st.markdown("## 담배기사 데이터 AI 분석가 ✨")
    st.markdown("""
    담배와 관련된 최근 뉴스, 정책, 흡연 부스, 건강 문제 등 궁금한 점을 자유롭게 질문해보세요.  
    AI가 중앙일보 기사 기반 데이터에서 유의미한 정보를 분석해 친절하게 답변해드립니다.
    """)


    # 컬렉션 목록 가져오기
    collection_list = get_available_collections()
    if not collection_list:
        st.warning("사용 가능한 컬렉션이 없습니다.")
        return

    # 첫 번째 컬렉션 자동 선택 (다른 탭들과 일관성 유지)
    collection_name = collection_list[0]
    
    # 컬렉션 가져오기
    collection = get_collection(collection_name)

    # 컬렉션 정보 표시
    if collection:
        try:
            count = collection.count()
            st.success(f"컬렉션 '{collection_name}'에서 {count:,}개의 문서를 불러왔습니다.")
        except Exception as e:
            st.warning(f"컬렉션 정보 확인 중 오류: {e}")
    else:
        st.warning("컬렉션을 선택하거나 찾을 수 없습니다. 컬렉션 목록을 확인하세요.")
        return

    # 세션 상태 초기화
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "is_processing" not in st.session_state:
        st.session_state.is_processing = False

    # 예시 질문 섹션
    st.markdown(
        "<p style='font-size:20px; font-weight:600;'>💡 예시 질문</p>", 
        unsafe_allow_html=True
    )
    example_questions = [
        "가장 최근에 발표된 금연 정책에는 어떤 내용이 포함되어 있나요?",
        "흡연 부스 설치가 민원 감소에 효과가 있었나요?",
        "담배와 관련된 건강 피해는 어느 정도인가요?",
        "금연 팁을 알려주세요!"
    ]

    # 예시 질문을 4열로 배치 (처리 중일 때는 비활성화)
    cols = st.columns(4)
    for i, question in enumerate(example_questions):
        with cols[i % 4]:
            if st.button(question, key=f"example_{i}", use_container_width=True, disabled=st.session_state.is_processing):
                st.session_state.selected_question = question
                st.session_state.is_processing = True

    # 대화 기록 초기화 버튼 (처리 중일 때는 비활성화)
    if st.button("🗑️ 대화 기록 초기화", disabled=st.session_state.is_processing):
        st.session_state.chat_history = []
        st.session_state.is_processing = False
        st.rerun()

    st.divider()

    # 이전 대화 내용 표시
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 예시 질문 버튼 클릭 시 처리 (채팅창보다 먼저 확인)
    if "selected_question" in st.session_state:
        selected_input = st.session_state.selected_question
        del st.session_state.selected_question
    else:
        selected_input = None

    # 사용자 입력 처리 (처리 중일 때는 채팅창 숨김)
    chat_input = None
    if not st.session_state.is_processing:
        chat_input = st.chat_input("질문을 입력하세요 (예: 서울에서 흡연 구역이 가장 많은 자치구는 어디인가요?)")
        if chat_input:
            st.session_state.is_processing = True
    
    # 최종 입력 결정 (예시 질문 우선, 그 다음 채팅 입력)
    final_input = selected_input if selected_input else chat_input

    if final_input:
        # 컬렉션이 없으면 오류 메시지 표시
        if not collection:
            with st.chat_message("assistant"):
                st.markdown("⚠️ 컬렉션을 선택해주세요. 현재 컬렉션이 선택되지 않았거나 찾을 수 없습니다.")
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": "⚠️ 컬렉션을 선택해주세요. 현재 컬렉션이 선택되지 않았거나 찾을 수 없습니다."
            })
            st.session_state.is_processing = False
        else:
            # 사용자 메시지 표시
            with st.chat_message("user"):
                st.markdown(final_input)

            # 사용자 메시지를 대화 이력에 저장
            st.session_state.chat_history.append({"role": "user", "content": final_input})

            # 응답 생성  
            with st.spinner("질문과 관련된 문서를 수집하여 답변을 준비하고 있는 중..."):
                response = chat_response(final_input, collection)

            # 응답 메시지 표시
            with st.chat_message("assistant"):
                st.markdown(response)

            # AI 응답을 대화 이력에 저장
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # 처리 완료 후 상태 초기화
            st.session_state.is_processing = False

        # 페이지 새로고침
        st.rerun()
    
    # 처리 중일 때 상태 표시
    if st.session_state.is_processing and not final_input:
        st.info("💭 답변을 생성하고 있습니다. 잠시만 기다려주세요...")
