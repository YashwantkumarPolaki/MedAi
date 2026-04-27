# MediAI – AI-Driven Healthcare Chatbot

A glassmorphism-themed medical triage chatbot with a **Node.js NLP backend** and a **vanilla JS frontend**. No cloud API keys required — all symptom detection, triage scoring, and condition matching runs locally.

---

## Project Structure

```
AI Driven Healthcare/
├── backend/
│   ├── server.js              ← Express API server (port 3000)
│   ├── package.json
│   └── nlp/
│       ├── engine.js          ← Core NLP: detection, triage, matching
│       ├── symptoms-db.js     ← 50+ symptoms with keywords & severity
│       ├── conditions-db.js   ← 35+ medical conditions
│       └── response-gen.js    ← Empathetic message templates & tips
└── frontend/
    ├── index.html             ← Main UI (open in browser)
    ├── css/
    │   └── style.css
    └── js/
        ├── api.js             ← fetch() calls to backend
        ├── ui.js              ← All DOM rendering helpers
        ├── chat.js            ← Chat state, session, history
        └── app.js             ← Entry point, nav, event wiring
```

---

## Quick Start

### 1. Install backend dependencies

```bash
cd backend
npm install
```

### 2. Start the backend server

```bash
npm start
# or for auto-reload during development:
npm run dev
```

You should see:
```
  ✅  MediAI NLP Backend running at http://localhost:3000
  📡  POST  http://localhost:3000/api/chat
  💓  GET   http://localhost:3000/api/health
```

### 3. Open the frontend

Open `frontend/index.html` directly in your browser (double-click or drag into Chrome/Edge/Firefox).

> The sidebar shows a green **NLP Server Online** dot when the backend is reachable.

---

## How the NLP Works

| Step | Description |
|------|-------------|
| **Tokenisation** | Input is lowercased and normalised |
| **Keyword matching** | Each symptom has 10–15 phrase variants matched with word-boundary regex |
| **Negation detection** | Checks 50 chars before a match for words like *no*, *not*, *don't*, *without* |
| **Intensity modifiers** | Words like *severe*, *extreme* → severity ×1.35 · *mild*, *slight* → severity ×0.68 |
| **Triage scoring** | Max severity ≥7 → EMERGENCY · ≥6 or avg >5 → HIGH · avg ≥3 → MODERATE · else LOW |
| **Condition matching** | Each condition has key + supporting symptom IDs; matched conditions scored by overlap ratio |
| **Session accumulation** | Symptoms accumulate across turns in the same session (in-memory, 30-min TTL) |

---

## API Endpoints

| Method | Path | Body | Description |
|--------|------|------|-------------|
| `GET` | `/api/health` | — | Server health check |
| `POST` | `/api/chat` | `{ message, sessionId }` | Analyse message, return triage result |
| `DELETE` | `/api/session/:id` | — | Clear accumulated session state |

### Example request

```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"I have severe chest pain and shortness of breath","sessionId":"abc123"}'
```

### Example response

```json
{
  "success": true,
  "data": {
    "message": "I'm genuinely concerned about the symptoms you're describing...",
    "symptoms": [
      { "id": "chest_pain",    "name": "Chest Pain",    "severity": 7 },
      { "id": "breathlessness","name": "Breathlessness","severity": 5 }
    ],
    "urgency": "EMERGENCY",
    "urgency_message": "Seek emergency care immediately — call 911 or go to the nearest ER.",
    "conditions": [
      { "name": "Myocardial Infarction (Heart Attack)", "probability": 78, "specialty": "Cardiologist" }
    ],
    "specialty": "Cardiologist",
    "tips": ["Call emergency services (911/112) immediately — do not wait.", "..."],
    "disclaimer": "Always consult a qualified healthcare professional for medical advice."
  }
}
```

---

## Features

- **50+ symptoms** with multi-keyword NLP matching
- **35+ medical conditions** with probabilistic scoring
- **4 urgency levels**: LOW / MODERATE / HIGH / EMERGENCY
- **Session memory**: symptoms accumulate across chat turns
- **Doctor directory**: 12 specialists, filtered by recommended specialty
- **Chat history**: saved to `localStorage`, readable in-app
- **Glassmorphism dark UI**: animated blobs, SVG triage ring, animated progress bars
- **Zero cloud dependencies**: runs 100% offline once `npm install` is done

---

## Requirements

- Node.js ≥ 18 (for `fetch` and `crypto.randomUUID`)
- A modern browser (Chrome, Edge, Firefox, Safari)
