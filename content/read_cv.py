import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pdfplumber

with pdfplumber.open('Phuong-Bui-Tuan-TopCV.vn-220526.72918_1.pdf') as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            print(f"=== PAGE {i+1} ===")
            print(text)
