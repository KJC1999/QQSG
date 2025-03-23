# tools/window_utils.py

from tools.win_API import *

def get_qqsg_windows():
    """
    获取所有 qq三国 窗口的句柄（仅用户可见的标签页窗口）
    :return: qq三国 窗口句柄列表
    """
    qqsg_handles = []

    def foreach_window(hwnd, lParam):
        # 检查窗口是否可见
        if not IsWindowVisible(hwnd):
            return True

        # 获取窗口类名
        class_name = ctypes.create_unicode_buffer(256)
        GetClassName(hwnd, class_name, 256)

        # 获取窗口的进程 ID
        pid = ctypes.c_ulong()
        GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

        # 打开进程
        h_process = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
        if h_process:
            # 获取进程的可执行文件路径
            exe_path = ctypes.create_unicode_buffer(512)
            if GetModuleFileNameEx(h_process, None, exe_path, ctypes.sizeof(exe_path)):
                if "qqsg.exe" in exe_path.value.lower():
                    qqsg_handles.append(hwnd)
            CloseHandle(h_process)
        return True

    # 枚举所有窗口
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return qqsg_handles

def get_window_at_position(x, y):
    """
    获取指定屏幕坐标处的窗口句柄
    :param x: 屏幕坐标 X
    :param y: 屏幕坐标 Y
    :return: 窗口句柄（十进制）
    """

    # 定义 POINT 结构体
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    # 创建 POINT 对象
    point = POINT(x, y)
    # 调用 WindowFromPoint 获取窗口句柄
    hwnd = WindowFromPoint(point)
    return hwnd if hwnd else None


if __name__ == '__main__':
    import time
    time.sleep(5)
    get_window_at_position(857,459)
    # get_qqsg_windows()