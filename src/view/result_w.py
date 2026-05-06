import customtkinter as ctk
import tkinter as tk
from src.view.base_view import BaseView
class ResultFrame(BaseView):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.configure(fg_color="#f0f8ff")
        self.processing_label_var = tk.StringVar(value="Початок обробки")

        self.main_frame = ctk.CTkFrame(master=self, fg_color="transparent")

        #Інформаційний лейбл про хід обробки
        self.processing_label = self.create_label(master=self.main_frame, text="", var=self.processing_label_var)
        self.processing_label.pack()

        #Фрейм з результатом
        self.processing_frame = ctk.CTkFrame(self, 
                                             fg_color="transparent",
                                             border_width=2,
                                             corner_radius=8,
                                             )
        self.processing_progressbar = ctk.CTkProgressBar(master=self.processing_frame, mode="indeterminate")
        
        self.processing_progressbar.pack(pady=(0, 15))
        

        self.processing_frame.place(relx=0.5, rely=0.5, anchor="center")


        