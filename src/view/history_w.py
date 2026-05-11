import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from src.view.base_view import BaseView
import src.config as config
import os
from PIL import Image

class HistoryFrame(BaseView):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.rows = {}
        self.controller = controller
        self.configure(fg_color=config.FG_COLOR)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True, fill="both", padx=20, pady=20)
        self.record_on_ui_count = 0

        self.history_label = self.create_label(self.main_container, text="Історія результатів", font_size=32)
        self.history_label.pack(anchor="w", pady=(0, 20))

        # Шапка таблиці
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color="#dfd9d9", height=40)
        self.header_frame.pack(fill="x", padx=5)
        
        for i in range(len(config.TABLE_HEADERS)):
            self.header_frame.grid_columnconfigure(i, weight=1, uniform="column_group")

        for i, col_name in enumerate(config.TABLE_HEADERS):

            align = "we"
            
            lbl = self.create_label(master=self.header_frame, text=col_name, text_color="#000000")
            lbl.grid(row=0, column=i, sticky=align, padx=10, pady=10)

        self.scroll_frame = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.scroll_frame.pack(expand=True, fill="both", pady=15)

        self.bottom_bar = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.bottom_bar.pack(fill="x", pady=(15, 0))

        self.create_button(self.bottom_bar, "На головну", 
                          self.controller.handle_back_to_main_frame,
                          width=200).pack(side="left", padx=5)
        
        self.load_more_btn = self.create_button(self.bottom_bar, "Завантажити ще", 
                          self.controller.load_more_history, 
                          fg_color=config.SIGNATURE_GREEN, hover_color=config.SIGNATURE_GREEN_HOVER, width=200)
        self.load_more_btn.pack(side="left", padx=5)
        
        self.create_button(self.bottom_bar, "Очистити все", 
                          self.controller.delete_all_records, 
                          fg_color=config.SIGNATURE_RED, hover_color=config.SIGNATURE_RED_HOVER, width=200).pack(side="right", padx=5)

    def fill_table(self, load_more, offset):
        font_size = 20
        
        if not load_more:
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()
            self.rows.clear()
            self.record_on_ui_count = 0
            self.load_more_btn.pack(side="left", padx=5)
        data = self.controller.get_history(offset=offset)

        actual_record_count = self.controller.history_record_count()

        if not data:
            self.load_more_btn.pack_forget()
            return 0
        
        for record in data:
            table_row = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            table_row.pack(fill="x", pady=5) 

            for col_idx in range(len(config.TABLE_HEADERS)):
                table_row.grid_columnconfigure(col_idx, weight=1, uniform="column_group")
            
            #Модель
            self.create_label(master=table_row, text=record.model_size, font_size=font_size)\
                .grid(row=0, column=0, padx=10, sticky="nwse")

            #Мова
            self.create_label(master=table_row, text=record.language, font_size=font_size)\
                .grid(row=0, column=1, padx=10, sticky="nwse")

            #FP16
            fp16_val = "Так" if record.fp16 else "Ні"
            self.create_label(master=table_row, text=fp16_val, font_size=font_size)\
                .grid(row=0, column=2, padx=10, sticky="nwse")

            #Preprocessing
            prep_val = "Так" if record.preprocessing else "Ні"
            self.create_label(master=table_row, text=prep_val, font_size=font_size)\
                .grid(row=0, column=3, padx=10, sticky="nwse")
            
            icons_namaes = ["message_light.png", "sheet_light.png", "trash_light.png"]
            icons = []
            for i_name in icons_namaes:

                icon_path = os.path.join(config.ASSETS_DIR, i_name)

                icon = ctk.CTkImage(
                    light_image = Image.open(icon_path),
                    dark_image= Image.open(icon_path.replace("light", "dark")),
                    size=(24, 24)
                )
                icons.append(icon)
            #Кнопка Промпт
            self.create_action_button(table_row, "", icons[0], lambda r_id=record.id: self.controller.open_prompt_viewer(r_id))\
                .grid(row=0, column=4, pady=2, padx=10)

            #Кнопка Результат
            self.create_action_button(table_row, "", icons[1], lambda r_id=record.id: self.controller.open_result_viewer(r_id))\
                .grid(row=0, column=5, pady=2, padx=10)

            #Кнопка Видалити
            self.create_action_button(table_row, "", icons[2], lambda r_id=record.id: self.controller.delete_record(r_id), color="#ff5252", hover_color="#ff1744")\
                .grid(row=0, column=6, pady=2, padx=10)
            
            self.rows[record.id] = table_row

        self.record_on_ui_count += len(data)
        
        actual_total_count = self.controller.history_record_count()
            
        if self.record_on_ui_count >= actual_total_count:
            self.load_more_btn.pack_forget()

    def remove_record_from_ui(self, record_id):
        if record_id in self.rows:
            self.rows[record_id].destroy()
            del self.rows[record_id]    

    def remove_all_records_from_ui(self):
        for record in self.rows.values():
            record.destroy()
            del record
        
    def open_text_viewer(self, title, can_save, content):
        top = ctk.CTkToplevel(self)
        top.title(title)
        top.geometry("600x500")
        top.attributes("-topmost", True)
        top.attributes("-toolwindow", True)
        txt = ctk.CTkTextbox(top, wrap="word")
        txt.pack(expand=True, fill="both", padx=20, pady=20)
        txt.insert("1.0", content)
        txt.configure(state="disabled")

        btn_frame = ctk.CTkFrame(top, fg_color="transparent")
        btn_frame.pack(fill="x", side="bottom", padx=20, pady=(0, 20))
        self.create_button(btn_frame, text="Закрити", command=top.destroy, fg_color=config.SIGNATURE_RED, hover_color=config.SIGNATURE_RED_HOVER).pack(side="right", padx=5)
        
        if can_save:
            self.create_button(master = btn_frame, 
                               text = "Зберегти",
                               command = lambda manual=False: self.controller.save_result(manual)).pack(side="left", padx=5)
            self.create_button(master = btn_frame,
                               text = "Зберегти як",
                               command = lambda manual=True: self.controller.save_result(manual)).pack(side="left", padx=5)
            btn_frame.pack()



