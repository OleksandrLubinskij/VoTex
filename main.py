from src.model.model import Model
from src.model.handle_json import read_json, write_json

if __name__ == "__main__":
    m1 = Model()
    print(m1.define_valid_models_for_device())