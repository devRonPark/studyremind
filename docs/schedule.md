# 📅 StudyRemind 개발 일정표 (9/29 ~ 10/9)

## 🎯 전체 목표

**MVP 완성 기한: 10/9 (11일)**

개인 학습 자료 기반 RAG 챗봇 + 퀴즈 + 학습 기록 관리 시스템 구축

---

## 📊 마일스톤 개요

| Phase       | 기간        | 주요 목표      | 완료 기준              |
| ----------- | ----------- | -------------- | ---------------------- |
| **Phase 1** | 9/29 ~ 10/3 | RAG 검색 챗봇  | 질문-답변 동작         |
| **Phase 2** | 10/4 ~ 10/7 | 핵심 기능 확장 | 퀴즈 + 코드검색 + 기록 |
| **Phase 3** | 10/8 ~ 10/9 | 배포 및 문서화 | 포트폴리오 완성        |

---

## 📅 일별 상세 계획

### **9/29 (월) - Day 1: 프로젝트 초기 설정**

**목표**: 개발 환경 구축 및 데이터 준비

#### 체크리스트

- [x] GitHub repo 생성 (`studymind`)
- [x] 폴더 구조 세팅
  ```
  /studymind
    /backend      # FastAPI
    /frontend     # Streamlit
    /data         # Notion export
    /docs         # 문서
    /scripts      # 유틸리티
  ```
- [x] 기본 설정 파일 작성
  - `.gitignore`
  - `.env.example`
  - `docker-compose.yml`
  - `requirements.txt` (backend/frontend)
- [x] 노션 export 샘플 확보 (`.md` or `.csv`)
- [x] 데이터 구조 정의 (`page_id, title, content, tags, url, content_type, language`)
- [ ] ERD 다이어그램 초안 작성

#### 산출물

- 초기 Git 커밋
- 프로젝트 뼈대
- PRD.md, schedule.md

---

### **9/30 (화) - Day 2: 데이터 로더 구축**

**목표**: Notion 데이터 → Vector DB 파이프라인

#### 체크리스트

- [ ] `scripts/load_notion.py` 작성
  - Notion export 파일 파싱
  - Markdown → JSON 변환
  - 코드 블록 추출 (`extract_code_blocks()`)
- [ ] `backend/app/utils/text_splitter.py` 구현
  - 문서 chunk 분리 (500 tokens, overlap 50)
  - 코드 블록은 분리하지 않고 통째로 저장
- [ ] FAISS 벡터DB 구축
  - `scripts/build_vector_store.py`
  - Embedding: OpenAI text-embedding-ada-002
  - 메타데이터 스키마 확장 (content_type, language)
- [ ] CLI 테스트: `"Redis 이벤트 저장"` → 관련 chunk 출력

#### 산출물

- `data/vector_db/` 폴더에 FAISS 인덱스 생성
- 샘플 데이터 검색 성공

---

### **10/1 (수) - Day 3: RAG 엔진 구현**

**목표**: 검색 + LLM 연결

#### 체크리스트

- [ ] `backend/app/services/rag_service.py` 작성
  - `search_documents(query, top_k, filters)`
  - FAISS 검색 → k=3 반환
- [ ] `backend/app/services/llm_service.py` 작성
  - Claude API 연동
  - Prompt 템플릿 작성
- [ ] RAG Chain 구성
  - 검색 결과 → Context 구성 → LLM 호출
- [ ] CLI 테스트: `"비동기 세션 관리"` → GPT 응답 확인

#### 산출물

- RAG 검색 엔진 동작
- Python 스크립트로 Q&A 가능

---

### **10/2 (목) - Day 4: API + UI 통합**

**목표**: FastAPI + Streamlit 챗봇 MVP

#### 체크리스트

- [ ] `backend/app/main.py` FastAPI 앱 생성
- [ ] `backend/app/api/chat.py` 엔드포인트 구현
  - `POST /api/chat/ask`
  - 요청: `{"question": "...", "tags": [...]}`
  - 응답: `{"answer": "...", "sources": [...]}`
- [ ] `frontend/app.py` Streamlit 메인 페이지
- [ ] `frontend/pages/1_💬_Chat.py` 챗봇 UI
  - 입력창 → FastAPI 호출 → 답변+근거 출력
  - 채팅 히스토리 표시
- [ ] CORS 설정 및 연동 테스트

#### 산출물

- **MVP RAG 챗봇 완성** (질문-응답 roundtrip)
- Git tag: `v0.1-mvp-chatbot`

---

