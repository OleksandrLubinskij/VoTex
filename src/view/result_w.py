import customtkinter as ctk
import tkinter as tk
from src.view.base_view import BaseView
import src.config as config
class ResultFrame(BaseView):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.configure(fg_color="#f0f8ff")
        self.processing_label_var = tk.StringVar()

        self.main_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        #Інформаційний лейбл про хід обробки
        self.processing_label = self.create_label(
            master=self.main_frame, 
            text="", 
            var=self.processing_label_var)
        self.processing_label.pack(pady=(0, 20))

        #Фрейм з результатом
        self.result_frame = ctk.CTkFrame(self.main_frame, 
                                             fg_color="white",
                                             border_width=2,
                                             border_color="#40c057",
                                             corner_radius=15,
                                             height=600,
                                             width=800
                                             )
        self.result_frame.pack(pady=(0, 20))
        self.result_frame.pack_propagate(False)

        self.processing_progressbar = ctk.CTkProgressBar(master=self.result_frame, 
                                                         mode="indeterminate",
                                                         height=30,
                                                         width=400,
                                                         progress_color="#40c057",
                                                         border_width=2,
                                                         corner_radius=10)
        
        self.processing_progressbar.place(relx=0.5, rely=0.5, anchor="center")
        

        self.result_textbox = ctk.CTkTextbox(master=self.result_frame,
                                             fg_color="transparent",
                                             height=600,
                                             width=800,
                                             text_color="black",
                                             font=("Segoe UI", 18),
                                             corner_radius=12)
        
        self.buttons_frame = ctk.CTkFrame(master=self.main_frame,
                                          fg_color="transparent")
        
        buttons_dict = {
            "Зберегти": lambda: self.controller.save_result(manual=False),
            "Зберегти як": lambda: self.controller.save_result(manual=True),
            "На головну": lambda: self.controller.switch_frame(config.MAIN_FRAME)
        }

        for i in range(len(buttons_dict)):
            self.buttons_frame.columnconfigure(i, weight=1, uniform="buttons")
            
        

        for i, (name_btn, command_btn) in enumerate(buttons_dict.items()):
            button = self.create_button(master = self.buttons_frame,
                                        text =name_btn,
                                        command = command_btn
                                        )
            button.grid(row=0, column=i, padx=10, sticky="nswe")
        

    def prepare_for_new_task(self):
        self.result_textbox.pack_forget()
        self.buttons_frame.pack_forget()
        self.result_textbox.delete("1.0", "end")
        self.processing_label_var.set("Процес транскрибації. Це може зайняти декілька хвилин")
        self.processing_progressbar.place(relx=0.5, rely=0.5, anchor="center")
        self.processing_progressbar.start() 

    def display_result(self, text):
        if self.processing_progressbar.winfo_exists():
            self.processing_progressbar.stop()
            self.processing_progressbar.place_forget()

        self.processing_label_var.set("Обробка завершена!")

        self.result_textbox.insert("end", text)
        
        self.result_textbox.pack(fill="both", expand=True, padx=15, pady=15)
        self.buttons_frame.pack(fill="x", padx=20, pady=10)    