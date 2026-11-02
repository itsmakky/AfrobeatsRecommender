# 🎵 Afrobeats Recommender

A full-stack web application that recommends Afrobeats songs based on user mood and activity, powered by the GROQ API.

🔗 **Live Demo:** [https://afrobeats-recommender.vercel.app/](https://afrobeats-recommender.vercel.app/)

---

## 🎯 Project Goal

To build an intuitive web app that helps users discover Afrobeats music tailored to their current mood and activity (e.g., studying, working out, relaxing).

---

## ✨ Features

- **Interactive Landing Screen** – Aesthetic welcome screen that transitions smoothly into the app.
- **Mood-based recommendations** – Select your current mood and get personalized song suggestions.
- **Activity-based filtering** – Get recommendations tailored to what you're doing.
- **AI-powered suggestions** – Uses GROQ API (Llama 3) with **Structured JSON Schema** to generate contextual artist recommendations.
- **Zero Hallucinations** – A custom backend "Gatekeeper" filters out gibberish input, and a local database maps AI-selected artists to real, verified songs.
- **YouTube integration** – Click to listen to recommended songs directly on YouTube.
- **Responsive Aesthetic Design** – Dark purple/black theme with Playfair Display and Inter fonts.

---

## 🛠️ Tech Stack

| Category        | Technologies |
| :--- | :--- |
| **Frontend** | React.js, JavaScript (ES6+), CSS3, Fetch API, Google Fonts |
| **Backend** | Python, Flask, Flask-CORS |
| **AI / APIs** | GROQ API (Llama 3), JSON Schema Structured Outputs |
| **Deployment** | Vercel (Frontend), Render (Backend) |
| **Version Control** | Git, GitHub |

---

## 📦 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/itsmakky/AfrobeatsRecommender.git
   cd AfrobeatsRecommender
