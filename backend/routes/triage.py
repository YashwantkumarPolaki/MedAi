from fastapi import APIRouter
from models import TriageRequest, TriageResult
from nlp.engine import calculate_triage

router = APIRouter()


@router.post("/triage", response_model=TriageResult)
async def triage_endpoint(body: TriageRequest):
    """Standalone triage scoring from a pre-supplied symptom list."""
    result = calculate_triage(body.symptoms)
    return result
