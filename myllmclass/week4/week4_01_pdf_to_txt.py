import pymupdf
import os

pdf_file_path = "./transformer_paper.pdf"
doc = pymupdf.open(pdf_file_path) # PDF 파일을 열어 문서 객체(doc)로 생성

full_text = ''

for page in doc: # 문서 객체(doc)의 각 페이지를 반복
    text = page.get_text() # 해당 페이지의 텍스트 추출
    full_text += text # 현재 페이지 텍스트를 전체 텍스트에 이어붙임

# PDF 파일 이름만 추출(ex: example.pdf → example)
pdf_file_name = os.path.basename(pdf_file_path)
pdf_file_name = os.path.splitext(pdf_file_name)[0]

# 저장할 TXT 파일 경로(동일 이름으로 .txt 확장자)
txt_file_path = f"./{pdf_file_name}.txt"
# 전체 텍스트를 TXT 파일로 저장(UTF-8 인코딩)
with open(txt_file_path, 'w', encoding = 'utf-8') as f:
    f.write(full_text) # 누적된 전체 텍스트를 파일에 기록

# 결과 확인용: 생성된 파일 경로 및 현재 폴더의 파일 목록 출력
print(f"저장된 파일 경로: {txt_file_path}")
print(f"현재 폴더 파일 목록: {os.listdir('.')}")
