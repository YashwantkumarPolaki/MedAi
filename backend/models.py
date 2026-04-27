from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class UrgencyLevel(str, Enum):
    LOW       = "LOW"
    MODERATE  = "MODERATE"
    HIGH      = "HIGH"
    EMERGENCY = "EMERGENCY"


# ── Inbound ──────────────────────────────────────────────────────────────────

class NLPTokens(BaseModel):
    """Preprocessed tokens from the frontend compromise.js NLP pass."""
    nouns:      List[str] = []
    adjectives: List[str] = []
    verbs:      List[str] = []
    phrases:    List[str] = []
    bodyParts:  List[str] = []
    rawTokens:  List[str] = []


class AnalyzeRequest(BaseModel):
    message:   str         = Field(..., min_length=1, max_length=2000)
    nlpTokens: Optional[NLPTokens] = None


class ChatRequest(BaseModel):
    message:   str         = Field(..., min_length=1, max_length=2000)
    sessionId: str         = Field(..., min_length=1)
    nlpTokens: Optional[NLPTokens] = None


class TriageRequest(BaseModel):
    symptoms: List[dict]


# ── Outbound ─────────────────────────────────────────────────────────────────

class DetectedSymptom(BaseModel):
    id:          str
    name:        str
    severity:    int
    description: str
    system:      str


class Condition(BaseModel):
    name:        str
    probability: int
    description: str
    specialty:   str


class TriageResult(BaseModel):
    level:    UrgencyLevel
    score:    float
    maxScore: int
    message:  str


class AnalysisResponse(BaseModel):
    symptoms:   List[DetectedSymptom]
    triage:     TriageResult
    conditions: List[Condition]
    specialty:  str


class ChatResponse(BaseModel):
    message:         str
    symptoms:        List[DetectedSymptom]
    urgency:         UrgencyLevel
    urgency_message: str
    conditions:      List[Condition]
    specialty:       str
    tips:            List[str]
    disclaimer:      str
    source:          str   # "gemini" | "nlp"


class DoctorModel(BaseModel):
    name:   str
    spec:   str
    rating: float
    avail:  str
    init:   str


class DoctorsResponse(BaseModel):
    specialty: str
    doctors:   List[DoctorModel]


class HistorySession(BaseModel):
    id:       str
    date:     str
    urgency:  str
    firstMsg: str
    msgCount: int


class NeuraMorphixRequest(BaseModel):
    symptoms:  List[dict]
    sessionId: str


class NeuraMorphixResponse(BaseModel):
    patterns:       List[dict]
    biomarkers:     List[dict]
    confidence:     float
    integrationTag: str
