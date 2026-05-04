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

    def create_label(self, master, text):
        label = ctk.CTkLabel(
            master=master,
            text=text,
            font=("Segoe UI", 24, "bold")
        )
        return label

    def create_option(self, master, values, var):
        option = ctk.CTkOptionMenu(
            master=master,
            values=values,
            variable=var,
            width=350,
            height=50,
            corner_radius=8,
            dynamic_resizing=False,
            anchor="center", 
            fg_color="#40c057",   
            button_color="#31b249", 
            button_hover_color="#2b9a3f",
            text_color="#000000",
            font=("Segoe UI", 20, "bold"),
            dropdown_font=("Segoe UI", 20)
        )
        return option
    
    def create_switch(self, master, var):
        switch = ctk.CTkSwitch(
            master=master,
            text="",
            variable=var,
            progress_color="#40c057",
            width=70
        )
        return switch