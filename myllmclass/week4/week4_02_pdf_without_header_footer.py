import pymupdf
import os

pdf_file_path = "./transformer_paper.pdf"
doc = pymupdf.open(pdf_file_path) # PDF 파일을 열어 문서 객체(doc)로 생성

header_height = 80 # 페이지 상단(헤더) 영역 높이, 필요시 직접 조정
footer_height = 80 # 페이지 하단(푸터) 영역 높이, 필요시 직접 조정

full_text = ''

for page in doc: # 문서 객체(doc)의 각 페이지를 반복
    rect = page.rect # 현재 페이지의 사이즈(Rect 객체, width/height)

    # 상단 header 영역 텍스트 추출(clip: 좌상단에서 header_height까지)
    header = page.get_text(clip = (0, 0, rect.width, header_height))
    # 하단 footer 영역 텍스트 추출(clip: 좌하단에서 footer_height 범위)
    footer = page.get_text(clip = (0, rect.height - footer_height, rect.width, rect.height))
    # 중앙 본문 영역(헤더/푸터 제외) 텍스트 추출
    text = page.get_text(clip = (0, header_height, rect.width, rect.height - footer_height))

    # 추출한 본문 텍스트를 덧붙이면서, 페이지 구분선을 추가함
    full_text += text + '\n------------------------------\n'

# PDF 파일 이름만 추출(ex: example.pdf → example)
pdf_file_name = os.path.basename(pdf_file_path)
pdf_file_name = os.path.splitext(pdf_file_name)[0]

# 저장할 TXT 파일 경로(같은 이름에 _with_preprocessing 추가, .txt 확장자)
txt_file_path = f"./{pdf_file_name}_with_preprocessing.txt"
# 전체 텍스트를 TXT 파일로 저장(UTF-8 인코딩)
with open(txt_file_path, 'w', encoding = 'utf-8') as f:
    f.write(full_text) # 누적된 전체 텍스트를 파일에 기록

# 결과 확인용: 생성된 파일 경로 및 현재 폴더의 파일 목록 출력
print(f"저장된 파일 경로: {txt_file_path}")
print(f"현재 폴더 파일 목록: {os.listdir('.')}")
