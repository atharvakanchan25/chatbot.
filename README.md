# 🧠 Chatbot with Ollama + Flask + Modern UI
A simple **AI-powered chatbot** built with [Ollama](https://ollama.ai/), Flask, and a modern UI that looks and feels like **ChatGPT**. This project streams responses in real time (word by word), giving a typing effect, just like ChatGPT.

## 🚀 Features
- ✅ ChatGPT-like UI (dark theme, professional look)  
- ✅ Transparent message bubbles (like ChatGPT)  
- ✅ Real-time streaming responses (typing effect)  
- ✅ Backend powered by **Flask**  
- ✅ Uses **Ollama models** (e.g., `llama3`, `mistral`)  
- ✅ Easy to deploy on **Render / Hugging Face Spaces / Localhost**  

## 📂 Project Structure
<img width="464" height="236" alt="image" src="https://github.com/user-attachments/assets/a586563d-739b-463a-83b4-e930fdbfc07b" />


## ⚡ Installation & Setup (Local)
### 1️⃣ Clone the repo
```bash
git clone https://github.com/atharvakanchan25/chatbot.git
cd chatbot

python3 -m venv aimodels
source aimodels/bin/activate   # (Linux/Mac)
aimodels\Scripts\activate      # (Windows)

pip install -r requirements.txt

python app.py
