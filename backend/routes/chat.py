"""
/api/chat  — NLP analysis + optional Gemini enrichment.
Gemini key priority: X-Gemini-Key header > GEMINI_API_KEY env var.
"""
from __future__ import annotations
import os, json
from fastapi import APIRouter, Request, HTTPException
import httpx
from models import ChatRequest, ChatResponse
from nlp.engine import analyze, get_or_create_session
from database import (
    upsert_session, add_message, upsert_symptoms
)

router = APIRouter()

_GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-2.0-flash:generateContent?key={key}"
)

_SYSTEM_PROMPT = """You are MediAI, a compassionate medical triage assistant.
You will receive a user symptom description AND a JSON block of already-detected symptoms and triage level from our NLP engine.
Your task is ONLY to write a warm, empathetic 2-3 sentence response acknowledging the patient's situation.
Do NOT repeat the symptoms list or triage data verbatim — those are shown separately.
Do NOT give a diagnosis. Always end with one sentence advising professional consultation.
Respond in plain text only (no markdown, no JSON)."""


async def _call_gemini(api_key: str, user_msg: str, nlp_context: dict) -> str | None:
    context_block = (
        f"NLP context: urgency={nlp_context.get('urgency')}, "
        f"symptoms={[s['name'] for s in nlp_context.get('symptoms', [])]}"
    )
    prompt = f"{_SYSTEM_PROMPT}\n\n{context_block}\n\nPatient says: {user_msg}"
    try:
        async with httpx.AsyncClient(timeout=12.0) as client:
            resp = await client.post(
                _GEMINI_URL.format(key=api_key),
                json={
                    "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.4, "maxOutputTokens": 300},
                },
                headers={"Content-Type": "application/json"},
            )
        if resp.status_code == 200:
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        pass
    return None


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(body: ChatRequest, request: Request):
    # Resolve Gemini key
    gemini_key = (
        request.headers.get("X-Gemini-Key")
        or os.getenv("GEMINI_API_KEY", "")
    )

    # Run NLP analysis (accumulates session state in memory)
    tokens = body.nlpTokens.model_dump() if body.nlpTokens else None
    result = analyze(body.message, body.sessionId, tokens)

    # Optionally enrich message via Gemini
    source = "nlp"
    if gemini_key:
        gemini_text = await _call_gemini(gemini_key, body.message, result)
        if gemini_text:
            result["message"] = gemini_text
            source = "gemini"

    result["source"] = source

    # Persist to SQLite
    try:
        await upsert_session(body.sessionId, urgency=result["urgency"])
        await add_message(body.sessionId, "user", body.message)
        await add_message(body.sessionId, "ai",   result["message"])
        if result["symptoms"]:
            await upsert_symptoms(body.sessionId, result["symptoms"])
    except Exception:
        pass  # DB failures should not break the chat response

    return result
