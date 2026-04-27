"""Core NLP engine — symptom detection, triage scoring, condition matching."""
from __future__ import annotations
import re
from typing import Optional
from .symptoms_db import SYMPTOMS_DB
from .conditions_db import CONDITIONS_DB

# ── Negation ────────────────────────────────────────────────────────────────
_NEGATION_RX = [
    re.compile(p, re.IGNORECASE) for p in [
        r"\bno\b", r"\bnot\b", r"\bnever\b", r"\bwithout\b", r"\babsence\b",
        r"\bdon['\u2019]?t\b", r"\bdont\b", r"\bdoesn['\u2019]?t\b", r"\bdoesnt\b",
        r"\bhaven['\u2019]?t\b", r"\bhasn['\u2019]?t\b",
        r"\bdenied?\b", r"\blacking?\b", r"\bfree\s+of\b", r"\bno\s+sign\b",
    ]
]
_CLAUSE_BOUNDARY_RX = re.compile(
    r"[,;.]|\b(but|however|although|though|yet|and\s+i|while)\b", re.IGNORECASE
)


def _is_negated(text: str, keyword_start: int) -> bool:
    window = text[max(0, keyword_start - 60):keyword_start]
    # clip at last clause boundary so "no headache, but I have fever" doesn't block fever
    boundaries = list(_CLAUSE_BOUNDARY_RX.finditer(window))
    if boundaries:
        window = window[boundaries[-1].end():]
    return any(rx.search(window) for rx in _NEGATION_RX)


# ── Intensity modifiers ──────────────────────────────────────────────────────
_AMPLIFIERS = re.compile(
    r"\b(severe|extreme(ly)?|intense(ly)?|terrible|horrible|excruciating|unbearable|"
    r"very|really|extremely|badly?|worst|awful|acute|sharp|constant|chronic|"
    r"persistent|splitting|pounding|throbbing|crushing)\b", re.IGNORECASE
)
_DIMINISHERS = re.compile(
    r"\b(mild|slightly?|minor|a\s+little|somewhat|barely|gently?|"
    r"low[\s-]?grade|soft|just\s+a|a\s+bit|slight|not\s+too)\b", re.IGNORECASE
)


def _intensity_multiplier(text: str, keyword_start: int) -> float:
    window = text[max(0, keyword_start - 55):keyword_start + 20]
    if _AMPLIFIERS.search(window):
        return 1.35
    if _DIMINISHERS.search(window):
        return 0.68
    return 1.0


# ── Symptom detection ────────────────────────────────────────────────────────

def detect_symptoms(raw_text: str, nlp_tokens: Optional[dict] = None) -> list[dict]:
    """
    Detect symptoms in raw_text using keyword matching + optional compromise.js
    nlp_tokens for enhanced body-part / adjective hints.
    """
    text = raw_text.lower().replace("\u2019", "'").replace("\u2018", "'")
    detected: list[dict] = []
    used_ids: set[str] = set()

    for symptom in SYMPTOMS_DB:
        if symptom["id"] in used_ids:
            continue

        match_index = -1
        for kw in symptom["keywords"]:
            escaped = re.escape(kw)
            m = re.search(rf"(?<![a-z]){escaped}(?![a-z])", text, re.IGNORECASE)
            if m:
                match_index = m.start()
                break

        if match_index == -1:
            continue

        if _is_negated(text, match_index):
            continue

        multiplier = _intensity_multiplier(text, match_index)
        severity   = min(7, max(1, round(symptom["base_severity"] * multiplier)))

        detected.append({
            "id":          symptom["id"],
            "name":        symptom["name"],
            "severity":    severity,
            "description": symptom["description"],
            "system":      symptom["system"],
        })
        used_ids.add(symptom["id"])

    return detected


# ── Triage ───────────────────────────────────────────────────────────────────

_URGENCY_MESSAGES = {
    "EMERGENCY": "Seek emergency care immediately - call 911 or go to the nearest ER.",
    "HIGH":      "See a doctor today. Your symptoms require prompt medical attention.",
    "MODERATE":  "Schedule a doctor appointment within 2-3 days.",
    "LOW":       "Monitor symptoms at home. Rest and stay hydrated.",
}


