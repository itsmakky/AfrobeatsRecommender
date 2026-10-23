# 🎵 Afrobeats Recommender

A full-stack web application that recommends Afrobeats songs based on user mood and activity, powered by the GROQ API.

> 🚧 **Status: Work in Progress** – This project is currently under active development.

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
| **Version Control** | Git, GitHub |

---


## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/itsmakky/AfrobeatsRecommender.git
   cd AfrobeatsRecommender
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Install backend dependencies:
   ```bash
   pip install flask flask-cors groq
   ```

4. Set up your GROQ API key:
   ```bash
   export GROQ_API_KEY=your_api_key_here
   ```

5. Start the backend server:
   ```bash
   python app.py
   ```

6. In a new terminal, start the frontend:
   ```bash
   npm start
   ```


---

## 🗓️ Current Progress

- [x] Project setup and initialization
- [x] React frontend with mood/activity selection
- [x] Flask backend with GROQ API integration
- [x] Song recommendations with YouTube links
- [x] Error handling and loading states
- [x] CSS styling and responsive design
- [x] Testing and bug fixes (Prevented AI hallucinations)
- [ ] Deployment

---

## 📁 Project Structure

```
AfrobeatsRecommender/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   └── README.md
├── backend/
│   ├── app.py
│  
└── .gitignore
```

---

## 👨‍💻 Author

**Makochukwu Frances Ifiorah**
- GitHub: [@itsmakky](https://github.com/itsmakky)
- LinkedIn: [Makochukwu Ifiorah](https://linkedin.com/in/makochukwuifiorah)

---

## 📄 License

This project is for educational purposes only.