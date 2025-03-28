import os
import tkinter as tk

from tools.win_API import *

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

def send_key(hwnd, key):
    """
    向指定窗口句柄发送【单个按键】
    :param hwnd: 窗口句柄
    :param key: 按键的虚拟键码（如 VK_F7）
    """
    PostMessage(hwnd, WM_KEYDOWN, key, 0)
    PostMessage(hwnd, WM_KEYUP, key, 0)

def get_system_scaling():
    # 获取屏幕设备上下文
    hDC = GetDC(0)
    # 获取屏幕的真实宽度和缩放后的宽度
    real_w = GetDeviceCaps(hDC, DESKTOPHORZRES)
    apparent_w = GetSystemMetrics(SM_CXSCREEN)
    # 计算缩放比
    scale = real_w / apparent_w
    return scale

def click_window(hwnd, x, y):
    """
    在指定窗口内触发单击操作
    :param hwnd: 窗口句柄
    :param x: 单击位置的 X 坐标（相对于窗口客户区）
    :param y: 单击位置的 Y 坐标（相对于窗口客户区）
    """
    # 将坐标打包为 lParam
    lparam = y << 16 | x
    # 发送鼠标左键按下消息
    PostMessage(hwnd, WM_LBUTTONDOWN, 1, lparam)  # wParam=1 表示左键
    # 发送鼠标左键释放消息
    PostMessage(hwnd, WM_LBUTTONUP, 0, lparam)  # wParam=0 表示无按键

def locate_position_in_hwnd(hwnd, x, y):
    if hwnd:
        # 计算相对坐标
        rect = wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        rel_x = x - rect.left
        rel_y = y - rect.top
        #返回
        click_position = (rel_x, rel_y)
        return click_position
    else:
        return False

# 示例使用
if __name__ == "__main__":
    # 假设 hwnd 是通过某种方式获取的窗口句柄
    import time
    time.sleep(2)
    click_window(657124, 616 , 84)
    pass
