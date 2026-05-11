import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from src.view.view import View
from src.model.model import ModelTransrib
from src.model.handle_json import read_json, write_json
import src.config as config
from datetime import datetime
import os
from src.model.history_management import HistoryManager

class Controller:
    def __init__(self):
        self.model = ModelTransrib() 
        self.view = View(controller=self)

        self.history_offset = 0
        self.history_manager = HistoryManager()
        self.view.set_maximized()
        self.view.setup_icon()

        
    def start_transcribation(self):
        self.model.is_busy = True
        self.model.result = None

        params = self.view.frames[config.MAIN_FRAME].compile_parameters()
        self.model.set_params(**params)
        self.view.frames[config.RESULT_FRAME].prepare_for_new_task()
        transcribe_thread = threading.Thread(
            target=self.model.transcribe,  
            daemon=True
        )
        transcribe_thread.start()
        self.switch_frame(config.RESULT_FRAME)
        self.view.set_current_frame(config.RESULT_FRAME)
        self.check_for_result()
        
        
    def check_for_result(self):
        if not self.model.is_busy:
            self.view.frames[config.RESULT_FRAME].display_result(self.model.result)
            data = self.model.get_trinscribe_data()
            self.write_history(data)
            self.model.result = None
        else:
            self.view.after(200, self.check_for_result)

    def save_result(self, manual):
        if manual:
            path = tk.filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Оберіть куди зберегти"
        )
        else:
            path = read_json("settings.json")["save_path"]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"transcription_{timestamp}.txt"
            path = os.path.join(path, filename)

        content = self.view.frames[config.RESULT_FRAME].result_textbox.get("1.0", "end-1c")
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)
    
    def open_history(self):
        current_frame = self.view.get_current_frame()
        if current_frame != config.HISTORY_FRAME:
            self.history_offset = 0 
            self.view.frames[config.HISTORY_FRAME].record_on_ui_count = 0
            self.switch_frame(config.HISTORY_FRAME)
            self.view.frames[config.HISTORY_FRAME].fill_table(load_more=False, offset=0)
            self.view.set_current_frame(config.HISTORY_FRAME)
        else:
            self.handle_back_to_main_frame()
        
    def switch_frame(self, frame):
        settings_f = self.view.frames[config.SETTINGS_FRAME]
        if self.view.get_current_frame() == config.SETTINGS_FRAME and settings_f.check_for_changes():

            choice = messagebox.askyesno(
                title="Незбережені зміни",
                message="Ви змінили налаштування. Зберегти їх перед виходом?"
            )
            
            if choice is True: 
                self.handle_save_settings()
            elif choice is False:
                settings_f.set_actual_settings()

        self.view.show_frame(frame)
        self.view.set_current_frame(frame)
    
    def get_available_models(self):
        return self.model.get_valid_models()
    
    def get_settings(self):
        settings = read_json("settings.json")
        return settings
    
    def get_available_languages(self):
        return self.model.get_available_languages()
    
    def get_history(self, offset):
        try:
            result = self.history_manager.read_records(offset=offset)
        except Exception as e:
            result = "Щось пішло не так ):"
            print(f"Datasbase error: {e}")
        finally:
            return result
    
    def get_history_prompt(self, id):
        try:
            result = self.history_manager.read_prompt(id)
        except Exception as e:
            result = "Щось пішло не так ):"
            print(f"Datasbase error: {e}")
        finally:
            return result
        
    def get_history_result(self, id):
        try:
            result = self.history_manager.read_result(id)
        except Exception as e:
            result = "Щось пішло не так ):"
            print(f"Datasbase error: {e}")
        finally:
            return result
        
    def write_history(self, data):
        try:
            self.history_manager.create_record(**data)
        except Exception as e:
            print(f"Datasbase error: {e}")

    def delete_all_history(self):
        try:
            self.history_manager.delete_all()
        except Exception as e:
            print(f"Datasbase error: {e}")

    def delete_history_record_by_id(self, id):
        try:
            self.history_manager.delete_by_id(id)
        except Exception as e:
            print(f"Database error: {e}")

    def load_more_history(self):
        self.history_offset += 10
        self.view.frames[config.HISTORY_FRAME].fill_table(load_more=True, offset=self.history_offset)

    def history_record_count(self):
        try:
            return self.history_manager.get_total_records_count()
        except Exception as e:
            print(f"Database error: {e}")
            return 0

    def open_prompt_viewer(self, id):
        prompt = self.get_history_prompt(id)
        self.view.frames[config.HISTORY_FRAME].open_text_viewer(title="Promt", can_save=False, content=prompt)

    def open_result_viewer(self, id):
        result = self.get_history_result(id)
        self.view.frames[config.HISTORY_FRAME].open_text_viewer(title="Result", can_save=True, content=result)
    
    def delete_record(self, id):
        self.delete_history_record_by_id(id)
        self.view.frames[config.HISTORY_FRAME].remove_record_from_ui(id)
    
    def delete_all_records(self):
        is_confirmed = messagebox.askyesno(
            title="Підтвердження видалення",
            message="Ви впевнені що хочете видалити усі записи з історії?"
        )
        if is_confirmed:
            self.delete_all_history()
            self.view.frames[config.HISTORY_FRAME].remove_all_records_from_ui()

    def handle_back_to_main_frame(self):
        self.switch_frame(config.MAIN_FRAME)
        self.view.set_current_frame(config.MAIN_FRAME)

    def handle_open_settings(self):
        current_frame = self.view.get_current_frame()
        if current_frame != config.SETTINGS_FRAME:
            self.switch_frame(config.SETTINGS_FRAME)
            self.view.frames[config.SETTINGS_FRAME].set_actual_settings()
            self.view.set_current_frame(config.SETTINGS_FRAME)
        else:
            self.handle_back_to_main_frame()
    
    def handle_open_info(self):
        current_frame = self.view.get_current_frame()
        if current_frame != config.INFO_FRAME:
            self.switch_frame(config.INFO_FRAME)
            self.view.set_current_frame(config.INFO_FRAME)
        else:
            self.handle_back_to_main_frame()
        
    def browse_file(self):
        file_path = tk.filedialog.askopenfilename(
            title="Оберіть файл",
            filetypes=[("Медіа файли", "*.mp3 *.wav *.m4a *.mp4 *.mkv *.avi *.ogg *m4a")]
        )
        if file_path:
            self.view.frames[config.MAIN_FRAME].file_name_var.set(os.path.basename(file_path))
            self.view.frames[config.MAIN_FRAME].file_path_var.set(file_path)

    def browse_directory(self):
        selected_path = filedialog.askdirectory(
            initialdir=os.getcwd(),
            title="Оберіть папку за замовчуванням"
        )

        if selected_path:
            self.view.frames[config.SETTINGS_FRAME].path_var.set(selected_path)
    
    def handle_save_settings(self):
        settings_frame = self.view.frames[config.SETTINGS_FRAME]
        new_settings = settings_frame.save_settings()
        write_json(config.SETTINGS_PATH, new_settings)
        settings_frame.old_settings = new_settings
        settings_frame.is_change = False
        settings_frame.save_and_notify()
        new_lang_names = list(new_settings[config.LANGUAGES_KEY].values())
        main_f = self.view.frames[config.MAIN_FRAME]
        main_f.available_languages = new_settings[config.LANGUAGES_KEY]
        main_f.main_content.parameters_frame.update_lang_options(new_lang_names)
        settings_frame.is_change = False