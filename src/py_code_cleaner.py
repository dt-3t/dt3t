# 去除Python代码注释

import re

def remove_comments(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.readlines()

    new_code = []
    in_block_comment = False
    for line in code:
        if '"""' in line or "'''" in line:
            in_block_comment = not in_block_comment
            new_code.append('\n')
        elif not in_block_comment:
            line = re.sub(r"#.*", "", line)
            new_code.append(line)
        else:
            new_code.append('\n')

    new_file_path = file_path.replace('.py', '_nocomments.py')
    with open(new_file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_code)

    print(f"注释已移除，新文件保存在：{new_file_path}")


def compress_empty_lines(file_path):
    """
    从指定的Python代码文件中将连续的多行空行压缩为一行空行。
    参数:
    - file_path: str，原始Python代码文件的路径。
    功能:
    - 读取原始文件，将连续的空行压缩为单一空行，然后保存修改后的代码。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    previous_line_empty = False

    for line in lines:
        current_line_empty = not line.strip()

        if current_line_empty and not previous_line_empty:
            new_lines.append(line)

        if not current_line_empty:
            new_lines.append(line)

        previous_line_empty = current_line_empty

    new_file_path = file_path.replace('.py', '_compressed.py')
    with open(new_file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

    print(f"多行空行已压缩，新文件保存在：{new_file_path}")


remove_comments(r'./main.py')  # 你期望被处理的文件路径
compress_empty_lines(r'./main_nocomments.py')