### **10/3 (금) - Day 5: RAG 검색 품질 개선**

**목표**: 챗봇 안정화 및 성능 튜닝

#### 체크리스트

- [ ] 검색 성능 조정
  - Chunk overlap 실험 (50 → 100)
  - top_k 값 튜닝 (3 → 5)
  - Re-ranking 적용 (선택)
- [ ] 태그 기반 필터링 옵션 추가
  - `POST /api/chat/ask?tags=Redis,FastAPI`
- [ ] 답변 품질 개선
  - Prompt 엔지니어링
  - 근거 문서 출처 명시
- [ ] 사용자 피드백 기능 (👍/👎 버튼)
- [ ] 에러 핸들링 강화

#### 산출물

- **RAG 챗봇 최종 안정화**
- GitHub PR: "feat(rag): 기본 챗봇 기능 완성"

---

### **10/4 (금) - Day 6: 퀴즈 생성 기능**

**목표**: 문서 기반 자동 퀴즈 생성

#### 체크리스트

- [ ] `backend/app/services/quiz_service.py` 작성
  - `generate_quiz(document_id, difficulty, count)`
  - LLM Prompt: 문서 → Q/A 생성
- [ ] `backend/app/api/quiz.py` 엔드포인트
  - `POST /api/quiz/generate`
  - `POST /api/quiz/submit`
- [ ] SQLite DB 스키마 생성
  - `quiz_history` 테이블
- [ ] `frontend/pages/2_📝_Quiz.py` UI
  - "퀴즈 생성" 버튼
  - 객관식/주관식 문제 표시
  - 정답 확인 및 해설

#### 산출물

- 퀴즈 생성 및 풀이 기능
- 기록 로컬 저장 (`db/quiz_log.json` or SQLite)

---

### **10/5 (토) - Day 7: 학습 기록 관리**

**목표**: 로깅 및 통계 기능

#### 체크리스트

- [ ] `backend/app/services/learning_log_service.py` 작성
  - 질문/답변/퀴즈 로그 자동 기록
  - SQLite or JSON 저장소 연결
- [ ] `backend/app/api/learning_log.py` 엔드포인트
  - `GET /api/logs` - 로그 조회
  - `GET /api/stats` - 통계 조회
- [ ] Notion API 연동 (선택)
  - `backend/app/services/notion_service.py`
  - 학습 일지 자동 업데이트
- [ ] `frontend/pages/3_📊_Learning_Log.py` UI
  - 일자별 질문 횟수 그래프 (Plotly)
  - 태그별 학습량 파이차트
  - 퀴즈 정답률 추이

#### 산출물

- 학습 기록 자동화
- 통계 대시보드

---

### **10/6 (일) - Day 8: 코드 검색 강화 🆕**

**목표**: 학습 자료 내 코드 검색 특화 기능

#### 체크리스트

- [ ] `backend/app/services/code_search_service.py` 작성
  - `search_code(query, language, top_k)`
  - 필터: `content_type='code'`, `language='python'`
- [ ] `backend/app/utils/code_extractor.py` 구현
  - 마크다운 코드 블록 추출
  - 언어 감지 및 메타데이터 생성
  - 컨텍스트 추출 (코드 전후 3줄)
- [ ] `backend/app/api/code_search.py` 엔드포인트
  - `POST /api/code/search`
- [ ] LLM 코드 요약 기능
  - `summarize_code(code, language)`
  - "이 코드는 ~하는 패턴입니다" 형태
- [ ] `frontend/pages/2_🔍_Code_Search.py` UI
  - 검색 모드 선택: "전체 검색" / "코드만 검색"
  - 언어 필터 (Python, JavaScript, SQL 등)
  - 문법 하이라이팅 (Pygments)
  - 복사 버튼 + AI 요약 표시

#### 산출물

- 코드 특화 검색 기능 완성
- 언어별 필터링 및 하이라이팅

---

### **10/7 (월) - Day 9: Slack 리마인더**

**목표**: 복습 알림 시스템

#### 체크리스트

- [ ] Slack Bot 생성 및 Token 발급
- [ ] `backend/app/services/slack_service.py` 작성
  - `send_quiz_reminder(user_id)`
  - Slack API 메시지 전송
- [ ] `backend/app/api/reminder.py` 엔드포인트
  - `POST /api/reminder/send`
- [ ] APScheduler 스케줄러 설정
  - 매일 아침 9시 자동 실행
  - "어제 학습한 주제" 기반 퀴즈 1개 전송
- [ ] 간소화된 Spaced Repetition
  - 틀린 문제 → 3일 후 재출제

