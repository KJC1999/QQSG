# import ctypes
# import time
# from ctypes import wintypes
#
# # 定义 INPUT 结构体
# class INPUT(ctypes.Structure):
#     _fields_ = [
#         ("type", wintypes.DWORD),
#         ("union", wintypes.BYTE * 24),
#     ]
#
# # 定义 KEYBDINPUT 结构体
# class KEYBDINPUT(ctypes.Structure):
#     _fields_ = [
#         ("wVk", wintypes.WORD),
#         ("wScan", wintypes.WORD),
#         ("dwFlags", wintypes.DWORD),
#         ("time", wintypes.DWORD),
#         ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),  # 修正为指针类型
#     ]
#
# # 定义 SendInput 函数
# SendInput = ctypes.windll.user32.SendInput
# SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
# SendInput.restype = wintypes.UINT
#
# # 定义常量
# INPUT_KEYBOARD = 1
# KEYEVENTF_KEYDOWN = 0x0000
# KEYEVENTF_KEYUP = 0x0002
#
# # 定义 F7 键的虚拟键码
# VK_F7 = 0x76
#
# def send_key(key):
#     """
#     发送按键
#     :param key: 按键的虚拟键码
#     """
#     # 按下按键
#     input_down = INPUT()
#     input_down.type = INPUT_KEYBOARD
#     keybd_input = KEYBDINPUT(key, 0, KEYEVENTF_KEYDOWN, 0, None)  # dwExtraInfo 设置为 None
#     ctypes.memmove(ctypes.byref(input_down.union), ctypes.byref(keybd_input), ctypes.sizeof(keybd_input))
#     SendInput(1, ctypes.byref(input_down), ctypes.sizeof(INPUT))
#
#     # 释放按键
#     input_up = INPUT()
#     input_up.type = INPUT_KEYBOARD
#     keybd_input = KEYBDINPUT(key, 0, KEYEVENTF_KEYUP, 0, None)  # dwExtraInfo 设置为 None
#     ctypes.memmove(ctypes.byref(input_up.union), ctypes.byref(keybd_input), ctypes.sizeof(keybd_input))
#     SendInput(1, ctypes.byref(input_up), ctypes.sizeof(INPUT))
#
# # 发送 F7 键
# time.sleep(3)
# send_key(VK_F7)

import pyautogui

def send_key(key):
    """
    发送按键
    :param key: 按键名称（字符串）或虚拟键码
    """
    if isinstance(key, int):
        # 如果传入的是虚拟键码，转换为按键名称
        key = pyautogui.KEY_NAMES.get(key, None)
        if key is None:
            raise ValueError(f"无效的虚拟键码: {key}")

    # 发送按键
    pyautogui.press(key)

def click(x, y):
    """
    发送鼠标点击事件
    :param x: 点击位置的 X 坐标
    :param y: 点击位置的 Y 坐标
    """
    pyautogui.click(x, y)

# 示例：发送 F7 键
import time
time.sleep(3)
send_key('f7')  # 使用按键名称
# send_key(0x76)  # 使用虚拟键码

# 示例：发送鼠标点击
# click(100, 200)  # 在 (100, 200) 位置点击
