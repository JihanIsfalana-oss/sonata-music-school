import librosa
import numpy as np
import torch

def analyze_vocal(audio_path):
    # 1. Load file audio menggunakan Librosa
    y, sr = librosa.load(audio_path, sr=None)
    
    # 2. Ekstrak fitur dasar: Pitch (nada)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
    # Ambil pitch tertinggi dari audio
    pitch_max = np.max(pitches)
    
    # 3. Ubah ke Tensor PyTorch agar bisa diproses AI nanti
    pitch_tensor = torch.tensor([pitch_max], dtype=torch.float32)
    
    # Logika sederhana: Tentukan range suara
    if pitch_max < 200:
        range_vokal = "Bass/Baritone"
    elif pitch_max < 400:
        range_vokal = "Tenor/Alto"
    else:
        range_vokal = "Soprano"
        
    return {
        "pitch_score": float(pitch_max),
        "category": range_vokal,
        "tensor_data": pitch_tensor
    }

print("Vocal Processor dengan PyTorch & Librosa siap!")