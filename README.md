
# 🧠 ChatApp – Local LLM Chat with Streamlit + FastAPI + Ollama

ChatApp is a simple and elegant chat interface powered by a **local large language model (LLM)** using [Ollama](https://ollama.com), a FastAPI backend, and a modern UI built with [Streamlit](https://streamlit.io).

---

## 📋 Features

- 💬 Real-time chatting experience
- 🧠 Local LLM (LLaMA 3 or others via Ollama)
- 🎨 Streamlit-based modern chat UI
- 🚀 FastAPI backend for prompt handling
- 🧾 Multiple session support with styled chat bubbles

---

## 🔧 Prerequisites

1. **Install Python (3.8 or above)**
   - [Download Python](https://www.python.org/downloads/)

2. **Install Ollama**
   - Download and install for your OS from:  
     👉 https://ollama.com/download

3. **Pull a Local Language Model (LLM)**
   ```bash
   ollama pull llama3
````

> You can also use other models like `mistral`, `phi`, `gemma`, etc.



## 📦 Install Required Python Packages

From the project folder, run:

```bash
pip install streamlit fastapi uvicorn requests
```

Or using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## 📁 Folder Structure

```
ChatApp/
│
├── chat_ui.py         # Streamlit frontend (UI)
├── api.py             # FastAPI backend (serves LLM responses)
├── requirements.txt   # Python dependencies
└── README.md          # Setup guide and documentation
```

---

## 🚀 Getting Started

### Step 1: Run the FastAPI Backend

Start the backend server that sends prompts to the LLM.

```bash
uvicorn api:app --reload --port 8000
```

This runs on: `http://localhost:8000`

---

### Step 2: Run the Streamlit Frontend

In a new terminal, start the Streamlit UI.

```bash
streamlit run chat_ui.py
```

Then go to: `http://localhost:8501`

---

## ✏️ Customizing the Model

The model name used is `"llama3"` by default.
To switch models, open `api.py` and change:

```python
response = ollama.chat(model="llama3", messages=[...])
```

Replace `"llama3"` with `"mistral"`, `"phi"`, `"gemma"`, etc., depending on which models you’ve pulled via Ollama.

---

## 🧪 Example Usage

1. Open browser at `http://localhost:8501`
2. Type a message like:

   > What's the capital of Germany?
3. The LLM (e.g., LLaMA 3) replies instantly from your local machine!

---

## 🛑 Stop the App

To stop both servers:

* Press `CTRL+C` in the terminals where backend and frontend are running.

---

## 📜 License

This project is intended for personal, educational, and local use only.

---

## 🙌 Credits

* [Ollama](https://ollama.com) – Run local LLMs
* [Streamlit](https://streamlit.io) – Chat UI framework
* [FastAPI](https://fastapi.tiangolo.com) – Backend API

---

> 💡 Tip: You can add avatars, chat export (PDF/TXT), or even database logging for a complete experience!

