import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

class SonataAI:
    def __init__(self):
        # 1. Tambahkan lebih banyak variasi kata kunci agar lebih akurat
        self.knowledge_base = {
            "salam": ["halo", "hi", "hai", "pagi", "siang", "malam", "oi", "hello"],
            "tanya_kabar": ["apa kabar", "gimana kabarnya", "kabar", "sehat", "how are you", "lagi apa"],
            "identitas": ["siapa kamu", "nama kamu", "kamu siapa", "maestro jihan"],
        }
        
        # Respon santai yang manusiawi
        self.human_responses = {
            "salam": ["Yo, Bro!", "Oi! Ready to rock?", "Halo!"],
            "tanya_kabar": ["Lagi tuning gitar nih, kabar baik!", "Selalu semangat kalau bahas musik!"],
            "identitas": ["Saya Maestro Jihan, asisten musik paling gokil di Sonata!"],
            "puji": ["Wah, selera musikmu paten juga!", "Keren! Itu baru jiwa musisi.", "Mantap!"], 
            "bingung": ["Waduh, monitor pecah nih, bisa diulang?", "Coba tanya soal musik deh!"]
        }

        # 2. Dataset Kurikulum (Smarter Data)
        self.curriculum = pd.DataFrame([
            {"inst": "Gitar", "gen": "Rock", "tips": "Coba latihan power chord 'Iron Man' - Black Sabbath. Jaga jempol tetap di belakang neck!"},
            {"inst": "Gitar", "gen": "Metal", "tips": "Fokus ke down-picking cepat. Coba riff 'Master of Puppets' pelan-pelan dulu."},
            {"inst": "Piano", "gen": "Klasik", "tips": "Mainkan 'Für Elise'. Pastikan dinamika piano dan forte-nya dapet."},
            {"inst": "Drum", "gen": "Jazz", "tips": "Latih 'Ghost Notes' pada snare. Swing feeling-nya harus dapet, jangan kaku!"},
            {"inst": "Vokal", "gen": "Pop", "tips": "Latihan kontrol napas diafragma. Coba nyanyikan nada tinggi tanpa maksa tenggorokan."}
        ])

        # 3. State Management (Memori Manusiawi)
        self.memory = {"step": "intro", "instrumen": None, "genre": None}
        
        # 4. Mesin NLU (TF-IDF untuk mencocokkan kemiripan kalimat)
        self.vectorizer = TfidfVectorizer()
        self.questions = list(self.knowledge_base.keys())
        # Kita buat representasi angka dari kategori pengetahuan
        self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)

    def _get_intent(self, user_msg):
        # Mencari kategori maksud user berdasarkan kemiripan kalimat
        user_vec = self.vectorizer.transform([user_msg.lower()])
        similarities = cosine_similarity(user_vec, self.tfidf_matrix)
        best_match_idx = np.argmax(similarities)
        
        if similarities[0][best_match_idx] > 0.2: # Threshold kemiripan
            return self.questions[best_match_idx]
        return "unknown"

    def get_chatbot_response(self, user_message):
        msg = user_message.lower().strip()
        
        # 1. CEK INTENT UMUM (Agar bisa disela kapan saja)
        if any(word in msg for word in ["kabar", "apa kabar", "how are you", "sehat"]):
            # Kita set step ke ask_instrument agar alurnya jelas setelah jawab kabar
            self.memory["step"] = "ask_instrument" 
            return f"{random.choice(self.human_responses['tanya_kabar'])} Kamu sendiri gimana? Sudah siap menggebrak panggung?"
        
        if any(word in msg for word in ["siapa", "identitas", "nama", "jihan"]):
            return random.choice(self.human_responses["identitas"])

        # 2. LOGIKA ALUR (State Machine)
        
        # Jika user merespon sapaan atau bilang "siap/baik"
        if "halo" in msg or any(word in msg for word in ["siap", "baik", "oke", "gas", "ready"]):
            if self.memory["step"] == "intro" or self.memory["step"] == "ask_instrument":
                self.memory["step"] = "ask_instrument"
                return "Mantap! 🔥 Biar gak salah panggung, kasih tahu saya dulu: Kamu main instrumen apa? (Gitar/Piano/Drum/Vokal)"

        # Menunggu jawaban Instrumen
        if self.memory["step"] == "ask_instrument":
            matched_inst = next((i for i in ["gitar", "piano", "drum", "vokal"] if i in msg), None)
            if matched_inst:
                self.memory["instrumen"] = matched_inst.capitalize()
                self.memory["step"] = "ask_genre"
                pujian = random.choice(self.human_responses.get('puji', ["Mantap!"]))
                return f"Ooh, anak {matched_inst.capitalize()} ternyata! {pujian} Sekarang, genre apa yang bikin kamu semangat? (Rock/Metal/Klasik/Jazz/Pop)"

        # Menunggu jawaban Genre
        if self.memory["step"] == "ask_genre":
            matched_gen = next((g for g in ["rock", "metal", "klasik", "jazz", "pop"] if g in msg), None)
            if matched_gen:
                self.memory["genre"] = matched_gen.capitalize()
                return self._give_final_recommendation()

        # 3. FALLBACK (Jika benar-benar tidak nyambung)
        return random.choice(self.human_responses["bingung"])
    def _give_final_recommendation(self):
        inst = self.memory["instrumen"]
        gen = self.memory["genre"]
        
        # Mencari tips di dataframe
        match = self.curriculum[(self.curriculum['inst'] == inst) & (self.curriculum['gen'] == gen)]
        
        if not match.empty:
            tips = match.iloc[0]['tips']
            res = f"🤘 OK Bro, ini 'Resep Rahasia' buat {inst} {gen} kamu: {tips}"
        else:
            res = f"Waduh, kombinasi {inst} {gen} belum ada di setlist. Tapi saran saya: Latihan basic scales tiap pagi!"

        # Reset Memory setelah selesai satu siklus
        self.memory = {"step": "intro", "instrumen": None, "genre": None}
        return res + "\n\nMau konsultasi lagi? Sapa saya lagi ya!"

sonata_ai = SonataAI()