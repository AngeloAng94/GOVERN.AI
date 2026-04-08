"""
GOVERN.AI — Score API Endpoints
Exposes the Compliance Intelligence Engine via REST.
"""

from fastapi import APIRouter, Depends, Request, HTTPException
from datetime import datetime, timezone

from database import db
from routes.auth import require_role
from rate_limiter import limiter
from services.compliance_engine import compute_and_snapshot, compute_full_scores

router = APIRouter(prefix="/api/score", tags=["score"])


@router.get("/overview")
@limiter.limit("20/minute")
async def get_score_overview(request: Request, user: dict = Depends(require_role("viewer"))):
    """Full Compliance Intelligence Engine overview with explainability."""
    result = await compute_and_snapshot()
    return result["overview"]


@router.get("/agents")
@limiter.limit("20/minute")
async def get_agent_scores(request: Request, user: dict = Depends(require_role("viewer"))):
    """Score breakdown for all agents."""
    result = await compute_full_scores()
    return {"agents": result["agent_scores"], "count": len(result["agent_scores"])}


@router.get("/agents/{agent_id}")
@limiter.limit("20/minute")
async def get_agent_score(agent_id: str, request: Request, user: dict = Depends(require_role("viewer"))):
    """Score breakdown for a specific agent."""
    result = await compute_full_scores()
    agent = next((a for a in result["agent_scores"] if a["agent_id"] == agent_id), None)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.get("/standards")
@limiter.limit("20/minute")
async def get_standard_scores(request: Request, user: dict = Depends(require_role("viewer"))):
    """Score breakdown for all compliance standards."""
    result = await compute_full_scores()
    return {"standards": result["standard_scores"], "count": len(result["standard_scores"])}


@router.get("/history")
@limiter.limit("10/minute")
async def get_score_history(request: Request, user: dict = Depends(require_role("viewer"))):
    """Historical score snapshots for trend analysis."""
    snapshots = await db.score_history.find(
        {}, {"_id": 0}
    ).sort("timestamp", -1).to_list(30)
    return {"snapshots": snapshots, "count": len(snapshots)}


@router.get("/insights")
@limiter.limit("20/minute")
async def get_score_insights(request: Request, user: dict = Depends(require_role("viewer"))):
    """High-level insights combining scores, risks, and remediations."""
    result = await compute_and_snapshot()
    overview = result["overview"]

    # Build structured insights
    insights = []

    # Critical agents
    critical_agents = [a for a in result["agent_scores"] if a["score_band"] == "critical"]
    if critical_agents:
        insights.append({
            "type": "critical_alert",
            "severity": "critical",
            "title": f"{len(critical_agents)} agent(s) in critical state",
            "detail": ", ".join(a["agent_name"] for a in critical_agents),
            "action": "Review and remediate immediately",
        })

    # Weakest standard
    weakest = min(result["standard_scores"], key=lambda s: s["final_score"]) if result["standard_scores"] else None
    if weakest and weakest["final_score"] < 60:
        insights.append({
            "type": "weak_standard",
            "severity": "high",
            "title": f"{weakest['code']} compliance at {weakest['final_score']}%",
            "detail": f"{weakest['requirements_total'] - weakest['requirements_met']} requirements pending",
            "action": weakest["recommended_actions"][0] if weakest["recommended_actions"] else "Review standard requirements",
        })

    # Unresolved conflicts
    if overview["unresolved_conflicts"] > 0:
        insights.append({
            "type": "unresolved_conflicts",
            "severity": "high",
            "title": f"{overview['unresolved_conflicts']} unresolved policy conflicts",
            "detail": "Policy conflicts reduce governance score and create compliance risks",
            "action": "Open Policy Engine and resolve conflicts with documented rationale",
        })

    # Score trend
    delta = overview.get("delta_score", 0)
    if delta != 0:
        insights.append({
            "type": "score_trend",
            "severity": "info",
            "title": f"Score {'improved' if delta > 0 else 'declined'} by {abs(delta)} points",
            "detail": f"Previous: {overview.get('previous_score', 'N/A')} -> Current: {overview['final_score']}",
            "action": "Review recent changes in agents, policies, and conflicts",
        })

    # Positive: excellent agents
    excellent = [a for a in result["agent_scores"] if a["score_band"] == "excellent"]
    if excellent:
        insights.append({
            "type": "positive",
            "severity": "info",
            "title": f"{len(excellent)} agent(s) rated 'excellent'",
            "detail": ", ".join(a["agent_name"] for a in excellent[:3]),
            "action": "Use as benchmark for other agents",
        })

    return {
        "overall_score": overview["final_score"],
        "overall_band": overview["score_band"],
        "insights": insights,
        "top_remediations": overview["priority_remediations"][:5],
        "top_risks": overview["top_risks"][:5],
        "explanation": overview["explanation"],
        "last_calculated_at": overview["last_calculated_at"],
    }
