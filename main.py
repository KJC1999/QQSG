# main.py

from ui.main_window import ToolApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = ToolApp(root)
    root.mainloop()