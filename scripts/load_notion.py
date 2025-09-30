from datetime import datetime
import json
from pathlib import Path
import re
from typing import Dict, List, Tuple
import uuid


class NotionLoader:
    """
    Notion export 파일을 파싱하여 JSON으로 변환
    """
    
    def __init__(self, input_dir: str, output_path: str):
        """
        Args:
            input_dir: Notion export 폴더 경로 (data/notion_export/)
            output_path: 출력 JSON 파일 경로 (data/processed/documents.json)
        """
        self.input_dir = Path(input_dir)
        self.output_path = Path(output_path)
    
    def load_all(self) -> List[Dict]:
        """
        input_dir의 모든 마크다운 파일 로드 및 파싱
        
        Returns:
            파싱된 문서 리스트
        """
        documents = []
        
        # .md 파일 찾기
        md_files = list(self.input_dir.glob('**/*.md'))
        
        print(f"📂 총 {len(md_files)}개의 마크다운 파일 발견")
        
        for i, file_path in enumerate(md_files, 1):
            try:
                print(f"📄 [{i}/{len(md_files)}] 파싱 중: {file_path.name}")
                doc = self.parse_markdown(file_path)
                documents.append(doc)
                print(f"  ✅ 완료 - 제목: {doc['title']}, 단어: {doc['word_count']}, 타입: {doc['content_type']}")
            except Exception as e:
                print(f"  ❌ 실패: {e}")
                continue
        
        print(f"\n✨ 총 {len(documents)}개 문서 파싱 완료")
        return documents
    
    def parse_markdown(self, file_path: Path) -> Dict:
        """
        단일 마크다운 파일을 파싱하여 Document 구조로 변환
        
        Args:
            file_path: 마크다운 파일 경로
            
        Returns:
            파싱된 문서 딕셔너리
        """
        # 1. 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        
        # 2. 제목 추출 (원본에서)
        title = self.extract_title(raw_content)

        # 2-1. 제목 줄 제거
        content = self.remove_title_line(raw_content)

        # 3. 참조 섹션 제거
        content = self.remove_references_section(content)
        
        # 4. 이미지 제거
        content = self.remove_images(content)
        
        # 5. 테이블 변환
        content = self.parse_table(content)
        
        # 6. 코드 블록 추출
        content, code_blocks = self.extract_code_blocks(content)
        
        # 7. content_type 판단
        content_type = self.determine_content_type(content, code_blocks)
        
        # 8. 대표 언어 추출
        language = self.get_dominant_language(code_blocks)
        
        # 9. 단어 수 계산
        word_count = len(content.split())
        
        # 10. 메타데이터 생성
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            "page_id": str(uuid.uuid4()),
            "title": title,
            "content": content.strip(),
            "content_type": content_type,
            "language": language,
            "file_path": str(file_path),
            "word_count": word_count,
            "status": "active",
            "created_at": now,
            "updated_at": now,
            "tags": [],
            "url": "",
            "code_blocks": code_blocks
        }

    def extract_title(self, content: str) -> str:
        """
        마크다운에서 첫 번째 # 제목 추출 (첫 번째 \n까지만)
        
        Args:
            content: 마크다운 본문
            
        Returns:
            제목 (없으면 "Untitled")
        """
        # [^\n]+ 는 \n이 아닌 문자들을 매칭 (첫 번째 줄바꿈 전까지)
        pattern = r'^# ([^\n]+)'
        match = re.search(pattern, content, re.MULTILINE)
        
        if match:
            return match.group(1).strip()
        else:
            return "Untitled"
        
    def remove_title_line(self, content: str) -> str:
        """
        첫 번째 # 제목 줄 제거
        
        Args:
            content: 마크다운 본문
            
        Returns:
            제목이 제거된 본문
        """
        # 첫 번째 # 제목 줄을 찾아서 제거
        pattern = r'^# [^\n]+\n+'
        content = re.sub(pattern, '', content, count=1, flags=re.MULTILINE)
        
        return content
    
    def extract_code_blocks(self, content: str) -> Tuple[str, List[Dict]]:
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
            language = match.group(1) or 'plaintext'  # 언어 정보 없으면 plaintext
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

    def parse_table(self, content: str) -> str:
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
    
    def remove_references_section(self, content: str) -> str:
        """
        참조 섹션 제거
        
        ## 참조 또는 ### 참조 이후 모든 내용 제거
        
        Args:
            content: 마크다운 본문
            
        Returns:
            참조 섹션이 제거된 본문
        """
        # ### 참조 또는 ## 참조 패턴
        patterns = [
            r'^###\s*참조.*$.*',  # ### 참조
            r'^##\s*참조.*$.*',   # ## 참조
            r'^###\s*Reference.*$.*',  # 영어 버전
            r'^##\s*Reference.*$.*'
        ]
        
        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
        
        return content


    def remove_images(self, content: str) -> str:
        """
        이미지 마크다운 제거
        
        ![alt text](path) → (제거)
        
        Args:
            content: 마크다운 본문
            
        Returns:
            이미지가 제거된 본문
        """
        # 이미지 패턴: ![...](...)
        pattern = r'!\[([^\]]*)\]\([^\)]+\)'
        content = re.sub(pattern, '', content)
        
        return content

    def determine_content_type(self, content: str, code_blocks: List) -> str:
        """
        content_type 자동 판단 (간단한 휴리스틱)
        """
        if len(code_blocks) == 0:
            return 'text'
        
        word_count = len(content.split())
        
        # 설명이 거의 없으면 code (임계값: 20단어)
        if word_count < 20:
            return 'code'
        
        # 코드 + 설명이 둘 다 있으면 mixed
        return 'mixed'

    def get_dominant_language(self, code_blocks: List) -> str:
        if not code_blocks:
            return None
        
        # 언어별 등장 횟수 카운트 (plaintext 제외)
        language_count = {}
        for block in code_blocks:
            lang = block.get('language', 'plaintext')
            if lang != 'plaintext': # plaintext는 제외
                language_count[lang] = language_count.get(lang, 0) + 1
        
        # 실제 언어가 하나도 없으면 None
        if not language_count:
            return None
        
        # 가장 많이 등장한 언어 반환
        dominant_lang = max(language_count, key=language_count.get)
        
        return dominant_lang

    def save_to_json(self, documents: List[Dict]):
        """
        파싱된 문서를 JSON 파일로 저장
        
        Args:
            documents: 문서 리스트
        """
        # 출력 디렉토리 생성
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # JSON 저장
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(documents, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 저장 완료: {self.output_path}")
        print(f"   - 총 문서 수: {len(documents)}")
        print(f"   - 파일 크기: {self.output_path.stat().st_size / 1024:.2f} KB")

def main():
    """메인 실행 함수"""
    
    # 경로 설정
    input_dir = "../data/notion_export"
    output_path = "../data/processed/documents.json"
    
    # NotionLoader 초기화
    loader = NotionLoader(input_dir, output_path)
    
    # 모든 파일 로드
    documents = loader.load_all()
    
    # JSON으로 저장
    loader.save_to_json(documents)
    
    # 간단한 통계 출력
    print("\n📊 파싱 통계:")
    content_types = {}
    languages = {}
    
    for doc in documents:
        ct = doc['content_type']
        content_types[ct] = content_types.get(ct, 0) + 1
        
        if doc['language']:
            lang = doc['language']
            languages[lang] = languages.get(lang, 0) + 1
    
    print(f"   Content Types: {content_types}")
    print(f"   Languages: {languages}")


if __name__ == "__main__":
    main()