def calculate_triage(symptoms: list[dict]) -> dict:
    if not symptoms:
        return {"level": "LOW", "score": 0.0, "maxScore": 0,
                "message": _URGENCY_MESSAGES["LOW"]}

    sevs    = [s["severity"] for s in symptoms]
    max_sev = max(sevs)
    avg_sev = sum(sevs) / len(sevs)
    score   = round(avg_sev * 10) / 10

    if max_sev >= 7:         level = "EMERGENCY"
    elif max_sev >= 6 or avg_sev > 5: level = "HIGH"
    elif avg_sev >= 3:       level = "MODERATE"
    else:                    level = "LOW"

    return {"level": level, "score": score, "maxScore": max_sev,
            "message": _URGENCY_MESSAGES[level]}


# ── Condition matching ───────────────────────────────────────────────────────

def match_conditions(symptoms: list[dict]) -> list[dict]:
    if not symptoms:
        return []

    detected_ids = {s["id"] for s in symptoms}
    scored: list[dict] = []

    for cond in CONDITIONS_DB:
        key_hits  = sum(1 for sid in cond["key_symptoms"]     if sid in detected_ids)
        supp_hits = sum(1 for sid in cond["support_symptoms"] if sid in detected_ids)

        if key_hits == 0:
            continue

        max_possible = len(cond["key_symptoms"]) * 2 + len(cond["support_symptoms"])
        actual_score = key_hits * 2 + supp_hits
        probability  = min(92, max(25, round(actual_score / max_possible * 100 + 15)))

        scored.append({
            "name":        cond["name"],
            "probability": probability,
            "description": cond["description"],
            "specialty":   cond["specialty"],
        })

    return sorted(scored, key=lambda x: x["probability"], reverse=True)[:3]


# ── Specialty ────────────────────────────────────────────────────────────────

def get_specialty(conditions: list[dict]) -> str:
    return conditions[0]["specialty"] if conditions else "General Physician"


# ── Tips ─────────────────────────────────────────────────────────────────────

_SYMPTOM_TIPS: dict[str, str] = {
    "fever":             "Stay hydrated - drink water, clear broths, or electrolyte drinks regularly.",
    "high_fever":        "Use a cool (not cold) damp cloth on your forehead and neck.",
    "persistent_fever":  "Monitor your temperature every 4 hours and record the results.",
    "headache":          "Rest in a quiet, dark room and apply a cold or warm compress.",
    "severe_headache":   "Avoid screens and bright lights; lie down in a dark room immediately.",
    "nausea":            "Sip ginger tea slowly. Avoid strong-smelling or fatty foods.",
    "vomiting":          "Take small sips of clear liquids every 15 minutes.",
    "cough":             "Honey in warm water soothes the throat. Use a humidifier if the air is dry.",
    "sore_throat":       "Gargle with warm salt water (1/4 tsp salt in 8 oz water) every few hours.",
    "runny_nose":        "Use saline nasal spray to clear passages and elevate your head when resting.",
    "nasal_congestion":  "Steam inhalation for 10 minutes can relieve sinus congestion significantly.",
    "fatigue":           "Prioritise 7-9 hours of sleep. Avoid caffeine after noon.",
    "dizziness":         "Sit or lie down immediately. Avoid sudden head movements.",
    "abdominal_pain":    "Apply a heating pad on low setting. Avoid spicy, fatty foods.",
    "diarrhea":          "Follow the BRAT diet (Bananas, Rice, Applesauce, Toast).",
    "back_pain":         "Apply ice for the first 48 h, then switch to heat. Gentle stretching helps.",
    "joint_pain":        "Rest the affected joint. Apply ice for 15 min and elevate if possible.",
    "itching":           "Apply a fragrance-free moisturiser or calamine lotion to irritated skin.",
    "skin_rash":         "Avoid scratching. Keep skin cool and wear loose cotton clothing.",
    "body_aches":        "A warm bath can ease aches. Rest and light stretching aid recovery.",
    "insomnia":          "Keep a consistent sleep schedule. Avoid screens 1 h before bed.",
    "anxiety":           "Try slow deep breathing: inhale 4 s, hold 4 s, exhale 6 s. Repeat 5 times.",
    "acid_reflux":       "Eat smaller meals and avoid lying down for 2 h after eating.",
    "chills":            "Layer warm clothing and blankets. Warm drinks can raise body temperature.",
    "sweating":          "Stay in a cool environment and wear breathable clothing.",
    "ear_pain":          "Apply a warm cloth over the ear. Avoid inserting anything into the canal.",
    "depression":        "Reach out to someone you trust. Short daily walks can lift mood noticeably.",
    "palpitations":      "Sit quietly, breathe slowly, and avoid caffeine. Log time and duration.",
    "breathlessness":    "Sit upright or lean slightly forward. Practise pursed-lip breathing.",
    "neck_pain":         "Apply heat or ice and do gentle neck rolls. Avoid hunching over screens.",
}

