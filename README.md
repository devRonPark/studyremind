# 🧠 StudyMind

> **AI 기반 개인 학습 비서** - RAG를 활용한 스마트 학습 기록 관리 시스템

개발 공부 중 노션에 쌓인 자료들을 효율적으로 검색하고, 자동 퀴즈 생성으로 복습하며, 학습 기록을 자동으로 관리하는 AI 챗봇입니다.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 프로젝트 목적

### 해결하려는 문제

- 📚 **노션에 자료는 많지만 검색이 비효율적** - 키워드 검색의 한계
- 🧩 **공부한 내용이 기억에 남지 않음** - 복습 시스템 부재
- 📊 **학습 기록 관리가 수동적** - 로그와 통계 기능 없음
- 💻 **예전에 작성한 코드 찾기 어려움** - 코드 스니펫 검색 불편

### 제공하는 가치

- ✅ AI 기반 의미 검색으로 관련 학습 자료를 즉시 찾기
- ✅ 자동 퀴즈 생성으로 효과적인 복습
- ✅ 학습 패턴 분석 및 자동 로깅
- ✅ 언어별 코드 검색 및 문법 하이라이팅

---

## ✨ 주요 기능

### 1. 💬 RAG 기반 스마트 검색

- 노션/문서 내용을 벡터 DB에 저장
- 자연어 질문으로 관련 문서 검색
- GPT 기반 답변 + 근거 문서 제공

### 2. 🔍 학습 자료 내 코드 검색 강화

- **코드 블록 특화 검색**: 마크다운 코드 블록만 필터링하여 검색
- **언어별 필터링**: Python, JavaScript, SQL 등 언어 선택
- **문법 하이라이팅**: 코드를 언어에 맞게 색상 표시
- **AI 코드 요약**: 각 코드의 목적과 사용법 자동 설명
- **실행 컨텍스트 제공**: 코드 주변 설명 + 관련 코드 추천
- **원클릭 복사**: 코드 복사 버튼 제공

### 3. 📝 자동 퀴즈 생성

- 학습 자료 기반 객관식/주관식 퀴즈 자동 생성
- 퀴즈 풀이 및 정답 확인
- 결과 자동 기록 및 통계

### 4. 📊 학습 기록 관리

- 질문, 검색, 퀴즈 결과 자동 로깅
- 태그별 학습 통계 제공
- Notion API 연동으로 자동 업데이트

### 5. ⏰ 학습 리마인더

- Slack 알림으로 복습 퀴즈 제공
- Spaced Repetition 알고리즘 적용

---

## 🛠 기술 스택

### Backend

- **Framework**: FastAPI
- **LLM**: Claude API (Anthropic)
- **Vector DB**: FAISS (향후 Chroma 확장)
- **Database**: SQLite
- **Task Queue**: APScheduler

### Frontend

- **UI Framework**: Streamlit
- **Code Highlighting**: Pygments
- **향후 확장**: React (예정)

### Integrations

- **Notion API**: 학습 기록 자동 동기화
- **Slack API**: 리마인더 및 알림

### Infrastructure

- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Deployment**: Streamlit Cloud / Render

---

## 📦 설치 및 실행

### 1. 사전 요구사항

- Python 3.11+
- Docker & Docker Compose (선택사항)
- Claude API Key
- Notion API Token (선택사항)

### 2. 설치

```bash
# 저장소 클론
git clone https://github.com/yourusername/studymind.git
cd studymind

# 환경 변수 설정
cp .env.example .env
# .env 파일에 API 키 입력

# Backend 설치
cd backend
pip install -r requirements.txt

# Frontend 설치
cd ../frontend
pip install -r requirements.txt
```

### 3. 데이터 준비

```bash
# Notion 데이터 export
# 1. Notion에서 워크스페이스 export (Markdown & CSV)
# 2. data/notion_export/ 폴더에 저장

# 벡터 DB 구축
cd scripts
python load_notion.py
python build_vector_store.py
```

### 4. 실행

#### 방법 1: 개별 실행

```bash
# Backend 실행 (터미널 1)
cd backend
uvicorn app.main:app --reload --port 8000

# Frontend 실행 (터미널 2)
cd frontend
streamlit run app.py
```

#### 방법 2: Docker Compose

```bash
docker-compose up -d
```

애플리케이션 접속:

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📁 프로젝트 구조

