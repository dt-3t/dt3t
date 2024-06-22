"""
适用系统：Windows
功能：提取指定PDF文件的所有文本内容并保存到指定txt文件中。
"""

import fitz

def extract_text_from_pdf(file_path, output_path):
    doc = fitz.open(file_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(full_text)
    return f"文本已保存到 {output_path}"


# 设置文件路径和输出路径
pdf_path = 'example.pdf'  # PDF文件路径
txt_path = 'output.txt'  # 输出TXT文件的路径

result = extract_text_from_pdf(pdf_path, txt_path)
print(result)

