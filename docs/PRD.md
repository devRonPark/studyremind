# PRD: StudyRemind (개인 학습 RAG 챗봇)

## 1. 배경 및 목적

### 배경

개발 공부 중 노션/메모에 기록은 많이 하지만, 다시 찾거나 복습하는 과정이 비효율적입니다.

- 키워드 검색의 한계: 정확한 단어를 기억해야만 찾을 수 있음
- 복습 시스템 부재: 공부한 내용이 기억에 남지 않음
- 코드 스니펫 관리 어려움: 예전에 작성한 코드를 찾기 힘듦

### 목적

개인 학습 자료를 기반으로 검색, 퀴즈, 기록 관리를 자동화하는 **AI 기반 학습 비서** 개발

### 포트폴리오 가치

- RAG·LLM 활용 능력 입증
- API 연동(FastAPI/Notion/Slack) 경험
- 실사용 가능한 생산성 도구 구현력 어필
- 데이터 처리 및 벡터 검색 엔진 구축 능력

---

## 2. 타겟 오디언스

### 1차 타겟

- 개발 공부하는 개인 (예: 개발자 본인)
- 학습 자료를 체계적으로 관리하고 싶은 사람
- 복습 시스템이 필요한 학습자

### 2차 타겟 (향후 확장)

- 팀 내 지식 공유가 필요한 조직
- 신입 개발자 온보딩을 위한 팀

---

## 3. 핵심 페인포인트

| 문제             | 현재 상황                               | 목표 상태               |
| ---------------- | --------------------------------------- | ----------------------- |
| 비효율적 검색    | 노션에 자료가 많아도 키워드 검색만 가능 | 의미 기반 자연어 검색   |
| 복습 부족        | 공부한 내용이 잘 기억 안 남             | 자동 퀴즈로 리텐션 강화 |
| 수동 기록 관리   | 학습 로그/통계가 없음                   | 자동 로깅 및 통계 제공  |
| 코드 찾기 어려움 | 예전 코드 스니펫을 찾기 힘듦            | 언어별 코드 검색        |

---

## 4. 주요 기능

### 4.1. RAG 기반 검색 (MVP) ⭐

**우선순위: P0 (필수)**

#### 기능 설명

- 노션/문서 내용을 벡터DB에 저장
- 사용자가 자연어로 질문하면 관련 문서 찾아 GPT 응답 + 근거 제공

#### 핵심 요구사항

- 질문-답변 정확도 > 80%
- 평균 응답 시간 < 3초
- 근거 문서 출처 명시 (링크, 제목)

#### 기술 스펙

- Vector DB: FAISS
- Embedding: OpenAI text-embedding-ada-002
- LLM: Claude API
- Chunk size: 500 tokens, overlap: 50

#### UI/UX

- Streamlit 챗봇 인터페이스
- 질문 입력창 + 답변 + 관련 문서 카드

---

### 4.2. 학습 자료 내 코드 검색 강화 ⭐

**우선순위: P0 (필수)**

#### 기능 설명

노션에 저장된 코드 블록을 특화하여 검색하고, 언어별로 필터링하며, AI가 코드를 요약 설명

#### 세부 기능

1. **코드 블록 추출 및 인덱싱**

   - 마크다운 `코드블록` 자동 감지
   - 언어 메타데이터 태깅 (Python, JavaScript, SQL 등)
   - 코드 + 주변 설명 컨텍스트 함께 저장

2. **언어별 필터링**

   - 사용자가 특정 언어만 검색 가능
   - 지원 언어: Python, JavaScript, TypeScript, SQL, Shell, Go

3. **문법 하이라이팅**

   - Pygments 라이브러리 활용
   - 언어에 맞는 색상 표시

4. **AI 코드 요약**

   - 각 코드의 목적과 사용법을 1-2줄로 설명
   - "이 코드는 ~하는 패턴입니다" 형태

