import threading
import time

from tools.public import *

class ClickerThread(threading.Thread):
    def __init__(self, hwnd, stop_event, callback, x, y):
        super().__init__()
        self.hwnd = hwnd  # 窗口句柄
        self.stop_event = stop_event  # 用于中断线程的事件
        self.callback = callback  # 回调函数，用于通知主线程
        self.scal = get_system_scaling()
        self.choose_route_pos = None
        self.click_x = x
        self.click_y = y
        print("获取到的scal是：", self.scal)
        print(f"获取到的坐标({self.click_x},{self.click_y})")

    def run(self):
        while not self.stop_event.is_set():
            try:
                click_window(self.hwnd, self.click_x, self.click_y)
                time.sleep(0.1)
            except Exception as e:
                print(f"执行过程中发生错误: {e}")
                break
        # 调用回调函数
        self.callback()