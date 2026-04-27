import whisper
import torch
import gc
import os
import subprocess
import src.config as config

class Model:
    def __init__(self):
        self._current_file_path = None
        self._save_directory = ""
        self._valid_models = []
        self._model_size = "base"
        self._language = "uk"
        self._fp16 = True if torch.cuda.is_available() else False
        self._prompt = ""
        self._use_preprocessing = False
        self._loaded_instance = None
        self._device = config.CUDA if torch.cuda.is_available() else config.CPU

    def get_all_settings(self):
        return {
            "file_path": self._current_file_path,
            "save_dir": self._save_directory,
            "model_size": self._model_size,
            "language": self._language,
            "fp16": self._fp16,
            "use_preprocessing": self._use_preprocessing,
            "device": self._device,
            "model_loaded": self._loaded_instance is not None
        }

    def get_vram_info(self):
        properties = torch.cuda.get_device_properties(0)

        total_gb = properties.total_memory / (1024**3)
        allocated_gb = torch.cuda.memory_allocated(0)
        reserved_gb = torch.cuda.memory_reserved(0) / (1024**3)

        return {
            "total": round(total_gb, 2),
            "allocated": round(allocated_gb, 2),
            "reserved": round(reserved_gb, 2),
            "free_approx": round(total_gb - reserved_gb, 2)
        }
    
    def define_valid_models_for_device(self):
        if self._device == config.CPU:
            return config.MODELS_FOR_CPU
        
        total_memory = self.get_vram_info()["total"]
        valid_models = []
        for key, val in config.WHISPER_MODELS_VRAM.items():
            if total_memory + 1.5 >= val:
                valid_models.append(key)
        return valid_models
    
    def set_current_file_path(self, path: str):
        self._current_file_path = path
    
    def set_save_dirrectory(self, path: str):
        self._save_directory = path

    def set_valid_models(self):
        self._valid_models = self.define_valid_models_for_device()

    def set_language(self, language: str):
        self._language = language
    
    def set_fp16(self, value: bool):
        self._fp16 = value
    
    def set_prompt(self, prompt: str):
        self._prompt = prompt
    
    def set_use_preprocessing(self, value: bool):
        self._use_preprocessing = value
    
    def get_load_model(self, size):
        if self._loaded_instance and self._model_size == size:
            return
        elif self._loaded_instance and self._model_size != size:
            del self._loaded_instance
            self._loaded_instance = None
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                print(f"Пам'ять очищено від моделі {self._model_size}")
        print(f"Початок завантаження моделі {size}")
        self._model_size = size
        self._loaded_instance = whisper.load_model(self._model_size, device=self._device)

    def preprocess_content(self, input_path):
        print("Покращення якості звуку")
        temp_audio = os.path.join(os.path.dirname(input_path), "temp_processed.wav")
        filters = "highpass=f=100, loudnorm, afftdn = nf = -50"
        cmd = [
            "ffmpeg", "-i", f"{self._current_file_path}",
            "-af", filters,
            "-ar", "16000",
            "-ac", "1",
            "-y", temp_audio
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return temp_audio
        except subprocess.CalledProcessError as e:
            print(f"Помилка FFmpeg {e}")
            return input_path

    def transcrib(self, model_size="medium"):
        self.get_load_model(model_size)
        file_path = self._current_file_path
        if self._use_preprocessing:
            file_path = self.preprocess_content(self._current_file_path)

        result = self._loaded_instance.transcribe(file_path,
                                                  language=self._language,
                                                  fp16=self._fp16,
                                                  initial_prompt=self._prompt)
        self.return_result(result["segments"])

    def return_result(self, transcrib_output):
        for x in transcrib_output:
            print(f"{round(x['start'])} - {round(x['end'])}\t{x['text']}")
