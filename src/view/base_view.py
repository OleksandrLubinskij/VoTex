import customtkinter as ctk
import os
from PIL import Image
import src.config as config
class BaseView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        

    def create_label(self, master, text, var=None, font_size=24, weight="bold"):
        label = ctk.CTkLabel(
            master=master,
            text=text,
            font=("Segoe UI", font_size, weight),
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
    
    def create_button(self, master, text, command, fg_color="#40c057", hover_color="#2b9a3f", font_size=20, height=56, width=140, image=None):
        button = ctk.CTkButton(
            master=master,
            text=text,
            image=image,
            fg_color=fg_color,
            hover_color=hover_color,
            font=("Segoe UI", font_size, "bold"),
            text_color="#000000",
            corner_radius=8,
            height=height,
            width=width,
            command=command
        )
        return button
    
    def create_action_button(self, master, text, image, command, color="#40c057", hover_color="#31b249"):
        return self.create_button(
            master=master, 
            text=text, 
            image=image,
            command=command, 
            fg_color=color,
            hover_color=hover_color,
            font_size=16, 
            height=32, 
            width=1
        )
class SideBarFrame(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master,
                        width=60, 
                        fg_color="#40c057",
                        border_color="#000000",
                        corner_radius=0,
                        **kwargs)
        self.controller = controller
        self.grid_propagate(False)
        icons = ["history_light.png", "settings_light.png", "info_light.png"]
        commands = [self.controller.open_history, self.controller.handle_open_settings, self.controller.handle_open_info]
        for command_index, icon_name in enumerate(icons):

            icon_path = os.path.join(config.ASSETS_DIR, icon_name)

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
                corner_radius=8,
                command=commands[command_index]
            )

            self.icon_btn.pack(pady=(20, 10), padx=5)