import os
import tkinter as tk

def load_icons(icons_dir):
    """
    加载指定目录下的所有图标文件
    :param icons_dir: 图标文件目录
    :return: 图标字典，键为文件名（不含扩展名），值为 PhotoImage 对象
    """
    icons = {}
    try:
        # 获取图标目录的绝对路径
        base_path = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在目录
        icons_path = os.path.join(os.path.dirname(base_path), icons_dir)  # 图标目录路径

        # 遍历 icons_dir 目录下的所有文件
        for filename in os.listdir(icons_path):
            if filename.endswith((".png", ".ico", ".gif")):  # 支持常见图标格式
                icon_name = os.path.splitext(filename)[0]  # 去除扩展名
                icon_path = os.path.join(icons_path, filename)
                icons[icon_name] = tk.PhotoImage(file=icon_path)
    except Exception as e:
        print(f"加载图标失败: {e}")
    return icons


# 示例使用
if __name__ == "__main__":
    # 假设 hwnd 是通过某种方式获取的窗口句柄
    pass