_URGENCY_TIPS: dict[str, list[str]] = {
    "LOW": [
        "Rest well and ensure you are getting 7-9 hours of sleep per night.",
        "Stay hydrated - aim for 8 glasses of water daily.",
        "Monitor your symptoms and note any changes over the next 24-48 hours.",
    ],
    "MODERATE": [
        "Rest as much as possible and avoid strenuous activities.",
        "Keep a symptom log noting severity, time, and any triggers.",
        "Ensure you are eating light, nutritious meals even if your appetite is low.",
    ],
    "HIGH": [
        "Do not drive yourself - arrange transport to the doctor or clinic.",
        "Bring a list of all current medications when you see your doctor.",
        "Have someone stay with you and monitor your condition.",
    ],
    "EMERGENCY": [
        "Call emergency services (911/112) immediately - do not wait.",
        "Do not eat or drink anything until assessed by medical personnel.",
        "Stay as calm and still as possible while waiting for help.",
    ],
}


def get_tips(urgency: str, symptoms: list[dict]) -> list[str]:
    if urgency == "EMERGENCY":
        return _URGENCY_TIPS["EMERGENCY"]
    tips: list[str] = []
    seen: set[str] = set()
    for s in symptoms:
        tip = _SYMPTOM_TIPS.get(s["id"])
        if tip and tip not in seen and len(tips) < 4:
            tips.append(tip)
            seen.add(tip)
    for t in _URGENCY_TIPS.get(urgency, _URGENCY_TIPS["LOW"]):
        if len(tips) >= 3:
            break
        if t not in seen:
            tips.append(t)
    return tips[:3]


# ── Session accumulation (in-memory, TTL 30 min) ─────────────────────────────

import time as _time

_sessions: dict[str, dict] = {}
_SESSION_TTL = 1800  # seconds


def _prune_sessions() -> None:
    cutoff = _time.time() - _SESSION_TTL
    stale  = [k for k, v in _sessions.items() if v["last_active"] < cutoff]
    for k in stale:
        del _sessions[k]


def get_or_create_session(session_id: str) -> dict:
    _prune_sessions()
    if session_id not in _sessions:
        _sessions[session_id] = {
            "symptoms":    [],
            "msg_count":   0,
            "last_active": _time.time(),
        }
    sess = _sessions[session_id]
    sess["last_active"] = _time.time()
    return sess


def _merge_symptoms(existing: list[dict], incoming: list[dict]) -> list[dict]:
    merged = list(existing)
    existing_ids = {s["id"] for s in merged}
    for s in incoming:
        if s["id"] not in existing_ids:
            merged.append(s)
            existing_ids.add(s["id"])
        else:
            idx = next(i for i, e in enumerate(merged) if e["id"] == s["id"])
            if s["severity"] > merged[idx]["severity"]:
                merged[idx] = s
    return merged


def clear_session(session_id: str) -> None:
    _sessions.pop(session_id, None)


# ── Conversational helpers ────────────────────────────────────────────────────

import random as _random

_GREETINGS = {"hello","hi","hey","good morning","good afternoon","good evening","howdy","hiya","sup"}
_THANKS    = {"thank","thanks","thank you","cheers","appreciate"}
_FAREWELLS = {"bye","goodbye","see you","farewell","take care","good night"}

