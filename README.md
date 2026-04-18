# 🧠 TriageX — AI-Powered Visual Medical Triage Assistant

> **"Explain. Assess. Act."**

TriageX is an intelligent healthcare pre-triage platform that collects symptoms via an interactive chat interface, uses AI + rule-based logic to assess severity, and generates visual explanations with structured clinical reports.

![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)
![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC?logo=tailwind-css)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)

---

## ✨ Features

### Core
- 🗣️ **Conversational Symptom Intake** — Chat-style UI for guided symptom collection
- 🧠 **AI Triage Engine** — 25+ clinical rules with NLP-powered symptom extraction
- 📊 **Severity Scoring** — 0-100 score with LOW/MEDIUM/HIGH urgency levels
- 💡 **Explainable AI** — Transparent reasoning showing triggered rules and key factors

### Visual Intelligence
- 🫀 **Interactive Body Mapping** — SVG human body with dynamic region highlighting
- 🎯 **Severity Gauge** — Animated semi-circular gauge with color-coded severity
- 🖼️ **Condition Illustrations** — Mapped medical illustrations for detected conditions

### Additional
- 📄 **PDF Report Generation** — Structured clinical PDF reports with ReportLab
- 🌐 **Multi-language** — English + Tamil support
- 🌙 **Dark Mode** — Full dark/light theme toggle
- 🎤 **Voice Input** — Web Speech API for voice-based symptom input
- 🔐 **JWT Authentication** — User registration and login
- 👨‍⚕️ **Admin Dashboard** — View, filter, and search all triage cases
- ⚠️ **Emergency Alerts** — Critical symptom detection with emergency override

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router), TypeScript, Tailwind CSS |
| Animations | Framer Motion |
| Charts | Chart.js |
| Backend | Python FastAPI, Pydantic |
| AI Engine | NLP (keyword-based) + Rule-based triage |
| Database | SQLite (dev) / PostgreSQL (prod) |
| PDF | ReportLab |
| Auth | JWT (python-jose + passlib) |

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.10+
- **pip**

### 1. Clone the repository
```bash
git clone https://github.com/madhumithadasarathy/triageX.git
cd triageX
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run the dev server
npm run dev
```

The frontend will be available at `http://localhost:3000`

---

## 📁 Project Structure

```
triageX/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Settings & configuration
│   │   ├── database.py          # SQLAlchemy setup
│   │   ├── routes/              # API endpoints
│   │   │   ├── triage.py        # Triage & chat endpoints
│   │   │   ├── auth.py          # JWT authentication
│   │   │   ├── admin.py         # Dashboard APIs
│   │   │   ├── reports.py       # PDF generation
│   │   │   └── translations.py  # i18n endpoints
│   │   ├── services/            # Business logic
│   │   │   ├── nlp_module.py    # Symptom extraction
│   │   │   ├── triage_engine.py # Rule-based scoring
│   │   │   ├── explanation_engine.py # XAI reasoning
│   │   │   ├── visual_mapper.py # Body mapping
│   │   │   └── report_generator.py  # PDF reports
│   │   ├── models/              # DB models & schemas
│   │   └── data/                # Rules, categories, translations
│   └── tests/
│
├── frontend/
│   └── src/
│       ├── app/                 # Next.js pages
│       │   ├── page.tsx         # Landing page
│       │   ├── chat/            # Chat interface
│       │   ├── results/         # Results dashboard
│       │   ├── admin/           # Admin dashboard
│       │   └── login/           # Authentication
│       ├── components/          # React components
│       │   ├── BodyDiagram.tsx  # SVG body map
│       │   ├── SeverityGauge.tsx # Animated gauge
│       │   ├── ReasoningPanel.tsx # XAI display
│       │   └── ...
│       └── services/            # API client
```

---

## 🧪 Running Tests

```bash
cd backend
python tests/test_triage_engine.py
```

---

## 🔐 Safety

- ⚠️ Always displays disclaimer: "TriageX is not a diagnostic tool"
- 🚨 Emergency override with alert banner for critical symptoms
- 📋 All outputs include medical consultation recommendations

---

## ⚠️ Disclaimer

**TriageX is NOT a diagnostic tool.** It is a pre-triage decision-support system designed for educational and demonstration purposes. Always consult a qualified medical professional for proper diagnosis and treatment.

---

## 📝 License

MIT License — Free for educational and commercial use.

---

Built with ❤️ by **Madhumitha Dasarathy**
