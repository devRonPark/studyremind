# test_extract_code_blocks.py

import re
from typing import Tuple, List, Dict

def extract_code_blocks(content: str) -> Tuple[str, List[Dict]]:
    """
    코드 블록 추출 및 플레이스홀더로 치환
    
    Args:
        content: 마크다운 본문
        
    Returns:
        (치환된 본문, 코드 블록 리스트)
    """
    code_blocks = []
    
    # 정규식: ```language\n...``` 패턴
    pattern = r'```(\w*)\n(.*?)```'
    
    def replace_with_placeholder(match):
        language = match.group(1) or 'plaintext'
        code = match.group(2).strip()
        
        block_id = f"CODE_BLOCK_{len(code_blocks)}"
        code_blocks.append({
            "id": block_id,
            "language": language,
            "code": code
        })
        
        return f"[{block_id}]"
    
    # 코드 블록을 플레이스홀더로 치환
    modified_content = re.sub(pattern, replace_with_placeholder, content, flags=re.DOTALL)
    
    return modified_content, code_blocks


# 테스트 케이스들
def test_case_1():
    """언어 정보가 있는 코드 블록"""
    content = """Redis 캐싱 예제:

```python
client = redis.Redis()
client.setex('key', 3600, 'value')
```

위 코드는 TTL을 설정합니다."""

    modified, blocks = extract_code_blocks(content)
    
    print("=" * 60)
    print("테스트 1: 언어 정보가 있는 코드 블록")
    print("=" * 60)
    print("\n[변환된 본문]")
    print(modified)
    print("\n[추출된 코드 블록]")
    for block in blocks:
        print(f"  ID: {block['id']}")
        print(f"  언어: {block['language']}")
        print(f"  코드: {block['code'][:50]}...")
    print()


def test_case_2():
    """언어 정보가 없는 코드 블록"""
    content = """셸 스크립트:

```
echo "hello world"
ls -la
```

간단한 명령어입니다."""

    modified, blocks = extract_code_blocks(content)
    
    print("=" * 60)
    print("테스트 2: 언어 정보가 없는 코드 블록")
    print("=" * 60)
    print("\n[변환된 본문]")
    print(modified)
    print("\n[추출된 코드 블록]")
    for block in blocks:
        print(f"  ID: {block['id']}")
        print(f"  언어: {block['language']}")
        print(f"  코드: {block['code']}")
    print()


def test_case_3():
    """여러 개의 코드 블록"""
    content = """Python 예제:

```python
def hello():
    print("world")
```

그리고 JavaScript 예제:

```javascript
const hello = () => {
    console.log("world");
}
```

마지막으로 SQL:

```sql
SELECT * FROM users;
```

총 3개의 코드 블록입니다."""

    modified, blocks = extract_code_blocks(content)
    
    print("=" * 60)
    print("테스트 3: 여러 개의 코드 블록")
    print("=" * 60)
    print("\n[변환된 본문]")
    print(modified)
    print("\n[추출된 코드 블록]")
    for i, block in enumerate(blocks, 1):
        print(f"\n  #{i}")
        print(f"  ID: {block['id']}")
        print(f"  언어: {block['language']}")
        print(f"  코드: {block['code'][:30]}...")
    print()


def test_case_4():
    """인라인 코드는 유지되는지 확인"""
    content = """Redis 명령어 `SET key value`는 기본 저장입니다.

```python
client.set('key', 'value')
```

인라인 코드 `GET key`도 있습니다."""

    modified, blocks = extract_code_blocks(content)
    
    print("=" * 60)
    print("테스트 4: 인라인 코드 유지 확인")
    print("=" * 60)
    print("\n[변환된 본문]")
    print(modified)
    print("\n인라인 코드가 그대로 유지되었나요?")
    print(f"  `SET key value` 존재: {'SET key value' in modified}")
    print(f"  `GET key` 존재: {'GET key' in modified}")
    print("\n[추출된 코드 블록]")
    for block in blocks:
        print(f"  ID: {block['id']}")
        print(f"  언어: {block['language']}")
    print()


if __name__ == "__main__":
    print("\n🧪 extract_code_blocks() 함수 테스트 시작\n")
    
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    
    print("=" * 60)
    print("✅ 모든 테스트 완료!")
    print("=" * 60)