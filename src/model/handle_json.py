import json

def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    
def write_json(file_path, settings):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)
