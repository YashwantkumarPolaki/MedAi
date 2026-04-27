from fastapi import APIRouter, HTTPException
from database import get_sessions, get_messages, delete_all_sessions
from models import HistorySession

router = APIRouter()


@router.get("/history", response_model=list[HistorySession])
async def list_history():
    """Return the last 20 sessions with metadata."""
    rows = await get_sessions(limit=20)
    return [
        HistorySession(
            id=r["id"],
            date=r["date"],
            urgency=r["urgency"] or "LOW",
            firstMsg=(r["first_msg"] or "")[:80],
            msgCount=r["msg_count"] or 0,
        )
        for r in rows
    ]


@router.get("/history/{session_id}")
async def get_session_history(session_id: str):
    """Return all messages for a specific session."""
    messages = await get_messages(session_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"sessionId": session_id, "messages": messages}


@router.delete("/history")
async def clear_history():
    """Delete all stored sessions and messages."""
    await delete_all_sessions()
    return {"success": True, "message": "All history cleared."}
