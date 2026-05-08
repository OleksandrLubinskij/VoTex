import threading
import tkinter as tk
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
        self.switch_frame(config.HISTORY_FRAME)
        self.view.frames[config.HISTORY_FRAME].fill_table()
        
    def switch_frame(self, frame):
        self.view.show_frame(frame)
    
    def get_available_models(self):
        return self.model.get_valid_models()
    
    def get_available_languages(self):
        settings = read_json("settings.json")
        return settings["languages"]
    
    def get_history(self):
        try:
            result = self.history_manager.read_records()
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
            print(f"Datasbase error: {e}")

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
        self.delete_all_history()
        self.view.frames[config.HISTORY_FRAME].remove_all_records_from_ui()
        