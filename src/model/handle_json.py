import json

def read_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)
    
def write_json(file_path, settings):
    with open(file_path, "w") as file:
        settings_json = json.dumps(settings)
        file.write(settings_json)
