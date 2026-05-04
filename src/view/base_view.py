import customtkinter as ctk
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