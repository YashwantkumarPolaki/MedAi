from fastapi import APIRouter
from models import AnalyzeRequest, AnalysisResponse
from nlp.engine import detect_symptoms, calculate_triage, match_conditions, get_specialty

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_endpoint(body: AnalyzeRequest):
    """
    Pure NLP analysis — no session state, no Gemini.
    The frontend compromise.js preprocessed tokens are used to boost detection.
    """
    tokens = body.nlpTokens.model_dump() if body.nlpTokens else None
    symptoms   = detect_symptoms(body.message, tokens)
    triage     = calculate_triage(symptoms)
    conditions = match_conditions(symptoms)
    specialty  = get_specialty(conditions)

    return {
        "symptoms":   symptoms,
        "triage":     triage,
        "conditions": conditions,
        "specialty":  specialty,
    }
