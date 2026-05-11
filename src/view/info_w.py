import customtkinter as ctk
import tkinter as tk
from src.view.base_view import BaseView
import src.config as config

class InfoFrame(BaseView):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.configure(fg_color="#f0f8ff")

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True, fill="both", padx=20, pady=20)

        self.title_label = self.create_label(self.main_container, text="Довідник параметрів")
        self.title_label.configure(font=("Segoe UI", 32, "bold"))
        self.title_label.pack(anchor="w", pady=(0, 20), padx=10)

        info_data = [
            ("Розмір моделі", 
             "Ші який транскрибує медіа-файли(Whisper) має кілька моделей: tiny, base, small, medium, large. "
             "Чим більша модель, тим вища точність, але вона потребує більше відеопам'яті (VRAM). "),
            
            ("Мова", 
             "Хоча модель вміє визначати мову автоматично, її ручний вибір (наприклад, 'uk') "
             "дозволяє уникнути помилок на початку запису та пришвидшує ініціалізацію моделі."),
            
            ("Режим FP16", 
             "Використання 16-бітних чисел замість 32-бітних. Це дозволяє вдвічі економити "
             "відеопам'ять та значно пришвидшує обробку на відеокартах NVIDIA, але з втратою якості."),
            
            ("Препроцесинг", 
             "Попередня обробка аудіо. Вона нормалізує гучність, видаляє шуми "
             "та конвертує файл у формат 16кГц, який є рідним для нейромережі."
             "Не рекомендується використовувати для файлів з хорошою якістю запису,"
             "оскільки це лише спотворить запис."),
            
            ("Початковий промпт", 
             "Це підказка для моделі. Тут можна вказати контекст (наприклад, 'технічна лекція') "
             "або специфічні терміни. Це допомагає моделі правильно розставляти розділові знаки "
             "та не вигадувати слова.")
        ]


        for title, description in info_data:
            self.create_info_card(title, description)

    def create_info_card(self, title, text):
        card = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15, 
                            border_width=1, border_color="#e0e0e0")
        card.pack(fill="x", pady=10, padx=10)
        title_lbl = self.create_label(card, text=title, font_size=20, weight="bold")
        title_lbl.configure(text_color="#40c057") # Твій фірмовий зелений
        title_lbl.pack(anchor="w", padx=20, pady=(15, 5))
        desc_lbl = self.create_label(card, text=text, font_size=16, weight="normal")
        desc_lbl.configure(wraplength=650, justify="left", text_color="#333333")
        desc_lbl.pack(anchor="w", padx=20, pady=(0, 15))