import streamlit as st
import requests
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="StudyMind",
    page_icon="🧠",
    layout="wide"
)

# API 설정
API_BASE_URL = "http://localhost:8000/api/v1"

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []


def check_api_health():
    """API 서버 상태 확인"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def main():
    """메인 앱"""
    
    # 사이드바
    with st.sidebar:
        st.title("🧠 StudyMind")
        st.markdown("### 개인 학습 RAG 챗봇")
        
        # API 상태 확인
        api_status = check_api_health()
        if api_status:
            st.success("✅ API 서버 연결됨")
        else:
            st.error("❌ API 서버 연결 안 됨")
            st.info("Backend 서버를 먼저 실행하세요:\n```\nuvicorn backend.app.main:app --reload\n```")
        
        st.markdown("---")
        st.markdown("### 📋 메뉴")
        menu = st.radio(
            "선택하세요:",
            ["💬 챗봇", "📊 학습 기록", "⚙️ 설정"],
            label_visibility="collapsed"
        )
    
    # 메인 화면
    if menu == "💬 챗봇":
        show_chatbot()
    elif menu == "📊 학습 기록":
        show_learning_log()
    elif menu == "⚙️ 설정":
        show_settings()


def show_chatbot():
    """챗봇 화면"""
    st.title("💬 학습 챗봇")
    st.markdown("노션 문서를 기반으로 질문하세요!")
    
    # 채팅 기록 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message:
                with st.expander("📚 참고 문서"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**{i}. {source.get('title', 'Unknown')}**")
                        st.text(source.get('content', '')[:200] + "...")
    
    # 사용자 입력
    if prompt := st.chat_input("질문을 입력하세요..."):
        # 사용자 메시지 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 봇 응답 표시 (현재는 테스트 응답)
        with st.chat_message("assistant"):
            if check_api_health():
                # TODO: 실제 API 호출로 대체
                response_text = f"질문을 받았습니다: '{prompt}'\n\n(아직 RAG 검색 기능이 연결되지 않았습니다. 10/3까지 구현 예정)"
                st.markdown(response_text)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text
                })
            else:
                st.error("API 서버가 실행되지 않았습니다. 사이드바를 확인하세요.")


def show_learning_log():
    """학습 기록 화면 (추후 구현)"""
    st.title("📊 학습 기록")
    st.info("10/5에 구현 예정입니다.")
    
    # 샘플 데이터
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("총 질문 수", "0")
    with col2:
        st.metric("퀴즈 풀이 수", "0")
    with col3:
        st.metric("학습 일수", "1")


def show_settings():
    """설정 화면"""
    st.title("⚙️ 설정")
    
    st.subheader("API 연결 정보")
    st.code(f"Backend URL: {API_BASE_URL}")
    
    if st.button("🔄 API 연결 테스트"):
        if check_api_health():
            st.success("✅ 연결 성공!")
        else:
            st.error("❌ 연결 실패")
    
    st.markdown("---")
    st.subheader("프로젝트 정보")
    st.markdown("""
    - **버전**: MVP v0.1
    - **개발 기간**: 9/29 ~ 10/9
    - **현재 상태**: Phase 1 (기본 설정)
    """)


if __name__ == "__main__":
    main()