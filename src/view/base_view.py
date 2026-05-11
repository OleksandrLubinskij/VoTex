import customtkinter as ctk
import os
from PIL import Image
import src.config as config

class BaseView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def create_label(self, master, text, var=None, font_size=24, weight="bold", text_color=config.TEXT_COLOR):
        label = ctk.CTkLabel(
            master=master,
            text=text,
            font=("Segoe UI", font_size, weight),
            text_color=text_color,
            textvariable=var
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
            fg_color=config.SIGNATURE_GREEN,   
            button_color="#31b249",
            button_hover_color=config.SIGNATURE_GREEN_HOVER,
            text_color=config.TEXT_COLOR,
            font=("Segoe UI", 20, "bold"),
            dropdown_font=("Segoe UI", 20)
        )
        return option
    
    def create_switch(self, master, var):
        switch = ctk.CTkSwitch(
            master=master,
            text="",
            variable=var,
            progress_color=config.SIGNATURE_GREEN,
            width=70
        )
        return switch
    
    def create_button(self, master, text, command, fg_color=config.SIGNATURE_GREEN, hover_color=config.SIGNATURE_GREEN_HOVER, font_size=20, height=56, width=140, image=None):
        button = ctk.CTkButton(
            master=master,
            text=text,
            image=image,
            fg_color=fg_color,
            hover_color=hover_color,
            font=("Segoe UI", font_size, "bold"),
            text_color=config.TEXT_COLOR,
            corner_radius=8,
            height=height,
            width=width,
            command=command
        )
        return button
    
    def create_action_button(self, master, text, image, command, color=config.SIGNATURE_GREEN, hover_color=config.SIGNATURE_GREEN_HOVER):
        return self.create_button(
            master=master, 
            text=text, 
            image=image,
            command=command, 
            fg_color=color,
            hover_color=hover_color,
            font_size=16, 
            height=32, 
            width=1,
        )

class SideBarFrame(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master,
                        width=60, 
                        fg_color=config.SIGNATURE_GREEN,
                        corner_radius=0,
                        **kwargs)
        self.controller = controller
        self.grid_propagate(False)
        
        icons = ["history_light.png", "settings_light.png", "info_light.png"]
        commands = [
            self.controller.open_history, 
            self.controller.handle_open_settings, 
            self.controller.handle_open_info
        ]
        
        for command_index, icon_name in enumerate(icons):
            icon_path = os.path.join(config.ASSETS_DIR, icon_name)

            # Перевірка наявності файлу іконки (щоб програма не падала)
            try:
                icon = ctk.CTkImage(
                    light_image = Image.open(icon_path),
                    dark_image= Image.open(icon_path.replace("light", "dark")),
                    size=(40, 40)
                )
            except Exception as e:
                print(f"Помилка завантаження іконки {icon_name}: {e}")
                continue

            btn = ctk.CTkButton(
                self,
                text="",
                image=icon,
                width=60,
                height=60,
                fg_color="transparent",
                hover_color=config.SIGNATURE_GREEN_HOVER,
                corner_radius=8,
                command=commands[command_index]
            )
            btn.pack(pady=(20, 10), padx=5)