#### 산출물

- Slack 알림 연동
- 자동 리마인더 시스템

---

### **10/8 (화) - Day 10: UI 개선 및 배포**

**목표**: 사용성 개선 및 배포 준비

#### 체크리스트

- [ ] UI/UX 개선
  - 탭 구조 정리: 챗봇 / 코드검색 / 퀴즈 / 학습기록
  - 로딩 스피너 추가
  - 에러 메시지 개선
  - 반응형 디자인 (모바일 고려)
- [ ] Dockerfile 최적화
  - 멀티스테이지 빌드
  - 이미지 사이즈 최소화
- [ ] Docker Compose 테스트
  - 전체 서비스 통합 실행
- [ ] 배포 환경 세팅
  - Streamlit Cloud or Render
  - 환경 변수 설정
- [ ] E2E 테스트
  - 실제 노션 데이터로 시나리오 테스트
  - 버그 수정

#### 산출물

- 배포 가능한 상태
- 프로덕션 환경 실행

---

### **10/9 (수) - Day 11: 포트폴리오 정리 (마감일)**

**목표**: 문서화 및 최종 점검

#### 체크리스트

- [ ] 프로젝트 문서 정리
  - PRD.md (최신화)
  - ERD.md (데이터베이스 스키마 다이어그램)
  - architecture.md (시스템 아키텍처 다이어그램)
  - API_SPEC.md (API 명세서)
- [ ] README.md 완성
  - 설치 가이드
  - 사용법 (스크린샷 포함)
  - 주요 기능 소개
  - 기술 스택
  - 프로젝트 구조
- [ ] 시연 영상 녹화 (3분 이내)
  - 챗봇 사용 시나리오
  - 코드 검색 데모
  - 퀴즈 풀이 과정
- [ ] GitHub 최종 정리
  - 코드 리뷰 및 리팩토링
  - 주석 추가
  - README 스크린샷 추가
  - 태그 생성: `v1.0`
- [ ] 포트폴리오 사이트에 추가
  - 프로젝트 소개
  - 주요 기능 GIF
  - GitHub 링크

#### 산출물

- **완성된 포트폴리오 프로젝트**
- GitHub Repository 공개
- 시연 영상

---

## 🎯 우선순위 관리

### P0 (필수) - 반드시 완성

- ✅ RAG 기반 검색 챗봇
- ✅ 코드 검색 강화
- ✅ Streamlit UI
- ✅ 기본 문서화

### P1 (중요) - 가능하면 완성

- 퀴즈 생성 기능
- 학습 기록 관리
- Docker 배포

### P2 (선택) - 시간 남으면

- Slack 리마인더
- Notion API 연동
- 고급 통계 기능

---

## ⚠️ 리스크 관리

| 위험 요소         | 발생 시점 | 대응 방안                     |
| ----------------- | --------- | ----------------------------- |
| LLM API 비용 초과 | 지속적    | 캐싱 적용, 무료 티어 모니터링 |
| 검색 품질 낮음    | 10/3      | Chunk 전략 재조정             |
| 개발 일정 지연    | 10/5      | P2 기능 과감히 제외           |
| 노션 데이터 부족  | 9/30      | 샘플 데이터 생성              |

---

## 📈 진행 상황 추적

### 일일 체크포인트

- 매일 저녁 9시: 진행 상황 점검
- GitHub 커밋 기록으로 확인
- 문제 발생 시 즉시 우선순위 재조정

### 완료 기준

- [ ] Phase 1 완료 (10/3) - RAG 챗봇 동작
- [ ] Phase 2 완료 (10/7) - 퀴즈 + 코드검색 + 기록
- [ ] Phase 3 완료 (10/9) - 배포 + 문서화

---

## 💡 팁

1. **데일리 커밋**: 매일 작은 단위로 커밋하여 진행 상황 가시화
2. **기능 단위 브랜치**: `feat/rag-chatbot`, `feat/code-search` 등
3. **테스트 먼저**: CLI 테스트 → API 테스트 → UI 테스트 순서
4. **문서화 병행**: 코드 작성하면서 바로 README 업데이트
5. **시간 박싱**: 하루 작업이 늦어지면 다음날로 넘기지 말고 스코프 축소

---

**목표**: 10/9까지 **실사용 가능한 학습 비서** 완성! 🚀

이 일정대로라면:

- **10/3**: 기본 챗봇 완성
- **10/7**: 모든 핵심 기능 구현
- **10/9**: 포트폴리오 완성

**화이팅!** 💪
