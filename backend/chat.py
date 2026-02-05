import random
import json
import torch
from ai_engine import SonataChatNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 1. Load Data
with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "models/chatbot_model.pth"
data = torch.load(FILE)

# 2. Setup Model
model = SonataChatNet(data["input_size"], data["hidden_size"], data["output_size"]).to(device)
model.load_state_dict(data["model_state"])
model.eval()

# 3. Logika Chat
bot_name = "Sonata-AI"
print("Mari mengobrol! (ketik 'keluar' untuk berhenti)")

while True:
    sentence = input("Kamu: ")
    if sentence.lower() == "keluar":
        break

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, data["all_words"])
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = data['tags'][predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    
    # Hanya jawab jika tingkat keyakinan AI di atas 75%
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                print(f"{bot_name}: {random.choice(intent['responses'])}")
    else:
        print(f"{bot_name}: Maaf Rocker, aku kurang paham. Bisa tanya soal tes vokal atau daftar guru?")