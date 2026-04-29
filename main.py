from src.model.model import Model
from src.view.main_w import MainFrame
from src.model.handle_json import read_json, write_json

if __name__ == "__main__":
    model = Model()
    view = MainFrame()
    view.set_maximized()
    view.setup_icon()
    print(model.define_valid_models_for_device())

    view.mainloop()