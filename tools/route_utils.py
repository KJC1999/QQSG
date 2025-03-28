import cv2
import time
import shutil
import threading

from tools.public import *
from tools.win_API import *
from win32con import *
from PIL import ImageGrab
from datetime import datetime

# 定义方向键映射
key_mapping = {
    "left": 0x25,  # 左箭头
    "right": 0x27,  # 右箭头
    "up": 0x26,     # 上箭头
    "down": 0x28,   # 下箭头
}

# 定义每条线路的方向键顺序
route_directions = {
    2: ["down"],
    3: ["down","down"],
    4: ["down", "down", "down"],  # 或者 ["down", "right"]
    5: ["down", "down", "down", "down"],
    6: ["down", "down", "down", "down", "down"],
    7: ["down", "down", "down", "down", "down", "down"],
    8: ["down", "down", "down", "down", "down", "down", "down"],
    9: ["down", "down", "down", "down", "down", "down", "down", "down"],
    10: ["down", "down", "down", "down", "down", "down", "down", "down", "down"],
    11: ["down", "down", "down", "down", "down", "down", "down", "down", "down", "down"],
    12: ["down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down"],
    13: ["down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down"],
    14: ["down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down"],
    15: ["down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down"],
    16: ["down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down", "down"]
}

def get_window_title(hwnd):
    """
    获取指定窗口句柄的标题
    :param hwnd: 窗口句柄
    :return: 窗口标题（字符串）
    """
    while hwnd:
        # 获取窗口标题的长度
        length = GetWindowTextLength(hwnd)
        if length > 0:
            # 创建缓冲区
            buffer = ctypes.create_unicode_buffer(length + 1)
            # 获取窗口标题
            GetWindowText(hwnd, buffer, length + 1)
            return buffer.value
        # 如果没有标题，查找父窗口
        hwnd = GetParent(hwnd)
    # 如果所有父窗口都没有标题，返回空字符串
    return ""

def send_shortcut(hwnd, key, modifier=VK_CONTROL):
    """
    向指定窗口句柄发送【快捷键】组合
    :param hwnd: 窗口句柄
    :param key: 快捷键的主键（如 VK_S）
    :param modifier: 修饰键（如 VK_CONTROL）
    """
    # 发送修饰键按下（如 Ctrl）
    PostMessage(hwnd, WM_KEYDOWN, modifier, 0)
    # 发送主键按下（如 S）
    PostMessage(hwnd, WM_KEYDOWN, key, 0)
    # 发送主键释放（如 S）
    PostMessage(hwnd, WM_KEYUP, key, 0)
    # 发送修饰键释放（如 Ctrl）
    PostMessage(hwnd, WM_KEYUP, modifier, 0)

def capture_window(hwnd, scal):
    """
    截图指定窗口并保存
    :param scal: 当前系统的缩放比
    :param hwnd: 窗口句柄
    :return: 截图文件路径
    """

    # 获取窗口位置和大小
    rect = wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    left, top, right, bottom = rect.left, rect.top, rect.right, rect.bottom
    # 获取系统缩放比例
    scaling = scal
    # 根据缩放比例调整窗口坐标和大小
    left = int(left * scaling)
    top = int(top * scaling)
    right = int(right * scaling)
    bottom = int(bottom * scaling)
    # 截图
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    # 创建保存目录
    save_dir = os.path.join("images/temp", str(hwnd))
    os.makedirs(save_dir, exist_ok=True)
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    screenshot_path = os.path.join(save_dir, f"{hwnd}_{timestamp}.png")
    # 保存截图
    screenshot.save(screenshot_path)
    return screenshot_path

def locate_image_in_window(screenshot_path, template_path, scal):
    """
    在窗口截图中定位模板图片的位置
    :param screenshot_path: 窗口截图路径
    :param template_path: 模板图片路径
    :param scal: 缩放比例
    :return: 模板图片在窗口中的中心坐标 (x, y)，如果未找到返回 None
    """
    # 加载截图和模板图片
    screenshot = cv2.imread(screenshot_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # 获取模板图片的宽度和高度
    template_height, template_width = template.shape

    # 模板匹配
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # 如果匹配度高于阈值，返回中心坐标
    if max_val > 0.9:  # 阈值可以根据实际情况调整
        # 计算左上角坐标
        top_left_x = max_loc[0]
        top_left_y = max_loc[1]

        # 计算中心坐标
        center_x = int((top_left_x + template_width / 2) / scal)
        center_y = int((top_left_y + template_height / 2) / scal)
        return center_x, center_y - 10
    return None


def choose_route(hwnd, target_route):
    """
    选择目标线路
    :param hwnd: 句柄
    :param target_route: 目标线路（1-16）
    """
    directions = route_directions.get(target_route, [])

    # 依次发送方向键
    for direction in directions:
        key = key_mapping.get(direction)
        if key:
            send_key(hwnd, key)
            time.sleep(0.1)  # 每次按键后等待 0.1 秒


class RouteThread(threading.Thread):
    def __init__(self, hwnd, stop_event, callback, route_number):
        super().__init__()
        self.hwnd = hwnd  # 窗口句柄
        self.stop_event = stop_event  # 用于中断线程的事件
        self.callback = callback  # 回调函数，用于通知主线程
        self.counter = 0  # 计数器
        self.scal = get_system_scaling()
        self.route_number = route_number
        self.choose_route_pos = None

    def run(self):
        """
        完整的换线过程：
        1、发送key->F7
        2、定位【选择线路】，记录坐标，触发左键单击操作
        3、定位线路坐标，记录坐标，触发左键双击操作
        """
        while not self.stop_event.is_set():
            try:
                # 1. 前置窗口
                SetForegroundWindow(self.hwnd)
                # 2. 触发 F7 按键
                send_key(self.hwnd, VK_F7)
                time.sleep(0.5)
                if self.choose_route_pos is None:
                    # 3. 截图并保存
                    screenshot_path = capture_window(self.hwnd, self.scal)
                    # 4. 定位 choose_route.png 在窗口中的位置
                    self.choose_route_pos = locate_image_in_window(screenshot_path, "images/targets/choose_route.png", self.scal)
                    self.mix_operation()
                    if self.check():
                        break
                else:
                    self.mix_operation()
                    if self.check():
                        break
                time.sleep(1)
            except Exception as e:
                # 触发异常前，先触发ESC按键，恢复环境
                send_key(self.hwnd, VK_ESCAPE)
                print(f"执行过程中发生错误: {e}")
                temp_dir = "images/temp"
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                break
        # 调用回调函数
        self.callback()

    def mix_operation(self):
        # 5. 触发单击操作
        click_window(self.hwnd, self.choose_route_pos[0], self.choose_route_pos[1])
        # 6. 触发线路选择方法
        choose_route(self.hwnd, self.route_number)
        # 7. 触发回车
        send_key(self.hwnd, VK_RETURN)

    def check(self):
        # 8. 检查标题来判断是否换线成功
        title = get_window_title(self.hwnd)
        if str(self.route_number) + "线" in title:
            temp_dir = "images/temp"
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            return True
        else:
            return False

if __name__ == '__main__':
    # send_key(918786, VK_F5)
    # time.sleep(3)
    # capture_window(67412)
    # get_window_title(3476046)
    # send_key(3476046, VK_F7)
    time.sleep(2)
    send_key(3476046, VK_RETURN)

