# ☕ LLM-Based NPC Café System (Unity + FastAPI)

An AI-powered NPC system for games where a café receptionist interacts with players using natural language, dynamic behavior, and a real-time backend.

## 🚀 Features

* 🧠 LLM-powered dialogue (natural conversations)
* 🎯 Intent detection (order, confirm, cancel, etc.)
* 😊 Behavior-based rating system
* 🛒 Inventory management
* 💰 Dynamic pricing (discounts & penalties)
* 🔒 Transaction-safe price locking
* 🧾 Purchase history tracking
* 🎮 Unity integration via REST API

## 🏗️ Architecture

Player (Unity) → FastAPI Backend → LLM → Game Logic → Response

## 📦 Tech Stack

* Python (FastAPI)
* OpenAI API
* Unity (C#)
* JSON-based communication

## ⚙️ Setup Instructions

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Unity

* Open the `unity/` folder in Unity Hub
* Run the scene
* Ensure backend is running at `http://127.0.0.1:8000`

## 📌 Example API Response

```json
{
  "reply": "Great! Here's your coffee. Enjoy!",
  "rating": 9,
  "consequence": "discount",
  "inventory": {
    "coffee": 1,
    "tea": 1,
    "bread": 0
  },
  "prices": {
    "coffee": 9,
    "tea": 9,
    "bread": 13
  },
  "purchase_price": 9
}
```

## 🎯 Future Improvements

* Chat history UI
* NPC animations based on mood
* Player wallet system
* Multiplayer support

## 👤 Author

Chinmay Gawas

