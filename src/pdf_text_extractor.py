"""
适用系统：Windows
功能：提取指定PDF文件的指定页面文本内容。
"""

import fitz

def extract_text_from_specific_page(file_path, page_number):
    doc = fitz.open(file_path)
    if page_number < 1 or page_number > len(doc):
        return "页面号超出文档范围"
    page = doc[page_number - 1]
    text = page.get_text()
    doc.close()
    return text


# 设置文件路径和要提取的页面号
pdf_path = './example.pdf'  # PDF文件路径
page_number = 3  # 假设我们要提取第3页的内容（从1开始）

extracted_text = extract_text_from_specific_page(pdf_path, page_number)
print(extracted_text)
