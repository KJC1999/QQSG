from tools.route_utils import *
from tools.auto_clicker import *
from tkinter import ttk, messagebox
from tools.window_utils import *

# 主窗口
class ToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QQSG小助手")
        self.root.geometry("600x700")

        # 创建顶部Tab
        self.tab_control = ttk.Notebook(root)

        # 添加各个功能Tab
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab4 = ttk.Frame(self.tab_control)
        self.tab5 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text="换线")
        self.tab_control.add(self.tab2, text="喊话")
        self.tab_control.add(self.tab3, text="卡键")
        self.tab_control.add(self.tab4, text="同步")
        self.tab_control.add(self.tab5, text="连点")
        self.tab_control.pack(expand=1, fill="both")

        # 初始化各类参数
        self.window_handles = {}
        self.threads = {}  # 存储线程对象
        self.stop_events = {}  # 存储线程中断事件
        self.locate_logo_buttons = []  # 存储定位按钮
        self.logo_labels = []  # 存储展示 Label
        self.start_buttons = []  # 存储开始按钮
        self.route_menu = []  # 存储下拉列表
        self.clicker_position = None  # 存储点击坐标(x,y)

        # 初始化所有图标
        self.icons = load_icons("images/icons")

        # 初始化各个功能界面
        self.init_tab1()
        self.init_tab2()
        self.init_tab3()
        self.init_tab4()
        self.init_tab5()

    # 换线功能界面
    def init_tab1(self):
        # 左上角：获取窗口按钮
        get_window_button = ttk.Button(self.tab1, text="获取窗口", command=self.get_window)
        get_window_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # 创建 5 个框
        for i in range(5):
            frame = ttk.LabelFrame(self.tab1, text=f"窗口 {i + 1}")
            frame.grid(row=i + 1, column=0, columnspan=4, padx=10, pady=5, sticky="w")

            # 定位 Logo 按钮（使用图标）
            if "locate_icon" in self.icons:  # 假设图标名为 locate_icon
                locate_logo_button = tk.Button(
                    frame,
                    image=self.icons["locate_icon"],
                    bd=0,  # 无边框
                    relief="flat",  # 扁平样式
                    cursor="hand2",  # 手型光标
                )
            else:
                locate_logo_button = tk.Button(frame, text="定位 Logo")

            locate_logo_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.locate_logo_buttons.append(locate_logo_button)  # 将按钮添加到列表

            # 绑定拖动事件
            locate_logo_button.bind("<ButtonPress-1>", self.on_drag_start)
            locate_logo_button.bind("<B1-Motion>", self.on_drag_motion)
            locate_logo_button.bind("<ButtonRelease-1>", lambda e, idx=i: self.on_drag_end(e, idx))

            # 展示 Label
            logo_label = ttk.Label(frame, text="无")
            logo_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
            self.logo_labels.append(logo_label)  # 将 Label 添加到列表

            # 选择路线的下拉列表
            route_var = tk.StringVar()
            route_options = [str(i) for i in range(1, 15)]  # 1-14
            route_menu = ttk.Combobox(frame, textvariable=route_var, values=route_options, state="readonly", width=5)
            route_menu.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.route_menu.append(route_menu)

            # 开始按钮
            start_button = ttk.Button(frame, text="开始", command=lambda idx=i: self.toggle_start_stop(idx))
            start_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")
            self.start_buttons.append(start_button)  # 将开始按钮添加到列表

    def get_window(self):
        """
        获取窗口按钮的回调函数
        """
        chrome_handles = get_qqsg_windows()
        if not chrome_handles:
            messagebox.showwarning("提示", "没有找到 Chrome 窗口！！！")
        else:
            print(f"找到 {len(chrome_handles)} 个 Chrome 窗口句柄")

    def on_drag_start(self, event):
        """
        开始拖动按钮
        """
        # 获取当前拖动的按钮索引
        widget = event.widget  # 获取触发事件的按钮
        for idx, button in enumerate(self.locate_logo_buttons):
            if button == widget:
                self.drag_data = {
                    "x": event.x,
                    "y": event.y,
                    "idx": idx  # 记录按钮的索引
                }
                break

    def on_drag_motion(self, event):
        """
        拖动按钮过程中
        """
        # 获取当前拖动的按钮
        idx = self.drag_data["idx"]
        locate_logo_button = self.locate_logo_buttons[idx]

        # 计算新位置
        x = locate_logo_button.winfo_x() + (event.x - self.drag_data["x"])
        y = locate_logo_button.winfo_y() + (event.y - self.drag_data["y"])

        # 更新按钮位置
        locate_logo_button.place(x=x, y=y)  # 使用 place 实现拖动效果

    def on_drag_end(self, event, idx):
        """
        拖动按钮结束
        """
        # 获取鼠标释放位置的窗口句柄
        x, y = self.root.winfo_pointerxy()  # 获取鼠标的屏幕坐标
        hwnd = get_window_at_position(x, y)  # 获取窗口句柄

        if hwnd:
            # 显示句柄信息（十进制）
            self.logo_labels[idx].config(text=f"句柄: {hwnd}")  # 更新对应的 Label
            print(f"框 {idx + 1} 获取到窗口句柄: {hwnd}")
            # 将句柄存储到字典中
            self.window_handles['窗口'+str(idx+1)] = hwnd
            print(self.window_handles)
        else:
            self.logo_labels[idx].config(text="无")  # 更新对应的 Label
            print(f"框 {idx + 1} 未获取到窗口句柄")
            # 如果未获取到句柄，从字典中移除（如果有）
            self.window_handles.pop(['窗口'+str(idx+1)], None)

        # 恢复按钮位置
        self.locate_logo_buttons[idx].grid(row=0, column=0, padx=5, pady=5, sticky="w")

    def toggle_start_stop(self, idx):
        """
        切换开始/停止按钮
        """
        route_idx = '换线操作' + str(idx + 1)
        if self.start_buttons[idx].cget("text") == "开始":
            handle = '窗口' + str(idx + 1)
            # 检查窗口句柄是否存在
            if handle in self.window_handles:
                # 切换到停止按钮
                self.start_buttons[idx].config(text="停止")
                # 禁用其他开始按钮
                for i, button in enumerate(self.start_buttons):
                    if i != idx:
                        button.config(state="disabled")
                if self.route_menu[idx].get() == '':
                    # 弹出提示
                    messagebox.showwarning("错误", f"请确认是否选择了线路！！！")
                else:
                    # 启动线程
                    hwnd = self.window_handles[handle]
                    route_number = int(self.route_menu[idx].get())
                    stop_event = threading.Event()
                    thread = RouteThread(hwnd, stop_event, lambda: self.on_thread_finish(idx, route_idx), route_number)
                    thread.start()
                    # 存储线程和事件
                    self.threads[route_idx] = thread
                    self.stop_events[route_idx] = stop_event
            else:
                # 弹出提示
                messagebox.showwarning("提示", f"没有找到窗口 {idx + 1} 的句柄！")
        else:
            # 停止线程
            if route_idx in self.stop_events:
                print("检测到线程存在，正在清理")
                self.stop_events[route_idx].set()  # 设置事件，中断线程
                # 设置超时时间，避免主线程无限等待
                self.threads[route_idx].join(timeout=1)  # 最多等待 2 秒
                # 清理线程和事件
                if route_idx in self.threads:
                    del self.threads[route_idx]
                if route_idx in self.stop_events:
                    del self.stop_events[route_idx]
            # 切换到开始按钮
            self.start_buttons[idx].config(text="开始")
            # 启用所有开始按钮
            for button in self.start_buttons:
                button.config(state="normal")

    def on_thread_finish(self, idx, route_idx):
        """
        线程完成时的回调函数
        """
        # 切换到开始按钮
        self.start_buttons[idx].config(text="开始")

        # 清理线程和事件
        if route_idx in self.stop_events:
            del self.threads[route_idx]
            del self.stop_events[route_idx]

        # 启用所有开始按钮
        for button in self.start_buttons:
            button.config(state="normal")

    # 喊话功能界面
    def init_tab2(self):
        label = ttk.Label(self.tab2, text="喊话功能")
        label.pack(pady=20)

        # 输入框
        self.message_entry = ttk.Entry(self.tab2, width=40)
        self.message_entry.pack(pady=10)

        # 喊话按钮
        shout_button = ttk.Button(self.tab2, text="喊话", command=self.shout_message)
        shout_button.pack(pady=10)

    def shout_message(self):
        message = self.message_entry.get()
        print(f"喊话内容：{message}")

    # 卡键功能界面
    def init_tab3(self):
        label = ttk.Label(self.tab3, text="卡键功能")
        label.pack(pady=20)

        # 开关按钮
        self.key_stuck_var = tk.BooleanVar()
        key_stuck_button = ttk.Checkbutton(self.tab3, text="启用卡键", variable=self.key_stuck_var)
        key_stuck_button.pack(pady=10)

    # 同步功能界面
    def init_tab4(self):
        label = ttk.Label(self.tab4, text="同步功能")
        label.pack(pady=20)

        # 同步按钮
        sync_button = ttk.Button(self.tab4, text="同步", command=self.sync_data)
        sync_button.pack(pady=10)

    def sync_data(self):
        print("数据已同步")

    # 连点功能界面
    def init_tab5(self):
        label = ttk.Label(self.tab5, text="连点功能")
        label.pack(pady=20)

        # 定位按钮
        self.click_locate_button = tk.Button(
            self.tab5,
            image=self.icons["locate_icon"],
            bd=0,  # 无边框
            relief="flat",  # 扁平样式
            cursor="hand2",  # 手型光标
        )
        self.click_locate_button.pack(pady=10)

        # 绑定拖动事件
        self.click_locate_button.bind("<ButtonPress-1>", self.on_click_drag_start)
        self.click_locate_button.bind("<B1-Motion>", self.on_click_drag_motion)
        self.click_locate_button.bind("<ButtonRelease-1>", self.on_click_drag_end)

        # 坐标显示
        self.click_pos_label = ttk.Label(self.tab5, text="点击位置：未定位")
        self.click_pos_label.pack()

        # 启动/停止按钮
        self.click_toggle_button = ttk.Button(
            self.tab5,
            text="启动连点",
            command=self.clicker_start_stop
        )
        self.click_toggle_button.pack(pady=10)

    def on_click_drag_start(self, event):
        """开始拖动定位按钮"""
        self.drag_data = {
            "x": event.x,
            "y": event.y,
            "widget": event.widget
        }

    def on_click_drag_motion(self, event):
        """拖动定位按钮过程中"""
        widget = self.drag_data["widget"]
        x = widget.winfo_x() + (event.x - self.drag_data["x"])
        y = widget.winfo_y() + (event.y - self.drag_data["y"])
        widget.place(x=x, y=y)

    def on_click_drag_end(self, event):
        """结束拖动定位按钮"""
        # 获取鼠标释放位置的窗口句柄
        self.clicker_x, self.clicker_y = self.root.winfo_pointerxy()
        self.clicker_hwnd = get_window_at_position(self.clicker_x, self.clicker_y)
        self.clicker_position = locate_position_in_hwnd(self.clicker_hwnd, self.clicker_x, self.clicker_y)
        if self.clicker_position:
            self.click_pos_label.config(text=f"点击位置：{self.clicker_position[0]}, {self.clicker_position[1]} (窗口: {self.clicker_hwnd})")
        else:
            self.click_pos_label.config(text="点击位置：定位失败")
        # 恢复按钮位置
        self.click_locate_button.pack(pady=10)

    def clicker_start_stop(self):
        """切换连点状态"""
        if self.click_toggle_button.cget("text") == "启动连点":
            # 检查是否已定位
            if not self.clicker_position:
                messagebox.showerror("错误", "请先定位点击位置")
                return

            # 开始连点
            self.click_toggle_button.config(text="停止连点")
            click_stop_event = threading.Event()
            thread = ClickerThread(self.clicker_hwnd, click_stop_event, lambda: self.on_thread_finish2(), self.clicker_position[0], self.clicker_position[1])
            thread.start()
            self.threads['clicker'] = thread
            self.stop_events['clicker'] = click_stop_event
        else:
            if 'clicker' in self.stop_events:
                self.stop_events['clicker'].set()  # 设置事件，中断线程
                # 设置超时时间，避免主线程无限等待
                self.threads['clicker'].join(timeout=1)  # 最多等待 2 秒
                # 清理线程和事件
                if 'clicker' in self.threads:
                    del self.threads['clicker']
                if 'clicker' in self.stop_events:
                    del self.stop_events['clicker']

    def on_thread_finish2(self):
        """
        线程完成时的回调函数
        """
        # 切换到开始按钮
        self.click_toggle_button.config(text="启动连点")
        # 清理线程和事件
        if 'clicker' in self.stop_events:
            del self.threads['clicker']
            del self.stop_events['clicker']


# 运行程序
if __name__ == "__main__":
    root = tk.Tk()
    app = ToolApp(root)
    root.mainloop()