```
studymind/
├── backend/          # FastAPI 백엔드
│   ├── app/
│   │   ├── api/      # API 엔드포인트
│   │   │   ├── chat.py
│   │   │   ├── quiz.py
│   │   │   └── learning_log.py
│   │   ├── services/ # 비즈니스 로직
│   │   │   ├── rag_service.py
│   │   │   ├── code_search_service.py
│   │   │   └── quiz_service.py
│   │   ├── models/   # 데이터 모델
│   │   └── utils/    # 유틸리티
│   │       ├── code_extractor.py
│   │       └── syntax_highlighter.py
│   └── tests/
├── frontend/         # Streamlit 프론트엔드
│   ├── pages/        # 멀티페이지 앱
│   │   ├── 1_💬_Chat.py
│   │   ├── 2_🔍_Code_Search.py
│   │   ├── 3_📝_Quiz.py
│   │   └── 4_📊_Learning_Log.py
│   ├── components/   # 재사용 컴포넌트
│   └── utils/
├── data/             # 데이터 저장소
│   ├── notion_export/
│   └── vector_db/
├── docs/             # 프로젝트 문서
└── scripts/          # 유틸리티 스크립트
```

---

## 🚀 사용 방법

### 1. RAG 챗봇 사용

1. Frontend 접속 → "💬 Chat" 탭
2. 학습 관련 질문 입력
3. AI 답변 + 관련 문서 확인

예시:

```
질문: "Redis 이벤트 저장 방식 알려줘"
→ 관련 노션 문서를 찾아 요약 답변 제공
```

### 2. 코드 검색

1. "🔍 Code Search" 탭 이동
2. 검색 모드 선택: "코드만 검색"
3. 언어 필터 선택 (Python, JavaScript 등)
4. 질문 입력: "FastAPI 의존성 주입 예제"
5. 결과 확인:
   - 문법 하이라이팅된 코드
   - AI 요약 설명
   - 주변 컨텍스트
   - 복사 버튼으로 원클릭 복사

예시:

```
질문: "비동기 처리 코드"
필터: Python
→ async/await 사용 예제들
→ 각 코드의 용도 설명
→ 관련 코드 추천
```

### 3. 퀴즈 풀기

1. "📝 Quiz" 탭 이동
2. 주제 선택 또는 자동 생성
3. 퀴즈 풀이 및 결과 확인

### 4. 학습 기록 확인

1. "📊 Learning Log" 탭
2. 일별/태그별 학습 통계 확인
3. Notion 동기화 상태 확인

---

## 📈 로드맵

### ✅ Phase 1: MVP (10/3까지)

- [x] RAG 기반 검색 챗봇
- [x] 노션 데이터 로더
- [x] FAISS 벡터 DB 구축
- [x] Streamlit 기본 UI

### 🚧 Phase 2: 핵심 기능 (10/7까지)

- [ ] 퀴즈 자동 생성
- [ ] 학습 기록 관리
- [ ] Notion API 연동
- [ ] 코드 검색 강화 (코드 블록 추출, 언어별 필터링, AI 요약)

### 🔮 Phase 3: 확장 (10/9까지)

- [ ] Slack 리마인더
- [ ] 학습 통계 대시보드
- [ ] Docker 배포
- [ ] 포트폴리오 문서화

### 💡 Future

- [ ] React 프론트엔드 전환
- [ ] 다중 사용자 지원
- [ ] 팀 지식 베이스 모드
- [ ] 코드 실행 환경 통합
- [ ] 모바일 앱

---

## 🧪 테스트

```bash
# Backend 테스트
cd backend
pytest tests/ -v

# 커버리지 확인
pytest --cov=app tests/

# 코드 검색 기능 테스트
pytest tests/test_services/test_code_search_service.py -v
```

---

## 🤝 기여 방법

1. Fork the repository
2. Create your feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat(code-search): Add language filtering'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

커밋 메시지는 [Conventional Commits](https://www.conventionalcommits.org/) 규칙을 따릅니다.

---

## 📝 라이선스

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 작성자

**Your Name**

- GitHub: [@devRonPark](https://github.com/devRonPark)
- Email: pbc9236@gmail.com

---

## 🙏 감사의 말

- [Anthropic Claude](https://www.anthropic.com/) - LLM API 제공
- [LangChain](https://www.langchain.com/) - RAG 구현 프레임워크
- [FAISS](https://github.com/facebookresearch/faiss) - 벡터 검색 엔진
- [Notion API](https://developers.notion.com/) - 학습 데이터 연동
- [Pygments](https://pygments.org/) - 코드 문법 하이라이팅

---

## 📚 참고 자료

- [프로젝트 PRD](docs/PRD.md)
- [API 문서](http://localhost:8000/docs)
- [아키텍처 다이어그램](docs/architecture.md)
- [개발 일정표](docs/schedule.md)

---

**⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!**
