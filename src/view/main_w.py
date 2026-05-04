import customtkinter as ctk
import tkinter as tk
import os
from PIL import Image
from src.view.base_view import BaseView

class MainFrame(BaseView):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.configure(fg_color="#f0f8ff")

        self.file_path_var = tk.StringVar(value="")
        
        self.model_size_var = tk.StringVar(value="base")
        self.language_var = tk.StringVar(value="uk")
        self.fp16_var = tk.BooleanVar(value=True)
        self.preprocessing_var = tk.BooleanVar(value=False)
        

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = SideBarFrame(master=self)
        self.sidebar.grid(row=0, column=0, sticky="nswe")

        self.main_content = MainContent(master=self, controller=self.controller)
        self.main_content.grid(row=0, column=1, sticky="nswe")
    
    def compile_parameters(self):
        prompt_var = self.main_content.parameters_frame.prompt_textbox.get("1.0", "end-1c")
        return {
            "file_path": self.file_path_var.get(),
            "model_size": self.model_size_var.get(),
            "language": self.language_var.get(),
            "fp16": self.fp16_var.get(),
            "preprocessing": self.preprocessing_var.get(),
            "prompt": prompt_var,
        }

class MainContent(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.input_frame = InputFrame(master=self, controller=controller)
        self.parameters_frame = ParametersFrame(master=self,
        controller=controller)

        self.input_frame.grid(row=0, column=0, sticky="we", pady=(240, 50))
        self.parameters_frame.grid(row=1, column=0, sticky="nwe")

    
class InputFrame(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.file_name_var = tk.StringVar(value="Виберіть аудіо або відео файл")
        
        self.choose_path_btn = ctk.CTkButton(
            master=self,
            fg_color="#40c057",
            hover_color="#31b249",
            textvariable=self.file_name_var,
            command=self.browse_file,
            font=("Segoe UI", 24, "bold"),
            text_color="#000000",
            width=850, height=80
        )
        self.choose_path_btn.grid(row=0, column=1, padx=10)

        icon_path = os.path.join(BaseView.project_dir, "assets", "play_light.png")
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

    def browse_file(self):
        file_path = tk.filedialog.askopenfilename(
            title="Оберіть файл",
            filetypes=[("Медіа файли", "*.mp3 *.wav *.m4a *.mp4 *.mkv *.avi")]
        )
        if file_path:
            self.file_name_var.set(os.path.basename(file_path))
            self.master.master.file_path_var.set(file_path)

class ParametersFrame(ctk.CTkFrame):
    def __init__(self, master,controller, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.controller = controller 
        self.available_models = self.controller.get_available_models()
        self.available_languages = self.controller.get_available_languages()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=1)
        for i in range(4):
            self.rowconfigure(i, weight=1)
        #Вибір моделі---------------------------------------
        self.choose_model_frame = ctk.CTkFrame(master=self,
                                               fg_color ="transparent",
                                               )
        self.choose_model_label = master.master.create_label(self.choose_model_frame, "Розмір моделі")
        self.choose_model_label.pack(anchor="w")

        self.choose_model_options = master.master.create_option(master = self.choose_model_frame,
                                                                values = self.available_models,
                                                                var = self.master.master.model_size_var)
        self.choose_model_options.pack()
        self.choose_model_frame.grid(row=0, column=1, sticky="nw", padx=(0, 145))    

        #Вибір мови-------------------------------------------------
        self.choose_language_frame = ctk.CTkFrame(master=self,
                                               fg_color ="transparent",
                                               )
        self.choose_language_label = master.master.create_label(self.choose_language_frame, "Мова")
        self.choose_language_label.pack(anchor="w")

        self.choose_language_options = master.master.create_option(master = self.choose_language_frame,
                                                                values = self.available_languages,
                                                                var = self.master.master.language_var)
        self.choose_language_options.pack()
        self.choose_language_frame.grid(row=1, column=1, pady=20, sticky="nw")

        #Перемикач FP16------------------------------------------------
        self.fp16_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        
        self.fp16_label = master.master.create_label(self.fp16_frame, "Використовувати fp16")
        self.fp16_label.pack(side="left", padx=(0, 10))

        self.fp16_switch = master.master.create_switch(master=self.fp16_frame,
                                                       var=self.master.master.fp16_var)
        self.fp16_switch.pack(side="right")
        self.fp16_frame.grid(row=2, column=1, sticky="nw", pady=20)

        #Перемикач препроцесинг---------------------------------------------------
        self.preprocessing_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        
        self.preprocessing_label = master.master.create_label(self.preprocessing_frame, "Попередня обробка")
        self.preprocessing_label.pack(side="left", padx=(0, 10))

        self.preprocessing_switch = master.master.create_switch(master=self.preprocessing_frame,
                                                       var=self.master.master.preprocessing_var)
        self.preprocessing_switch.pack(side="right")
        self.preprocessing_frame.grid(row=3, column=1, sticky="nw", pady=5)

        #Поле вводу промпту---------------------------------------
        self.prompt_frame = ctk.CTkFrame(master=self,
                                         fg_color="transparent")
        self.prompt_label = master.master.create_label(self.prompt_frame, "Промпт")
        self.prompt_label.pack(anchor="w", padx=5, pady=(0, 5))
        self.prompt_textbox = ctk.CTkTextbox(
            master=self.prompt_frame,
            width=450,
            corner_radius=12,
            border_width=2,
            border_color="#40c057",
            fg_color="#ffffff",  
            text_color="#000000",
            font=("Segoe UI", 24),
            undo=True,   
            wrap="word",
        )
        self.prompt_textbox.pack(fill="both", expand=True)
        self.prompt_frame.grid(row=0, column=2,rowspan=4, sticky="nwse")

    
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
        
        