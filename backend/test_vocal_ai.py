from vocal_processor import analyze_vocal
import os

# Ganti 'suara_jihan.wav' dengan nama file audio kamu yang ada di folder backend
file_audio = "Saat Saat Itu - Last Child.mp3" 

if os.path.exists(file_audio):
    print(f"Menganalisis file: {file_audio}...")
    hasil = analyze_vocal(file_audio)
    
    print("\n--- HASIL ANALISIS AI SONATA ---")
    print(f"Pitch Score (Hz) : {hasil['pitch_score']:.2f}")
    print(f"Kategori Suara   : {hasil['category']}")
    print(f"Tensor Data (AI) : {hasil['tensor_data']}")
    print("---------------------------------")
    
    if hasil['category'] == "Soprano":
        print("Saran AI: Kamu cocok banget masuk kelas Pop-Opera!")
    else:
        print("Saran AI: Suara kamu punya karakter kuat untuk kelas Rock/Blues!")
else:
    print(f"Error: File {file_audio} tidak ditemukan di folder backend!")