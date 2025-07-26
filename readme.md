# ✨ Triwizardathon: Exyst ✨

Welcome to **Exyst**, the all-in-one AI-powered academic assistant built for the Triwizardathon Hackathon — themed around the magical world of **Harry Potter**. Just like a wizard’s wand, Exyst equips students with tools to conquer the academic battlefield with ease and precision.

## 🧙‍♂️ About the Project

**Exyst** is a mobile + backend solution that helps students:

* 📖 **Generate Personalized Study Plans** based on syllabus, time, and goals.
* 🪡 **Predict Exam Questions** using AI and past year papers.
* 💼 **Craft Impressive Resumes** in minutes.
* ⏳ **Manage Time & Tasks** with an intuitive To-Do and Pomodoro-style planner.

Our mission: Reduce overwhelm, increase clarity, and empower every student like a true Hogwarts champion.

## 🔧 Features

| Feature              | Description                                                                |
| -------------------- | -------------------------------------------------------------------------- |
| Study Plan Generator | Input your subject list & timeline, and get a smart, realistic study path. |
| Exam Paper Predictor | Upload previous year papers and let our model forecast probable questions. |
| Resume Builder       | AI-backed resume generator that highlights your strengths professionally.  |
| Task + Time Manager  | Todo list with reminders and Pomodoro timers to boost focus.               |

## 🧪 Tech Stack

| Tech             | Purpose                      |
| ---------------- | ---------------------------- |
| Flutter          | Frontend mobile app          |
| Python + FastAPI | Backend APIs                 |
| GrokAPI          | LLM-based content generation |
| JWT              | Secure authentication        |

## 🏠 Folder Structure

```
.
├── backend/             # FastAPI app
├── frontend/            # Flutter app
│   ├── assets/
│   
└── Export/  # Downloadable APK inside this folder
├── README.md
└── ...
```

## 📂 How to Run

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend (Flutter)

```bash
cd frontend
flutter pub get
flutter run
```

> **Note:** The compiled Android APK is available in the `export` folder for direct installation.

## 🔮 Team & Credits

Made by the wizards of the Triwizardathon:

* Ananta Agarwal (Design Witch)
* Ashmit Jain (App Wizard)
* Himanshu Jain (Backend + LLM Summoner)
* Adi Jain (Analyst Wizard)

Special thanks to:

* The Triwizardathon organizers
* All Hogwarts houses (yes, even Slytherin)

## 🚀 Future Scope

* Timetable sync with Google Calendar
* AI Interview Prep
* Doubt-solving with voice & OCR
* House Points Leaderboard 🏆

---

> *"Help will always be given at Hogwarts to those who ask for it."* — Albus Dumbledore

Let Exyst be your magical companion through the toughest exams.

**Accio Productivity!** 🪄
