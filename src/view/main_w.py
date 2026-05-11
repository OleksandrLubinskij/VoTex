import customtkinter as ctk
import tkinter as tk
import os
from PIL import Image
from src.view.base_view import BaseView
import src.config as config

class MainFrame(BaseView):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller

        self.available_languages = self.controller.get_settings()[config.LANGUAGES_KEY]

        self.file_path_var = tk.StringVar(value="")
        self.model_size_var = tk.StringVar(value="base")
        self.language_var = tk.StringVar(value=list(self.available_languages.values())[0])
        self.fp16_var = tk.BooleanVar(value=True)
        self.preprocessing_var = tk.BooleanVar(value=False)
        
        self.file_name_var = tk.StringVar(value="Виберіть аудіо або відео файл")
        
        self.main_content = MainContent(master=self, controller=self.controller)
        self.main_content.place(relx=0.5, rely=0.5, anchor="center")
    
    def compile_parameters(self):
        prompt_var = self.main_content.parameters_frame.prompt_textbox.get("1.0", "end-1c")
        return {
            "file_path": self.file_path_var.get(),
            "model_size": self.model_size_var.get(),
            "language": next((short_lang for short_lang, lang in self.available_languages.items() if lang == self.language_var.get()), None),
            "fp16": self.fp16_var.get(),
            "preprocessing": self.preprocessing_var.get(),
            "prompt": prompt_var,
        }
    

class MainContent(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.columnconfigure(0, weight=1)

        self.input_frame = InputFrame(master=self, controller=controller)
        self.parameters_frame = ParametersFrame(master=self, controller=controller)

        self.input_frame.grid(row=0, column=0, sticky="we", pady=(0, 40))
        self.parameters_frame.grid(row=1, column=0, sticky="nwe")

   
class InputFrame(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        
        
        self.choose_path_btn = ctk.CTkButton(
            master=self,
            fg_color="#40c057",
            hover_color="#31b249",
            textvariable=master.master.file_name_var,
            command=self.controller.browse_file,
            font=("Segoe UI", 24, "bold"),
            text_color="#000000",
            width=800, height=80 
        )
        self.choose_path_btn.grid(row=0, column=1, padx=10)

        icon_path = os.path.join(config.ASSETS_DIR, "play_light.png")
        icon = ctk.CTkImage(light_image=Image.open(icon_path), size=(30, 30))

        self.start_algorithm_btn = ctk.CTkButton(
            self,
            text="",
            image=icon,
            width=80, height=80,
            fg_color="#40c057",
            hover_color="#31b249",
            command=self.controller.start_transcribation 
        )
        self.start_algorithm_btn.grid(row=0, column=2, padx=10)

class ParametersFrame(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = controller 
        
        self.available_models = self.controller.get_available_models()
        
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=1)

        self.settings_col = ctk.CTkFrame(self, fg_color="transparent")
        self.settings_col.grid(row=0, column=1, sticky="n", padx=(0, 40))
        self.lang = [val for val in master.master.available_languages.values()]

        # 1. Модель
        self.m_frame = ctk.CTkFrame(self.settings_col, fg_color="transparent")
        self.m_frame.pack(fill="x", pady=(0, 15))
        master.master.create_label(self.m_frame, "Розмір моделі").pack(anchor="w")
        master.master.create_option(self.m_frame, self.available_models, master.master.model_size_var).pack(fill="x")

        # 2. Мова
        self.l_frame = ctk.CTkFrame(self.settings_col, fg_color="transparent")
        self.l_frame.pack(fill="x", pady=15)
        master.master.create_label(self.l_frame, "Мова").pack(anchor="w")
        self.lang_options = master.master.create_option(self.l_frame, self.lang, master.master.language_var)
        self.lang_options.pack(fill="x")

        # 3. FP16
        self.f_frame = ctk.CTkFrame(self.settings_col, fg_color="transparent")
        self.f_frame.pack(fill="x", pady=10)
        master.master.create_label(self.f_frame, "Використати FP16").pack(side="left", padx=(0, 10))
        master.master.create_switch(self.f_frame, master.master.fp16_var).pack(side="right")

        # 4. Препроцесинг
        self.p_frame = ctk.CTkFrame(self.settings_col, fg_color="transparent")
        self.p_frame.pack(fill="x", pady=10)
        master.master.create_label(self.p_frame, "Попередня обробка").pack(side="left", padx=(0, 10))
        master.master.create_switch(self.p_frame, master.master.preprocessing_var).pack(side="right")

        # Поле Промпту (Права колонка)
        self.prompt_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.prompt_frame.grid(row=0, column=2, sticky="nsew")
        
        master.master.create_label(self.prompt_frame, "Промпт").pack(anchor="w", pady=(0, 5))
        self.prompt_textbox = ctk.CTkTextbox(
            self.prompt_frame,
            width=400, height=250,
            corner_radius=12, border_width=2,
            border_color="#40c057", fg_color="#ffffff", text_color="#000000",
            font=("Segoe UI", 18), wrap="word"
        )
        self.prompt_textbox.pack(fill="both", expand=True)

    def update_lang_options(self, new_languages):
        self.lang = new_languages
        self.lang_options.configure(values=new_languages) 
        if self.lang:
            self.master.master.language_var.set(self.lang[0])