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
HISTORY_FRAME = "HistoryFrame"
SETTINGS_FRAME = "SettingsFrame"
INFO_FRAME = "InfoFrame"

CURRENT_OS = platform.system()
current_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(current_dir)


ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DB_PATH = os.path.join(BASE_DIR, "history.db")
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")

TABLE_HEADERS = ("Модель", "Мова", "FP16", "Prep", "Промпт", "Результат", "")

THEMES = {"Світла": "light", "Темна": "dark"}


DEFAULT_SAVE_PATH_KEY = "save_path"
LANGUAGES_KEY = "languages"
THEME_KEY = "theme"

TEXT_COLOR = ("#000000", "#f0f8ff")
FG_COLOR = ("#f0f8ff", "#504B4B")
SIGNATURE_GREEN = ("#40c057", "#2e9641")
SIGNATURE_GREEN_HOVER = ("#31b249", "#238535")
TEXT_BOX_COLOR = ("#ffffff", "#6E6969")
SIGNATURE_RED = ("#ff5252", "#da4040")
SIGNATURE_RED_HOVER = ("#ff1744", "#e7143e")