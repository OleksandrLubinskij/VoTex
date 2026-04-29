import customtkinter as ctk
import tkinter as tk
import os
from PIL import Image
from src.view.base_view import BaseView

class MainFrame(BaseView):
    def __init__(self):
        super().__init__()
        self.configure(fg_color="#f0f8ff")
        self.file_path = ""
        self.model_size_var = tk.StringVar(value="base")
        self.language_var = tk.StringVar(value="en")
        self.fp16_var = tk.StringVar(value=True)
        self.preprocessing_var = False
        self.prompt_var = "Введіть промпт"

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = SideBarFrame(master=self)
        self.sidebar.grid(row=0, column=0, sticky="nswe")

        self.main_content = MainContent(master=self)
        self.main_content.grid(row=0, column=1, sticky="nswe")
        
class MainContent(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.input_frame = InputFrame(master=self)
        self.parameters_frame = ctk.CTkFrame(master=self)

        self.input_frame.grid(row=0, column=0, sticky="nswe")
        self.parameters_frame.grid(row=1, column=0, sticky="nswe")

class InputFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        # 1. Створюємо 4 колонки:
        # Колонка 0 і 3 — це "пружини" (weight=1), вони виштовхують контент у центр
        # Колонка 1 і 2 — для кнопок (weight=0), вони мають розмір самих кнопок
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.file_name_var = tk.StringVar(value="Виберіть аудіо або відео файл")
        
        # --- Кнопка вибору шляху ---
        self.choose_path_btn = ctk.CTkButton(
            master=self,
            fg_color="#40c057",
            hover_color="#36a64b",
            width=700,          # Тепер ми самі задаємо комфортну ширину
            height=80,
            corner_radius=8,
            border_color="#000000",
            border_width=3,
            font=("Segoe UI", 24, "bold"),
            text_color="#000000",
            textvariable=self.file_name_var,
            command=self.browse_file
        )
        # БЕЗ sticky="ew" — просто ставимо в 1-шу колонку
        self.choose_path_btn.grid(row=0, column=1, padx=10)

        # --- Кнопка ПУСК (Стрілочка) ---
        # Використовуємо Спосіб 1, який ми обговорили (project_dir як атрибут класу)
        icon_path = os.path.join(BaseView.project_dir, "assets", "play_light.png")
        icon = ctk.CTkImage(
            light_image=Image.open(icon_path),
            dark_image=Image.open(icon_path.replace("light", "dark")),
            size=(30, 30)
        )

        self.start_algorithm_btn = ctk.CTkButton(
            self,
            text="",
            image=icon,
            width=80,          # Робимо її компактною та квадратною
            height=80,
            corner_radius=8,
            border_color="#000000",
            border_width=3,
            fg_color="#40c057",
            hover_color="#36a64b",
        )
        # Ставимо в 2-гу колонку поруч
        self.start_algorithm_btn.grid(row=0, column=2, padx=10)

    def browse_file(self):
        file_path =  tk.filedialog.askopenfilename(
            title ="Оберіть аудіо або відео для транскрибації",
            filetypes=[
                ("Медіа файли", "*.mp3 *.wav *.m4a *.mp4 *.mkv *.avi"),
                ("Усі файли", "*.*")
            ]
        )
        if file_path:
            file_name = os.path.basename(file_path)
            self.file_name_var.set(file_name)
            self.file_path_var.set(file_path)

class ParametersFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
class SideBarFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master,
                        width=60, 
                        fg_color="#40c057",
                        border_color="#000000",
                        corner_radius=0,
                        **kwargs)
        
        self.grid_propagate(False)
        icons = ["history_light.png", "info_light.png", "settings_light.png"]
        for icon_name in icons:

            icon_path = os.path.join(BaseView.project_dir, "assets", icon_name)

            icon = ctk.CTkImage(
                light_image = Image.open(icon_path),
                dark_image= Image.open(icon_path.replace("light", "dark")),
                size=(40, 40)
            )

            self.icon_btn = ctk.CTkButton(
                self,
                text="",
                image=icon,
                width=60,
                height=60,
                fg_color="transparent",
                hover_color="#66ce79",
                corner_radius=8
            )

            self.icon_btn.pack(pady=(20, 10), padx=5)
        
        