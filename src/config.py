import os
import platform
WHISPER_MODELS_VRAM = {
    "tiny": 1.0,
    "tiny.en": 1.0,
    "base": 1.0,
    "base.en": 1.0,
    "small": 2.0,
    "small.en": 2.0,
    "medium": 5.0,
    "medium.en": 5.0,
    "large": 10.0,
    "large-v1": 10.0,
    "large-v2": 10.0,
    "large-v3": 10.0,
    "turbo": 6.0
}

MODELS_FOR_CPU = ["tiny", "tiny.en", "base", "base.en", "small", "small.en"]

CPU = "cpu"
CUDA = "cuda"

WINDOWS = "Windows"
LINUX = "Linux"
MACOS = "Darwin"

MAIN_FRAME = "MainFrame"
RESULT_FRAME = "ResultFrame"

CURRENT_OS = platform.system()
current_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(current_dir)

# Тепер асети будуть шукатися правильно
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DB_PATH = os.path.join(BASE_DIR, "history.db")