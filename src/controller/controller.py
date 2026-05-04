import threading
from src.view.main_w import MainFrame
from src.view.view import View
from src.model.model import ModelTransrib
from src.model.handle_json import read_json, write_json
import src.config as config

class Controller:
    def __init__(self):
        self.model = ModelTransrib() 
        self.view = View(controller=self)

        self.view.set_maximized()
        self.view.setup_icon()

        self.transcrib_thread = threading.Thread(
            target=self.model.transcrib,  
            daemon=True
        )
    def start_transcribation(self):
        params = self.view.frames[config.MAIN_FRAME].compile_parameters()
        self.model.set_params(**params)
        print(self.model.get_all_settings())
        self.transcrib_thread.start()
        self.view.show_frame(config.PROCESSING)
        processing_frame = self.view.frames[config.PROCESSING]
        processing_frame.processing_progressbar.start()

    def get_available_models(self):
        return self.model.get_valid_models()
    
    def get_available_languages(self):
        settings = read_json("settings.json")
        return settings["languages"]