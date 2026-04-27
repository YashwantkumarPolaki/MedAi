"""MediAI FastAPI Backend — entry point."""
from __future__ import annotations
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from database import init_db
from routes import analyze, chat, doctors, history, triage, neuramorphix


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("\n  [OK]  MediAI FastAPI Backend ready")
    print(f"  [>>]  http://localhost:{os.getenv('PORT', 3000)}/api")
    print("  [?]   Docs: http://localhost:3000/docs\n")
    yield


app = FastAPI(
    title="MediAI API",
    version="2.0.0",
    description="AI-Driven Healthcare NLP + Gemini backend",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────────────────────
for router_module in (analyze, chat, doctors, history, triage, neuramorphix):
    app.include_router(router_module.router, prefix="/api")


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "MediAI NLP+Gemini Backend", "version": "2.0.0"}