_NO_SYMPTOM_MSGS = [
    "I wasn't able to detect specific symptoms in your message. Could you describe how you're feeling physically - for example, 'I have a headache and fever'?",
    "To give you the best analysis, please describe your symptoms in more detail.",
    "I'd love to help! Please describe any physical symptoms you are experiencing.",
]
_LOW_MSGS = [
    "Your symptoms appear mild at this stage. With some self-care you should start feeling better soon.",
    "Based on what you've described, your symptoms are relatively mild. Here's some guidance to help you recover.",
    "The symptoms you've mentioned are on the milder side, which is reassuring. Here's what I found.",
]
_MOD_MSGS = [
    "Your symptoms are moderate in severity and should be looked at by a healthcare professional soon.",
    "Your symptoms warrant a medical evaluation within the next couple of days.",
    "I'd recommend scheduling a doctor's appointment soon. Here's what the analysis shows.",
]
_HIGH_MSGS = [
    "I'm genuinely concerned. These symptoms indicate a need for prompt medical attention today.",
    "These symptoms are quite serious. Please see a doctor or visit an urgent care clinic today.",
    "This is a high-priority situation. Please seek medical care today.",
]
_EMERGENCY_MSGS = [
    "This is a medical emergency. Please call 911 or go to the nearest ER immediately.",
    "URGENT: These symptoms are life-threatening warning signs. Call for emergency help now.",
    "These symptoms require immediate emergency care. Do not wait - call 911 right away.",
]
_GREETING_MSGS = [
    "Hello! I'm MediAI. Describe your symptoms and I'll analyse them instantly.",
    "Hi there! Tell me how you're feeling and I'll help you understand your symptoms.",
    "Welcome to MediAI! Please describe any symptoms or health concerns you have.",
]


def _pick(arr: list[str]) -> str:
    return _random.choice(arr)


def _is_conversational(text: str) -> bool:
    t = text.lower().strip()
    if any(t.startswith(g) or t == g for g in _GREETINGS) and len(t) < 60:
        return True
    if any(th in t for th in _THANKS):
        return True
    if any(f in t for f in _FAREWELLS):
        return True
    return False


def _gen_message(urgency: str, symptom_count: int) -> str:
    if symptom_count == 0:  return _pick(_NO_SYMPTOM_MSGS)
    if urgency == "EMERGENCY": return _pick(_EMERGENCY_MSGS)
    if urgency == "HIGH":      return _pick(_HIGH_MSGS)
    if urgency == "MODERATE":  return _pick(_MOD_MSGS)
    return _pick(_LOW_MSGS)


# ── Main analyze function ─────────────────────────────────────────────────────

def analyze(message: str, session_id: str, nlp_tokens: Optional[dict] = None) -> dict:
    sess = get_or_create_session(session_id)
    sess["msg_count"] += 1

    if _is_conversational(message.strip()):
        acc = sess["symptoms"]
        triage     = calculate_triage(acc)
        conditions = match_conditions(acc)
        return {
            "message":         _pick(_GREETING_MSGS),
            "symptoms":        acc,
            "urgency":         triage["level"],
            "urgency_message": "",
            "conditions":      conditions,
            "specialty":       get_specialty(conditions),
            "tips":            [],
            "disclaimer":      "Always consult a qualified healthcare professional.",
            "source":          "nlp",
        }

    new_symptoms     = detect_symptoms(message, nlp_tokens)
    sess["symptoms"] = _merge_symptoms(sess["symptoms"], new_symptoms)

    # Analyse only current-turn symptoms; fall back to session if nothing new detected
    active = new_symptoms if new_symptoms else sess["symptoms"]
    triage     = calculate_triage(active)
    conditions = match_conditions(active)
    specialty  = get_specialty(conditions)
    tips       = get_tips(triage["level"], active)

    return {
        "message":         _gen_message(triage["level"], len(active)),
        "symptoms":        active,
        "urgency":         triage["level"],
        "urgency_message": triage["message"],
        "conditions":      conditions,
        "specialty":       specialty,
        "tips":            tips,
        "disclaimer":      "Always consult a qualified healthcare professional.",
        "source":          "nlp",
    }
