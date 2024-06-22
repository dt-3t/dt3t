"""
适用系统：Windows
功能：监听系统剪贴板，将新复制的文本内容保存到指定文件夹中，文件名基于当前时间戳。
"""

import os
import time
import pyperclip
import tkinter as tk
from tkinter import messagebox

# 自定义配置
save_path = './'  # 修改为你想要保存文件的文件夹路径
show_messagebox = True  # 是否显示保存成功弹窗
time_threshold = 0.2  # 剪贴板监听间隔时间
file_prefix = 'clipboard_'  # 保存文件名前缀

root = tk.Tk()
root.withdraw()
save_path = os.path.abspath(save_path)
if not os.path.exists(save_path):
    os.makedirs(save_path)

def save_text_to_file(text, folder, show_messagebox, file_prefix):
    text = text.replace('\r\n', '\n').strip()
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    filename = file_prefix + f'{timestamp}.txt'
    file_path = os.path.join(folder, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"内容已保存至：{file_path}")
    if not show_messagebox:
        return
    root.attributes('-topmost', True)
    messagebox.showinfo("保存成功", f"复制的内容已保存至：{file_path}")
    root.attributes('-topmost', False)

last_text = pyperclip.paste()

print("开始监听剪贴板...")
while True:
    time.sleep(time_threshold)
    current_text = pyperclip.paste()
    if current_text != last_text:
        last_text = current_text
        save_text_to_file(current_text, save_path, show_messagebox, file_prefix)
