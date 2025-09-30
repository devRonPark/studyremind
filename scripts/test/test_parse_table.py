# test_parse_table.py

import re

def parse_table(content: str) -> str:
    """
    마크다운 테이블을 구조화된 텍스트로 변환
    
    Args:
        content: 마크다운 본문
        
    Returns:
        테이블이 변환된 본문
    """
    # 테이블 패턴: | header1 | header2 | ... |
    #             |---------|---------|-----|
    #             | value1  | value2  | ... |
    
    # 테이블 전체를 찾는 정규식
    table_pattern = r'\|(.+)\|\n\|[-:\s\|]+\|\n((?:\|.+\|\n?)+)'
    
    def replace_table(match):
        header_line = match.group(1)
        rows_text = match.group(2)
        
        # 헤더 파싱
        headers = [h.strip() for h in header_line.split('|') if h.strip()]
        
        # 각 행 파싱
        rows = []
        for row_line in rows_text.strip().split('\n'):
            if not row_line.strip():
                continue
            values = [v.strip() for v in row_line.split('|') if v.strip()]
            
            # 헤더 개수와 값 개수가 맞지 않으면 스킵
            if len(values) != len(headers):
                continue
            
            # "헤더: 값" 형태로 변환
            row_text = ', '.join([f"{h}: {v}" for h, v in zip(headers, values)])
            rows.append(row_text)
        
        # 각 행을 줄바꿈으로 연결
        return '\n'.join(rows)
    
    # 테이블을 변환된 텍스트로 치환
    modified_content = re.sub(table_pattern, replace_table, content)
    
    return modified_content


# 테스트 케이스들
def test_case_1():
    """기본 테이블 변환"""
    content = """HTTP 메서드 정리:

| 메서드 | 설명 | 예시 |
|--------|------|------|
| GET | 조회 | /users |
| POST | 생성 | /users |
| PUT | 수정 | /users/1 |

위 표는 REST API 메서드입니다."""

    result = parse_table(content)
    
    print("=" * 60)
    print("테스트 1: 기본 테이블 변환")
    print("=" * 60)
    print("\n[원본]")
    print(content)
    print("\n[변환 결과]")
    print(result)
    print()


def test_case_2():
    """2열 테이블"""
    content = """Redis 명령어:

| 명령어 | 설명 |
|--------|------|
| SET | 값 저장 |
| GET | 값 조회 |
| DEL | 값 삭제 |

간단한 CRUD 명령어입니다."""

    result = parse_table(content)
    
    print("=" * 60)
    print("테스트 2: 2열 테이블")
    print("=" * 60)
    print("\n[원본]")
    print(content)
    print("\n[변환 결과]")
    print(result)
    print()


def test_case_3():
    """여러 개의 테이블"""
    content = """첫 번째 테이블:

| 이름 | 나이 |
|------|------|
| 철수 | 25 |
| 영희 | 30 |

두 번째 테이블:

| 과일 | 가격 |
|------|------|
| 사과 | 1000 |
| 바나나 | 2000 |

총 2개의 테이블입니다."""

    result = parse_table(content)
    
    print("=" * 60)
    print("테스트 3: 여러 개의 테이블")
    print("=" * 60)
    print("\n[원본]")
    print(content)
    print("\n[변환 결과]")
    print(result)
    print()


def test_case_4():
    """테이블이 없는 경우"""
    content = """이 문서에는 테이블이 없습니다.

일반 텍스트만 있습니다.
코드나 다른 내용들..."""

    result = parse_table(content)
    
    print("=" * 60)
    print("테스트 4: 테이블이 없는 경우")
    print("=" * 60)
    print("\n[원본]")
    print(content)
    print("\n[변환 결과]")
    print(result)
    print("\n변경 사항 없음:", content == result)
    print()


def test_case_5():
    """복잡한 테이블 (4개 열)"""
    content = """데이터베이스 비교:

| DB | 타입 | 속도 | 용도 |
|----|------|------|------|
| MySQL | RDBMS | 중간 | 일반 웹 |
| Redis | NoSQL | 빠름 | 캐싱 |
| MongoDB | NoSQL | 중간 | 문서 저장 |

다양한 데이터베이스입니다."""

    result = parse_table(content)
    
    print("=" * 60)
    print("테스트 5: 복잡한 테이블 (4개 열)")
    print("=" * 60)
    print("\n[원본]")
    print(content)
    print("\n[변환 결과]")
    print(result)
    print()


if __name__ == "__main__":
    print("\n🧪 parse_table() 함수 테스트 시작\n")
    
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    test_case_5()
    
    print("=" * 60)
    print("✅ 모든 테스트 완료!")
    print("=" * 60)