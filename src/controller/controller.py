import threading
import tkinter as tk
from src.view.view import View
from src.model.model import ModelTransrib
from src.model.handle_json import read_json, write_json
import src.config as config
from datetime import datetime
import os

class Controller:
    def __init__(self):
        self.model = ModelTransrib() 
        self.view = View(controller=self)

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
            res = self.model.format_segments_to_text(self.model.result)
            self.view.frames[config.RESULT_FRAME].display_result(res)
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
    
    def switch_frame(self, frame):
        self.view.show_frame(frame)
    
    def get_available_models(self):
        return self.model.get_valid_models()
    
    def get_available_languages(self):
        settings = read_json("settings.json")
        return settings["languages"]