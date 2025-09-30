# test_extract_title.py

import re

def extract_title(content: str) -> str:
    """
    마크다운에서 첫 번째 # 제목 추출
    
    Args:
        content: 마크다운 본문
        
    Returns:
        제목 (없으면 "Untitled")
    """
    # 첫 번째 # 로 시작하는 줄 찾기 (##, ### 등은 제외)
    pattern = r'^# (.+)$'
    match = re.search(pattern, content, re.MULTILINE)
    
    if match:
        return match.group(1).strip()
    else:
        return "Untitled"


# 테스트 케이스들
def test_case_1():
    """일반적인 제목"""
    content = """# OSI 7계층

## OSI 7계층이란?

본문 내용..."""

    result = extract_title(content)
    
    print("=" * 60)
    print("테스트 1: 일반적인 제목")
    print("=" * 60)
    print(f"추출된 제목: '{result}'")
    print(f"예상: 'OSI 7계층'")
    print(f"통과: {result == 'OSI 7계층'}")
    print()


def test_case_2():
    """제목이 없는 경우"""
    content = """본문부터 시작하는 문서

## 소제목만 있음

내용..."""

    result = extract_title(content)
    
    print("=" * 60)
    print("테스트 2: 제목이 없는 경우")
    print("=" * 60)
    print(f"추출된 제목: '{result}'")
    print(f"예상: 'Untitled'")
    print(f"통과: {result == 'Untitled'}")
    print()


def test_case_3():
    """## 소제목만 있고 # 제목이 없는 경우"""
    content = """## 소제목

### 더 작은 제목

본문..."""

    result = extract_title(content)
    
    print("=" * 60)
    print("테스트 3: ## 소제목만 있는 경우")
    print("=" * 60)
    print(f"추출된 제목: '{result}'")
    print(f"예상: 'Untitled' (# 제목만 추출)")
    print(f"통과: {result == 'Untitled'}")
    print()


def test_case_4():
    """제목에 특수문자가 있는 경우"""
    content = """# FastAPI: 비동기 처리 & 성능 최적화 (2024)

본문..."""

    result = extract_title(content)
    
    print("=" * 60)
    print("테스트 4: 특수문자 포함 제목")
    print("=" * 60)
    print(f"추출된 제목: '{result}'")
    print(f"예상: 'FastAPI: 비동기 처리 & 성능 최적화 (2024)'")
    print(f"통과: {result == 'FastAPI: 비동기 처리 & 성능 최적화 (2024)'}")
    print()


def test_case_5():
    """여러 # 제목이 있는 경우 (첫 번째만 추출)"""
    content = """# 첫 번째 제목

본문 내용...

# 두 번째 제목

더 많은 내용..."""

    result = extract_title(content)
    
    print("=" * 60)
    print("테스트 5: 여러 # 제목 중 첫 번째만")
    print("=" * 60)
    print(f"추출된 제목: '{result}'")
    print(f"예상: '첫 번째 제목'")
    print(f"통과: {result == '첫 번째 제목'}")
    print()


def test_case_6():
    """제목 앞뒤 공백 제거 확인"""
    content = """#   공백이 많은 제목   

본문..."""

    result = extract_title(content)
    
    print("=" * 60)
    print("테스트 6: 제목 공백 제거")
    print("=" * 60)
    print(f"추출된 제목: '{result}'")
    print(f"예상: '공백이 많은 제목'")
    print(f"통과: {result == '공백이 많은 제목'}")
    print()


if __name__ == "__main__":
    print("\n🧪 extract_title() 함수 테스트 시작\n")
    
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    test_case_5()
    test_case_6()
    
    print("=" * 60)
    print("✅ 모든 테스트 완료!")
    print("=" * 60)