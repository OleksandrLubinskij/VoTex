import threading
from src.view.main_w import MainFrame
from src.model.model import ModelTransrib
from src.model.handle_json import read_json, write_json

class Controller:
    def __init__(self):
        self.model = ModelTransrib() 
        self.main_frame = MainFrame(controller=self)

        self.main_frame.set_maximized()
        self.main_frame.setup_icon()

        self.transcrib_thread = threading.Thread(
            target=self.model.transcrib,  
            daemon=True
        )
    def start_transcribation(self):
        params = self.main_frame.compile_parameters()
        self.model.set_params(**params)
        print(self.model.get_all_settings())
        self.transcrib_thread.start()

    def get_available_models(self):
        return self.model.get_valid_models()
    
    def get_available_languages(self):
        settings = read_json("settings.json")
        return settings["languages"]