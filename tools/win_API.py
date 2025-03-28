import ctypes
from ctypes import wintypes

# 定义 Windows API 函数
# 用于 get_qqsg_windows 方法
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
GetParent = ctypes.windll.user32.GetParent
OpenProcess = ctypes.windll.kernel32.OpenProcess
CloseHandle = ctypes.windll.kernel32.CloseHandle
GetModuleFileNameEx = ctypes.windll.psapi.GetModuleFileNameExW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
GetClassName = ctypes.windll.user32.GetClassNameW
WindowFromPoint = ctypes.windll.user32.WindowFromPoint
SendMessage = ctypes.windll.user32.SendMessageW
PostMessage = ctypes.windll.user32.PostMessageW
SetForegroundWindow = ctypes.windll.user32.SetForegroundWindow
GetDC = ctypes.windll.user32.GetDC
ReleaseDC = ctypes.windll.user32.ReleaseDC
GetDeviceCaps = ctypes.windll.gdi32.GetDeviceCaps
GetSystemMetrics = ctypes.windll.user32.GetSystemMetrics
GetWindowRect = ctypes.windll.user32.GetWindowRect

# 常量
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
VK_CONTROL = 0x11
VK_S = 0x53
VK_F5 = 0x74  # F5 的虚拟键码
VK_F7 = 0x76 # F7 的虚拟键码
VK_RETURN = 0x0D  # 回车键的虚拟键码
VK_ESCAPE = 0x1B # ESC 的虚拟键码
WM_LBUTTONDOWN = 0x0201  # 鼠标左键按下
WM_LBUTTONUP = 0x0202    # 鼠标左键释放
DESKTOPHORZRES = 118  # 真实屏幕宽度
SM_CXSCREEN = 0  # 缩放后的屏幕宽度