5. **실행 컨텍스트 제공**

   - 코드 주변의 설명 표시
   - 관련 코드 추천 (유사한 패턴의 다른 코드)

6. **원클릭 복사**
   - 코드 블록 복사 버튼 제공

#### 기술 스펙

- 코드 추출: 정규표현식 기반 파서
- 문법 하이라이팅: Pygments
- 메타데이터 스키마:
  ```json
  {
    "content_type": "code",
    "language": "python",
    "code": "...",
    "context_before": "...",
    "context_after": "...",
    "related_codes": []
  }
  ```

#### UI/UX

- "🔍 Code Search" 전용 탭
- 사이드바: 언어 필터 (체크박스)
- 검색 결과: 코드 + 요약 + 컨텍스트
- 복사 버튼 배치

---

### 4.3. 퀴즈 생성

**우선순위: P1 (중요)**

#### 기능 설명

- 문서 기반 객관식/주관식 퀴즈 자동 생성
- 사용자는 퀴즈를 풀고 정답 확인
- 기록은 DB에 저장

#### 세부 기능

- 난이도 선택 (쉬움, 보통, 어려움)
- 퀴즈 유형: 객관식(4지선다), 단답형
- 정답 확인 및 해설 제공
- 틀린 문제 복습 큐에 자동 추가

#### 기술 스펙

- LLM 프롬프트로 퀴즈 생성
- 저장: SQLite (quiz_id, question, answer, user_answer, is_correct, timestamp)

---

### 4.4. 학습 기록 관리

**우선순위: P1 (중요)**

#### 기능 설명

- 사용자의 질문, 검색, 퀴즈 결과를 자동 로그화
- 태그별 학습 통계 제공
- Notion API 연동으로 기록 자동 업데이트

#### 세부 기능

- 일별 질문 횟수 그래프
- 태그별 학습량 파이차트
- 학습 시간 추적
- 퀴즈 정답률 추이

#### 기술 스펙

- DB 스키마: user_id, action_type, content, tags, timestamp
- Notion API: 학습 일지 페이지 자동 생성
- 시각화: Plotly

---

### 4.5. 학습 리마인더

**우선순위: P2 (선택)**

#### 기능 설명

- Slack/Notion 알림으로 "복습 퀴즈" 제공
- Spaced Repetition 알고리즘 간단 적용

#### 세부 기능

- 매일 아침 9시 Slack 메시지
- "어제 학습한 주제" 기반 퀴즈 1개
- 틀린 문제는 3일 후 재출제

#### 기술 스펙

- Slack Bot API
- APScheduler (cron job)
- 간소화된 Spaced Repetition: 1일 → 3일 → 7일

---

## 5. 비기능 요구사항

### 5.1. 성능

- RAG 검색 응답 시간: 평균 < 3초
- 퀴즈 생성 시간: < 5초
- 동시 사용자: 1명 (MVP), 향후 10명까지 확장

### 5.2. 개발 속도

- **MVP 완성 기한: 10/9**
- 데일리 커밋 필수
- 기능별 브랜치 관리

### 5.3. 사용성

- 최소한의 UI (챗봇, 퀴즈 탭)
- 설치/실행 가이드 완비
- 3분 이내 시연 가능한 데모

### 5.4. 확장성

- 노션/Slack API 연동 고려
- 다중 사용자 지원 가능한 구조
- Vector DB 교체 가능 (FAISS → Chroma)

### 5.5. 배포

- Docker Compose로 원클릭 실행
- Streamlit Cloud / Render 배포
- CI/CD: GitHub Actions

---

## 6. 기술 스택

