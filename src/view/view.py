import tkinter as tk
import customtkinter as ctk
import os
import src.config as config
from src.view.main_w import MainFrame
from src.view.result_w import ResultFrame
from src.view.history_w import HistoryFrame
from src.view.settings_w import SettingsFrame
from src.view.info_w import InfoFrame
from src.view.base_view import SideBarFrame

class View(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.title("VoTex")
        self.set_maximized()
    
    
        self.frames = {}
        self.controller = controller
        self.theme = self.controller.get_settings()[config.THEME_KEY]
        ctk.set_appearance_mode(config.THEMES[self.theme])
        self.container = ctk.CTkFrame(self)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=0)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.pack(side="right",
                                      fill="both",
                                      expand=True)
        self.sidebar = SideBarFrame(master=self.container, controller = self.controller)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self._current_frame = config.MAIN_FRAME
        for F in (MainFrame, ResultFrame, HistoryFrame, SettingsFrame, InfoFrame):
            page_name = F.__name__
            frame = F(controller=self.controller, master=self.container)
            self.frames[page_name] = frame
            frame.grid(row=0, column=1, sticky="nswe")

        self.show_frame(config.MAIN_FRAME)

    def set_maximized(self):
        os_action = {
            config.WINDOWS: lambda: self.state("zoomed"),
            config.LINUX: lambda: self.attributes("-zoomed", True),
            config.MACOS: lambda: self.state("normal")
        }

        action = os_action.get(config.CURRENT_OS, lambda: self.geometry("1200x800"))

        try:
            action()
        except Exception as e:
            print(f"Can`t open zoomed window, used default size\n Error: {e}")

    def setup_icon(self):
        
        icon_path = os.path.join(config.ASSETS_DIR, "logo.ico")
        print(icon_path)
        os_action = {
            config.WINDOWS: lambda: self.iconbitmap(icon_path),
            config.LINUX: lambda: self._set_png_icon(icon_path),
            config.MACOS: lambda: self._set_png_icon(icon_path),
        }
        action = os_action.get(config.CURRENT_OS)
        try:
            action()
        except:
            print("Can`t load icon!")
    
    def _set_png_icon(self, icon_path):
        png_path = icon_path.replace(".ico", ".png")
        if os.path.exists(png_path):
            self.icon_image = tk.PhotoImage(file=png_path)
            self.iconphoto(False, self.icon_image)

    def get_current_frame(self):
        return self._current_frame
    
    def set_current_frame(self, new_frame):
        self._current_frame = new_frame
        
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

