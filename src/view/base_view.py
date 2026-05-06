import customtkinter as ctk
import os
from PIL import Image
import src.config as config
class BaseView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        

    def create_label(self, master, text, var=None):
        label = ctk.CTkLabel(
            master=master,
            text=text,
            font=("Segoe UI", 24, "bold"),
            textvariable = var
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
                corner_radius=8
            )

            self.icon_btn.pack(pady=(20, 10), padx=5)