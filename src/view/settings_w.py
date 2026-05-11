import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from src.view.base_view import BaseView
import src.config as config
import os

class SettingsFrame(BaseView):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.configure(fg_color="#f0f8ff")
        self.old_settings = self.controller.get_settings()
        self.is_change = False
        # Головний контейнер із відступами
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True, fill="both", padx=40, pady=30)

        # Заголовок
        self.settings_label = self.create_label(master=self.main_container, text="Налаштування")
        self.settings_label.configure(font=("Segoe UI", 32, "bold"))
        self.settings_label.pack(anchor="w", pady=(0, 30))

        self.general_section = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15, border_width=1, border_color="#e0e0e0")
        self.general_section.pack(fill="x", pady=(0, 20), padx=2)
        self.general_section.grid_columnconfigure(1, weight=1)

        # Шлях
        self.create_label(self.general_section, text="Шлях за умовчанням", font_size=16).grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        path_wrapper = ctk.CTkFrame(self.general_section, fg_color="transparent")
        path_wrapper.grid(row=0, column=1, padx=20, pady=20, sticky="e")
        
        self.path_var = tk.StringVar(value=self.old_settings.get(config.DEFAULT_SAVE_PATH_KEY, ""))
        self.path_entry = ctk.CTkEntry(path_wrapper, textvariable=self.path_var, state="readonly", width=300, height=35)
        self.path_entry.pack(side="left", padx=(0, 10))
        
        self.path_button = self.create_button(path_wrapper, text="Обрати шлях", width=80, height=35, command=self.controller.browse_directory)
        self.path_button.pack(side="left")


        ctk.CTkFrame(self.general_section, height=2, fg_color="#f0f0f0").grid(row=1, column=0, columnspan=2, sticky="ew", padx=15)

        # Тема
        self.create_label(self.general_section, text="Кольорова тема", font_size=16).grid(row=2, column=0, padx=20, pady=20, sticky="w")
        self.theme_var = tk.StringVar(value=self.old_settings.get(config.THEME_KEY))
        self.theme_option = self.create_option(self.general_section, values=tuple(k for k in config.THEMES.keys()), var=self.theme_var)
        self.theme_option.configure(width=200)
        self.theme_option.grid(row=2, column=1, padx=20, pady=20, sticky="e")

        self.lang_section = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15, border_width=1, border_color="#e0e0e0")
        self.lang_section.pack(fill="both", expand=True, pady=(0, 20), padx=2)
        
        self.create_label(self.lang_section, text="Доступні мови для вибору", font_size=18).pack(anchor="w", padx=20, pady=(15, 10))
        
        self.available_langs = self.controller.get_available_languages()
        in_use_lang = self.old_settings.get(config.LANGUAGES_KEY, {})
        self.checkouts = {}

        self.lang_scroll = ctk.CTkScrollableFrame(self.lang_section, fg_color="transparent", height=200)
        self.lang_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        for lang_short, lang_full in self.available_langs.items():
            cb = ctk.CTkCheckBox(self.lang_scroll, text=lang_full, font=("Segoe UI", 14), 
                                 hover_color="#40c057", fg_color="#40c057")
            if lang_short in in_use_lang:
                cb.select()
            cb.pack(anchor="w", padx=20, pady=8)
            self.checkouts[lang_short] = cb

        #Панель з кнопками
        self.button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.button_frame.pack(fill="x", pady=10)

        self.save_btn = self.create_button(self.button_frame, text="Зберегти зміни", 
                                           command=self.controller.handle_save_settings, 
                                           width=200, height=45)
        self.save_btn.pack(side="right", padx=2)
    
    def save_and_notify(self):
        self.save_btn.configure(fg_color="#2f9e44", text="Збережено ✓")
        self.after(2000, lambda: self.save_btn.configure(fg_color="#40c057", text="Зберегти зміни"))

    

    def forming_new_lang_dict(self):
        current_langs = {l_s: self.available_langs[l_s] for l_s, cb in self.checkouts.items() if cb.get() == 1}
        if not current_langs:
            current_langs["en"] = "english"
        return current_langs

    def get_current_ui_state(self):
        return {
            config.DEFAULT_SAVE_PATH_KEY: str(self.path_var.get()).strip(),
            config.THEME_KEY: self.theme_var.get(),
            config.LANGUAGES_KEY: self.forming_new_lang_dict()
        }

    def check_for_changes(self):
        current_state = self.get_current_ui_state()
        self.is_change = current_state != self.old_settings
        self.pending_settings = current_state
        
        return self.is_change

    def save_settings(self):
        current_theme = self.get_current_ui_state()[config.THEME_KEY]
        ctk.set_appearance_mode(config.THEMES[current_theme])
        return self.get_current_ui_state()
    
    def set_actual_settings(self):
        self.path_var.set(self.old_settings[config.DEFAULT_SAVE_PATH_KEY])
        self.theme_var.set(self.old_settings[config.THEME_KEY])   
        active_lang_keys = self.old_settings.get(config.LANGUAGES_KEY, {}).keys()
        
        for lang_short, cb in self.checkouts.items():
            if lang_short in active_lang_keys:
                cb.select()
            else:
                cb.deselect()     