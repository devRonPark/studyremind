# FastAPI 트러블슈팅: ModuleNotFoundError 해결하기

## 🐛 문제 상황

FastAPI 프로젝트를 uvicorn으로 실행할 때 `ModuleNotFoundError`가 발생하는 경우가 있습니다.

```bash
# backend 폴더에서 실행
cd backend
uvicorn backend.app.main:app --reload

# 에러 발생
ModuleNotFoundError: No module named 'backend'
```

**프로젝트 구조:**

```
/studyremind
  /backend
    /app
      main.py
      /core
      /models
      /api
```

---

## 🔍 원인 분석

uvicorn은 **현재 작업 디렉토리(cwd)**를 Python 모듈 검색 경로의 시작점으로 사용합니다.

### 실패한 경우:

```bash
cd /path/to/studyremind/backend  # ← 여기가 현재 위치
uvicorn backend.app.main:app     # ← backend 폴더를 또 찾으려고 시도
```

**uvicorn이 찾는 경로:**

- 현재 위치: `/path/to/studyremind/backend`
- 찾으려는 파일: `backend/app/main.py`
- 실제 존재하는 경로: `/path/to/studyremind/backend/backend/app/main.py` ❌

실제 파일은 `/path/to/studyremind/backend/app/main.py`에 있는데, `backend`를 한 번 더 찾으려고 하니 에러가 발생합니다.

---

## ✅ 해결 방법

### 방법 1: 올바른 모듈 경로 사용 (권장)

**현재 위치에 맞는 상대 경로를 사용하세요.**

```bash
# backend 폴더 안에서 실행할 때
cd backend
uvicorn app.main:app --reload  # ✅ 성공

# studyremind 루트에서 실행할 때
cd studyremind
uvicorn backend.app.main:app --reload  # ✅ 성공
```

### 방법 2: PYTHONPATH 설정

프로젝트 루트를 PYTHONPATH에 추가하는 방법도 있습니다.

```bash
# Linux/Mac
export PYTHONPATH="${PYTHONPATH}:/path/to/studyremind"
uvicorn backend.app.main:app --reload

# Windows
set PYTHONPATH=%PYTHONPATH%;C:\path\to\studyremind
uvicorn backend.app.main:app --reload
```

---

## 💡 핵심 개념

### uvicorn 모듈 경로 규칙

uvicorn의 모듈 경로는 다음과 같이 해석됩니다:

```bash
uvicorn [모듈.경로.파일명:FastAPI객체명]
```

**예시:**

- `app.main:app` → `./app/main.py` 파일의 `app` 객체
- `backend.app.main:app` → `./backend/app/main.py` 파일의 `app` 객체

**경로 규칙:**

1. 첫 번째 요소(`app` or `backend`)는 **현재 디렉토리 기준**으로 찾습니다
2. `.`는 폴더 구분자로 해석됩니다
3. 마지막 `:` 뒤는 Python 객체명입니다

---

## 🎯 베스트 프랙티스

### 1. 일관된 실행 위치 유지

프로젝트별로 실행 위치를 정하고 문서화하세요.

```bash
# 프로젝트 README.md에 명시
## 개발 서버 실행

\`\`\`bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
\`\`\`
```

### 2. 스크립트 파일 작성

실행 명령어를 스크립트로 만들어두면 실수를 방지할 수 있습니다.

```bash
# backend/run.sh
#!/bin/bash
cd "$(dirname "$0")"  # 스크립트 위치로 이동
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

```bash
chmod +x backend/run.sh
./backend/run.sh
```

### 3. Makefile 활용

```makefile
# Makefile
.PHONY: dev

dev:
	cd backend && uvicorn app.main:app --reload
```

```bash
make dev
```

### 4. Docker 사용 시

Dockerfile에서 WORKDIR을 명확히 지정하세요.

```dockerfile
FROM python:3.10

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🔧 디버깅 팁

### 현재 Python 경로 확인

```python
# test_path.py
import sys
print("Python 모듈 검색 경로:")
for path in sys.path:
    print(f"  {path}")
```

```bash
python test_path.py
```

### uvicorn 로그 상세히 보기

```bash
uvicorn app.main:app --reload --log-level debug
```

---

## 📚 관련 리소스

- [Uvicorn 공식 문서](https://www.uvicorn.org/)
- [FastAPI 배포 가이드](https://fastapi.tiangolo.com/deployment/)
- [Python 모듈 시스템 이해하기](https://docs.python.org/3/tutorial/modules.html)

---

## 🎓 배운 점 정리

1. **uvicorn은 현재 작업 디렉토리를 기준으로 모듈을 찾는다**
2. **파일 시스템 경로 ≠ Python 모듈 경로**
3. **실행 위치에 따라 모듈 경로를 조정해야 한다**
4. **프로젝트 구조와 실행 방법을 문서화하는 것이 중요하다**

---

**작성일**: 2025-09-29  
**태그**: `#FastAPI` `#Uvicorn` `#Python` `#Troubleshooting` `#ModuleNotFoundError`
