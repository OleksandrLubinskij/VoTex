import torch
import whisper

print(f"CUDA доступна: {torch.cuda.is_available()}")
model = whisper.load_model("tiny")
print(f"Модель працює на: {model.device}")