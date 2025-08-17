# 🧠 Chatbot with Ollama + Flask + Modern UI

A simple **AI-powered chatbot** built with [Ollama](https://ollama.ai/), Flask, and a modern UI that looks and feels like **ChatGPT**.  
This project streams responses in real time (word by word), giving a typing effect, just like ChatGPT.

---

## 🚀 Features
- ✅ ChatGPT-like UI (dark theme, professional look)  
- ✅ Transparent message bubbles (like ChatGPT)  
- ✅ Real-time streaming responses (typing effect)  
- ✅ Backend powered by **Flask**  
- ✅ Uses **Ollama models** (e.g., `llama3`, `mistral`)  
- ✅ Easy to deploy on **Render / Hugging Face Spaces / Localhost**  

---

## 📂 Project Structure

chatbot/
│── app.py # Flask backend
│── templates/
│ └── index.html # Frontend UI
│── static/
│ └── style.css # Styling for UI
│── requirements.txt # Python dependencies
│── README.md # Project documentation


---

## ⚡ Installation & Setup (Local)
 
1️⃣ Clone the repo

git clone https://github.com/atharvakanchan25/chatbot.git
cd chatbot

2️⃣ Create virtual environment
python3 -m venv aimodels
source aimodels/bin/activate   # (Linux/Mac)
aimodels\Scripts\activate      # (Windows)

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Install Ollama

Download Ollama and install it.
Then pull a model (e.g., Llama 3):

5️⃣ Run the Flask app
python app.py


Now visit 👉 http://127.0.0.1:5000/ in your browser.
You should see your chatbot UI working.

🌍 Deployment Guide
🔹 Deploy on Render

Push your code to GitHub

Go to Render

Create a Web Service → connect your repo

Set:

Start command:

gunicorn app:app


Environment: Python 3

Click Deploy 🎉

Your app will be live on a free Render URL like:
https://your-chatbot.onrender.com

💡 Usage

Type your question in the input box

Press Enter → see the AI typing the response in real-time

🔮 Future Improvements

 Add user authentication

 Support multiple models (choose from dropdown)

 Chat history saving

 Voice input/output

🤝 Contributing

Pull requests are welcome!

📜 License

This project is licensed under the MIT License.
