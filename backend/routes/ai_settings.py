"""
Admin-only AI provider toggle (Sovereign Mode / Performance Mode).

The state lives in-memory inside ``settings`` so the toggle has effect
immediately without restarting the backend. It does not persist across
process restarts on purpose — production deployments should set the
``LLM_SOVEREIGN_ENABLED`` env var as authoritative default.
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from routes.auth import require_role
from settings import settings

router = APIRouter(prefix="/api/settings", tags=["settings"])


class AIModeRequest(BaseModel):
    sovereign_mode: bool


def _state() -> dict:
    cfg = settings.get_llm_model()
    return {
        "sovereign_mode": settings.sovereign_enabled,
        "sovereign_configured": settings.sovereign_configured,
        "sovereign_model": settings.sovereign_model,
        "current_provider": cfg["provider"],
        "current_model": cfg["model"],
    }


@router.get("/ai-mode")
async def get_ai_mode(user: dict = Depends(require_role("viewer"))):
    """Return the current AI provider state."""
    return _state()


@router.post("/ai-mode")
async def set_ai_mode(
    req: AIModeRequest,
    user: dict = Depends(require_role("admin")),
):
    """Toggle Sovereign Mode at runtime (admin only)."""
    settings.set_sovereign_mode(req.sovereign_mode)
    return _state()
