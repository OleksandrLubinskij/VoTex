import tkinter as tk
import customtkinter as ctk
import platform
import src.config as config
import os

class BaseView(ctk.CTk):
    current_os = platform.system()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(current_dir))

    def __init__(self):
        super().__init__()
        self.title("VoTex")
        self.after(0, self.set_maximized)
    
    def set_maximized(self):
        os_action = {
            config.WINDOWS: lambda: self.state("zoomed"),
            config.LINUX: lambda: self.attributes("-zoomed", True),
            config.MACOS: lambda: self.state("normal")
        }

        action = os_action.get(self.current_os, lambda: self.geometry("1200x800"))

        try:
            action()
        except Exception as e:
            print(f"Can`t open zoomed window, used default size\n Error: {e}")

    def setup_icon(self):
        
        icon_path = os.path.join(self.project_dir, "assets", "logo.ico")
        print(icon_path)
        os_action = {
            config.WINDOWS: lambda: self.iconbitmap(icon_path),
            config.LINUX: lambda: self._set_png_icon(icon_path),
            config.MACOS: lambda: self._set_png_icon(icon_path),
        }
        action = os_action.get(self.current_os)
        try:
            action()
        except:
            print("Can`t load icon!")
    
    def _set_png_icon(self, icon_path):
        png_path = icon_path.replace(".ico", ".png")
        if os.path.exists(png_path):
            self.icon_image = tk.PhotoImage(file=png_path)
            self.iconphoto(False, self.icon_image)