| 영역               | 기술                   | 용도                            |
| ------------------ | ---------------------- | ------------------------------- |
| **LLM**            | Claude API             | 질문-답변, 퀴즈 생성, 코드 요약 |
| **Embedding**      | OpenAI Embedding       | 문서 벡터화                     |
| **Vector DB**      | FAISS                  | 유사도 검색 (추후 Chroma 확장)  |
| **Backend**        | FastAPI                | REST API 서버                   |
| **Frontend**       | Streamlit              | 웹 UI (초기), 추후 React 확장   |
| **Database**       | SQLite                 | 학습 기록, 퀴즈 저장            |
| **Integration**    | Notion API, Slack API  | 데이터 연동, 알림               |
| **Infra**          | Docker, GitHub Actions | 컨테이너화, CI/CD               |
| **Code Highlight** | Pygments               | 코드 문법 하이라이팅            |

---

## 7. 데이터 모델

### 7.1. Document (Vector DB)

```python
{
    "page_id": "uuid",
    "title": "FastAPI 학습 정리",
    "content": "...",
    "content_type": "text" | "code",  # NEW
    "language": "python",             # NEW (코드인 경우)
    "embedding": [0.1, 0.2, ...],
    "tags": ["FastAPI", "async"],
    "url": "notion.so/...",
    "created_at": "2024-09-15"
}
```

### 7.2. Learning Log (SQLite)

```sql
CREATE TABLE learning_logs (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    action_type TEXT,  -- 'search', 'quiz', 'code_search'
    content TEXT,
    tags TEXT,
    result TEXT,  -- JSON (quiz 결과 등)
    timestamp DATETIME
);
```

### 7.3. Quiz History

```sql
CREATE TABLE quiz_history (
    id INTEGER PRIMARY KEY,
    quiz_id TEXT,
    question TEXT,
    correct_answer TEXT,
    user_answer TEXT,
    is_correct BOOLEAN,
    difficulty TEXT,
    timestamp DATETIME
);
```

---

## 8. 성공 지표 (MVP 기준)

### 정량 지표

1. **검색 정확도**

   - 목표: 사용자가 원하는 답을 찾는 비율 > 80%
   - 측정: 사용자 피드백 (👍/👎 버튼)

2. **퀴즈 품질**

   - 목표: 생성된 퀴즈가 학습에 도움되는 비율 > 70%
   - 측정: 퀴즈 풀이율, 만족도 설문

3. **사용 빈도**

   - 목표: 주 5회 이상 사용
   - 측정: 학습 로그 기록 횟수

4. **코드 검색 활용도**
   - 목표: 전체 검색 중 코드 검색 비율 > 30%
   - 측정: action_type='code_search' 로그 비율

### 정성 지표

- 포트폴리오 리뷰어 피드백
- 실제 학습 효율성 개선 체감
- 채용 담당자의 기술 스택 이해도

---

## 9. 위험 요소 및 대응

| 위험                      | 영향도 | 대응 방안                        |
| ------------------------- | ------ | -------------------------------- |
| LLM API 비용 초과         | 중     | 무료 티어 모니터링, 캐싱 적용    |
| 검색 품질 낮음            | 고     | Chunk 전략 조정, Re-ranking 적용 |
| 개발 일정 지연            | 고     | 우선순위 관리 (P0 > P1 > P2)     |
| Notion export 데이터 부족 | 중     | 샘플 데이터 생성                 |

---

## 10. 출시 계획

### Phase 1: MVP (10/3)

- RAG 검색 챗봇
- 기본 UI

### Phase 2: 핵심 기능 (10/7)

- 코드 검색 강화
- 퀴즈 생성
- 학습 기록 관리

### Phase 3: 확장 (10/9)

- Slack 리마인더
- 배포 및 문서화

### Phase 4: Future

- React 프론트엔드
- 다중 사용자 지원
- 팀 지식 베이스 모드

---

## 11. 참고 자료

- [LangChain Documentation](https://python.langchain.com/)
- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [Notion API Docs](https://developers.notion.com/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Pygments Documentation](https://pygments.org/)

---

**작성자**: 박병찬
**작성일**: 2025-09-29  
**버전**: 1.0  
**상태**: Draft → Review → **Approved**
