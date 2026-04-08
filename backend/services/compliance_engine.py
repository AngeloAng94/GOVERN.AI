"""
GOVERN.AI — Compliance Intelligence Engine
Deterministic, explainable, modular scoring engine.
Produces scores, breakdowns, risks, remediations, and explanations
from real data (agents, policies, audit logs, compliance standards, conflicts).
"""

from datetime import datetime, timezone
from typing import Optional
from database import db
from routes.policy_engine import detect_conflicts


# ─── WEIGHTS & BANDS ─────────────────────────────────────────────────────────

RISK_BASE = {"critical": 25, "high": 45, "medium": 65, "low": 82}
SCORE_BANDS = [
    (90, "excellent", "Postura eccellente"),
    (70, "strong", "Postura solida"),
    (50, "warning", "Attenzione richiesta"),
    (0, "critical", "Rischio critico"),
]

CONFLICT_PENALTY = {"critical": 18, "high": 10, "medium": 5, "low": 2}


def _band(score: float) -> tuple:
    for threshold, band, label_it in SCORE_BANDS:
        if score >= threshold:
            return band, label_it
    return "critical", "Rischio critico"


# ─── AGENT SCORING ───────────────────────────────────────────────────────────

def score_agent(agent: dict, agent_policies: list, agent_audit: list, agent_conflicts: list) -> dict:
    """Compute a deterministic score for a single agent."""
    risk = agent.get("risk_level", "medium")
    base = RISK_BASE.get(risk, 65)

    # Policy coverage
    n_policies = len(agent_policies)
    policy_bonus = min(n_policies * 5, 15) if n_policies > 0 else -20

    # Audit outcome ratio
    total_audit = len(agent_audit)
    if total_audit > 0:
        allowed = sum(1 for a in agent_audit if a.get("outcome") == "allowed")
        ratio = allowed / total_audit
        audit_factor = round((ratio - 0.5) * 30)  # -15 to +15
    else:
        audit_factor = -5  # no audit data = slight penalty

    # Conflict penalty
    conflict_pen = 0
    for c in agent_conflicts:
        sev = c.get("severity", "medium") if isinstance(c, dict) else getattr(c, "severity", "medium")
        sev_val = sev.value if hasattr(sev, "value") else sev
        if not (c.get("resolved") if isinstance(c, dict) else getattr(c, "resolved", False)):
            conflict_pen += CONFLICT_PENALTY.get(sev_val, 5)

    # Status factor
    status = agent.get("status", "active")
    status_factor = 0 if status == "active" else (-10 if status == "suspended" else -20)

    raw = base + policy_bonus + audit_factor - conflict_pen + status_factor
    final = max(0, min(100, round(raw)))
    band, band_label = _band(final)

    # Build breakdown
    breakdown = {
        "base_risk_score": base,
        "policy_coverage": policy_bonus,
        "audit_outcome_factor": audit_factor,
        "conflict_penalty": -conflict_pen,
        "status_factor": status_factor,
    }

    positive = []
    negative = []
    if policy_bonus > 0:
        positive.append(f"{n_policies} governance policies assigned")
    if audit_factor > 0:
        positive.append(f"High compliance rate in audit trail ({round((audit_factor/30+0.5)*100)}%)")
    if risk in ("low", "medium"):
        positive.append(f"Risk level '{risk}' within acceptable range")
    if policy_bonus < 0:
        negative.append("No governance policies assigned — policy gap detected")
    if conflict_pen > 0:
        negative.append(f"{len([c for c in agent_conflicts if not (c.get('resolved') if isinstance(c, dict) else getattr(c, 'resolved', False))])} unresolved policy conflicts")
    if audit_factor < 0 and total_audit > 0:
        negative.append("High rate of blocked/escalated actions in audit trail")
    if status != "active":
        negative.append(f"Agent status is '{status}'")

    missing = []
    if n_policies == 0:
        missing.append(f"Assign at least one governance policy to agent '{agent.get('name', '')}'")
    if total_audit == 0:
        missing.append(f"No audit data available for agent '{agent.get('name', '')}' — enable logging")

    remediations = []
    if conflict_pen > 0:
        remediations.append(f"Resolve {len(agent_conflicts)} policy conflicts to improve score by up to +{conflict_pen} points")
    if policy_bonus < 0:
        remediations.append("Assign governance policies to gain +35 points (from -20 to +15)")
    if status != "active":
        remediations.append(f"Reactivate agent to recover +{abs(status_factor)} points")

    risks = []
    if conflict_pen > 0:
        risks.append({"type": "conflict", "detail": f"Unresolved conflicts impacting score by -{conflict_pen}"})
    if policy_bonus < 0:
        risks.append({"type": "gap", "detail": "No policy coverage — uncontrolled AI agent"})
    if risk in ("critical", "high") and n_policies < 2:
        risks.append({"type": "insufficient_controls", "detail": f"High-risk agent with only {n_policies} policies"})

    return {
        "agent_id": agent.get("id", ""),
        "agent_name": agent.get("name", ""),
        "risk_level": risk,
        "status": status,
        "final_score": final,
        "score_band": band,
        "score_band_label": band_label,
        "score_breakdown": breakdown,
        "positive_drivers": positive,
        "negative_drivers": negative,
        "missing_controls": missing,
        "top_risks": risks,
        "recommended_actions": remediations,
    }


# ─── STANDARD SCORING ────────────────────────────────────────────────────────

def score_standard(standard: dict, std_policies: list, std_agents: list, std_conflicts: list) -> dict:
    """Compute a deterministic score for a compliance standard."""
    progress = standard.get("progress", 0)
    req_total = standard.get("requirements_total", 1)
    req_met = standard.get("requirements_met", 0)

    base = progress  # 0-100

    # Requirements ratio bonus
    req_ratio = (req_met / max(req_total, 1)) * 100
    req_bonus = round((req_ratio - progress) * 0.2)  # small adjustment

    # Policy coverage for this regulation
    policy_bonus = min(len(std_policies) * 3, 12) if std_policies else -8

    # Conflict penalty for this regulation
    conflict_pen = 0
    for c in std_conflicts:
        sev = c.get("severity", "medium") if isinstance(c, dict) else getattr(c, "severity", "medium")
        sev_val = sev.value if hasattr(sev, "value") else sev
        if not (c.get("resolved") if isinstance(c, dict) else getattr(c, "resolved", False)):
            conflict_pen += CONFLICT_PENALTY.get(sev_val, 3)

    raw = base + req_bonus + policy_bonus - conflict_pen
    final = max(0, min(100, round(raw)))
    band, band_label = _band(final)

    positive = []
    negative = []
    if progress >= 70:
        positive.append(f"Strong progress at {progress}%")
    if len(std_policies) >= 3:
        positive.append(f"{len(std_policies)} policies mapped to this standard")
    if progress < 50:
        negative.append(f"Progress below 50% ({progress}%)")
    if len(std_policies) == 0:
        negative.append("No policies mapped to this standard")
    if conflict_pen > 0:
        negative.append(f"Policy conflicts impacting this standard (-{conflict_pen} pts)")

    remediations = []
    gap = req_total - req_met
    if gap > 0:
        remediations.append(f"Complete {gap} remaining requirements to reach full compliance")
    if conflict_pen > 0:
        remediations.append(f"Resolve policy conflicts to recover +{conflict_pen} points")
    if len(std_policies) == 0:
        remediations.append(f"Create policies mapped to {standard.get('code', '')} regulation")

    return {
        "standard_id": standard.get("id", ""),
        "standard_name": standard.get("name", ""),
        "code": standard.get("code", ""),
        "final_score": final,
        "score_band": band,
        "score_band_label": band_label,
        "progress": progress,
        "requirements_met": req_met,
        "requirements_total": req_total,
        "policies_count": len(std_policies),
        "score_breakdown": {
            "base_progress": base,
            "requirements_bonus": req_bonus,
            "policy_coverage": policy_bonus,
            "conflict_penalty": -conflict_pen,
        },
        "positive_drivers": positive,
        "negative_drivers": negative,
        "recommended_actions": remediations,
    }


# ─── OVERVIEW SCORING ────────────────────────────────────────────────────────

def calculate_overview(agent_scores: list, standard_scores: list, conflicts: list) -> dict:
    """Compute the overall governance score and insights."""
    if not agent_scores:
        agent_avg = 0
    else:
        agent_avg = sum(s["final_score"] for s in agent_scores) / len(agent_scores)

    if not standard_scores:
        std_avg = 0
    else:
        std_avg = sum(s["final_score"] for s in standard_scores) / len(standard_scores)

    # Weighted: standards 55%, agents 45%
    raw_overall = round(std_avg * 0.55 + agent_avg * 0.45)

    # Global conflict penalty
    unresolved_critical = sum(
        1 for c in conflicts
        if not (c.get("resolved") if isinstance(c, dict) else getattr(c, "resolved", False))
        and (c.get("severity", "") if isinstance(c, dict) else getattr(c, "severity", "")) in ("critical", ConflictSeverityVal("critical"))
    )
    global_penalty = min(unresolved_critical * 5, 15)
    final = max(0, min(100, raw_overall - global_penalty))
    band, band_label = _band(final)

    # Top risks (across all agents and standards)
    all_risks = []
    for a in agent_scores:
        for r in a.get("top_risks", []):
            all_risks.append({**r, "entity": a["agent_name"], "entity_type": "agent", "score": a["final_score"]})
    weakest_std = sorted(standard_scores, key=lambda s: s["final_score"])[:3]
    for s in weakest_std:
        if s["final_score"] < 60:
            all_risks.append({"type": "weak_standard", "detail": f"{s['code']} at {s['final_score']}%", "entity": s["standard_name"], "entity_type": "standard", "score": s["final_score"]})

    # Missing controls aggregate
    all_missing = []
    for a in agent_scores:
        all_missing.extend(a.get("missing_controls", []))

    # Priority remediations (sorted by impact)
    all_remediations = []
    for a in agent_scores:
        for r in a.get("recommended_actions", []):
            all_remediations.append({"action": r, "entity": a["agent_name"], "entity_type": "agent", "impact": _estimate_impact(r)})
    for s in standard_scores:
        for r in s.get("recommended_actions", []):
            all_remediations.append({"action": r, "entity": s["code"], "entity_type": "standard", "impact": _estimate_impact(r)})
    all_remediations.sort(key=lambda x: x["impact"], reverse=True)

    # Explainability
    explanation = _build_explanation(final, band, agent_scores, standard_scores, conflicts, all_risks)

    return {
        "final_score": final,
        "score_band": band,
        "score_band_label": band_label,
        "agent_avg_score": round(agent_avg, 1),
        "standard_avg_score": round(std_avg, 1),
        "total_agents": len(agent_scores),
        "total_standards": len(standard_scores),
        "unresolved_conflicts": sum(1 for c in conflicts if not (c.get("resolved") if isinstance(c, dict) else getattr(c, "resolved", False))),
        "total_conflicts": len(conflicts),
        "top_risks": all_risks[:8],
        "missing_controls": all_missing[:10],
        "priority_remediations": all_remediations[:10],
        "explanation": explanation,
        "last_calculated_at": datetime.now(timezone.utc).isoformat(),
    }


def _estimate_impact(action_text: str) -> int:
    """Estimate remediation impact from text (heuristic)."""
    if "critical" in action_text.lower() or "+35" in action_text or "+20" in action_text:
        return 90
    if "conflict" in action_text.lower() or "+1" in action_text:
        return 70
    if "policy" in action_text.lower() or "assign" in action_text.lower():
        return 60
    return 40


def _build_explanation(score, band, agent_scores, standard_scores, conflicts, risks) -> dict:
    """Build deterministic explainability payload."""
    n_agents = len(agent_scores)
    n_standards = len(standard_scores)
    n_excellent = sum(1 for a in agent_scores if a["score_band"] == "excellent")
    n_warning = sum(1 for a in agent_scores if a["score_band"] == "warning")
    n_critical = sum(1 for a in agent_scores if a["score_band"] == "critical")
    weakest_agent = min(agent_scores, key=lambda a: a["final_score"]) if agent_scores else None
    strongest_agent = max(agent_scores, key=lambda a: a["final_score"]) if agent_scores else None
    weakest_std = min(standard_scores, key=lambda s: s["final_score"]) if standard_scores else None

    strongest_positive = "No significant positive factors"
    if n_excellent > 0:
        strongest_positive = f"{n_excellent}/{n_agents} agents rated 'excellent'"
    elif strongest_agent and strongest_agent["final_score"] >= 70:
        strongest_positive = f"Strongest agent '{strongest_agent['agent_name']}' at {strongest_agent['final_score']}%"

    strongest_negative = "No critical issues detected"
    if n_critical > 0:
        strongest_negative = f"{n_critical} agent(s) in 'critical' status"
    elif weakest_agent and weakest_agent["final_score"] < 50:
        strongest_negative = f"Agent '{weakest_agent['agent_name']}' at {weakest_agent['final_score']}% — needs immediate attention"

    unresolved = sum(1 for c in conflicts if not (c.get("resolved") if isinstance(c, dict) else getattr(c, "resolved", False)))

    summary = f"Overall governance score is {score}/100 ({band}). "
    if band == "excellent":
        summary += f"All {n_agents} agents and {n_standards} standards show strong compliance posture."
    elif band == "strong":
        summary += f"{n_excellent} agents excel, but {n_warning + n_critical} need attention. "
        if weakest_std:
            summary += f"Weakest standard: {weakest_std['code']} at {weakest_std['final_score']}%."
    elif band == "warning":
        summary += f"Multiple areas require improvement. {n_warning + n_critical} agents below threshold. "
        if unresolved > 0:
            summary += f"{unresolved} unresolved policy conflicts."
    else:
        summary += f"Critical governance gaps detected. {n_critical} agents in critical state. Immediate action required."

    why = f"Score is computed as weighted average of agent scores (45%, avg {round(sum(a['final_score'] for a in agent_scores)/max(len(agent_scores),1),1)}%) and standard scores (55%, avg {round(sum(s['final_score'] for s in standard_scores)/max(len(standard_scores),1),1)}%)"
    if unresolved > 0:
        why += f", with a -{min(unresolved * 5, 15)} penalty for {unresolved} unresolved critical conflicts"

    return {
        "explanation_summary": summary,
        "why_this_score": why,
        "strongest_positive_factor": strongest_positive,
        "strongest_negative_factor": strongest_negative,
        "methodology_note": "Scores are deterministic, computed from real governance data. No LLM involved in calculations. Methodology: risk-weighted base + policy coverage + audit outcomes - conflict penalties.",
        "score_factors": {
            "agents_excellent": n_excellent,
            "agents_warning": n_warning,
            "agents_critical": n_critical,
            "unresolved_conflicts": unresolved,
            "weakest_standard": weakest_std["code"] if weakest_std else None,
            "weakest_standard_score": weakest_std["final_score"] if weakest_std else None,
        }
    }


class ConflictSeverityVal:
    """Helper for severity comparison."""
    def __init__(self, v):
        self.v = v
    def __eq__(self, other):
        if hasattr(other, "value"):
            return other.value == self.v
        return other == self.v


# ─── MAIN ORCHESTRATOR ───────────────────────────────────────────────────────

async def compute_full_scores() -> dict:
    """Run the full Compliance Intelligence Engine and return all scores."""
    # Fetch data
    agents = await db.agents.find({}, {"_id": 0}).to_list(500)
    policies = await db.policies.find({}, {"_id": 0}).to_list(500)
    audit_logs = await db.audit_logs.find({}, {"_id": 0}).sort("timestamp", -1).to_list(2000)
    standards = await db.compliance_standards.find({}, {"_id": 0}).to_list(50)
    conflicts_raw = await detect_conflicts()
    # Convert to dicts
    conflicts = [c.model_dump() if hasattr(c, "model_dump") else c for c in conflicts_raw]

    # Check resolved status
    resolved_docs = await db.resolved_conflicts.find({}, {"_id": 0}).to_list(500)
    resolved_ids = {d["id"] for d in resolved_docs if d.get("resolved")}
    for c in conflicts:
        if c["id"] in resolved_ids:
            c["resolved"] = True

    # Index data by agent_id
    policies_by_agent = {}
    for p in policies:
        aid = p.get("agent_id", "")
        if aid:
            policies_by_agent.setdefault(aid, []).append(p)

    audit_by_agent = {}
    for log in audit_logs:
        aname = log.get("agent_name", "")
        audit_by_agent.setdefault(aname, []).append(log)

    conflicts_by_agent = {}
    for c in conflicts:
        for aid in c.get("agent_ids", []):
            conflicts_by_agent.setdefault(aid, []).append(c)

    # Score agents
    agent_scores = []
    for agent in agents:
        aid = agent.get("id", "")
        aname = agent.get("name", "")
        a_policies = policies_by_agent.get(aid, [])
        a_audit = audit_by_agent.get(aname, [])
        a_conflicts = conflicts_by_agent.get(aid, [])
        s = score_agent(agent, a_policies, a_audit, a_conflicts)
        agent_scores.append(s)

    # Index data by regulation
    policies_by_reg = {}
    for p in policies:
        reg = p.get("regulation", "")
        if reg:
            policies_by_reg.setdefault(reg, []).append(p)

    agents_by_reg = {}
    for p in policies:
        reg = p.get("regulation", "")
        aid = p.get("agent_id", "")
        if reg and aid:
            agents_by_reg.setdefault(reg, set()).add(aid)

    conflicts_by_reg = {}
    for c in conflicts:
        for reg in c.get("regulation", []):
            conflicts_by_reg.setdefault(reg, []).append(c)

    # Score standards
    standard_scores = []
    for std in standards:
        code = std.get("code", "")
        s_policies = policies_by_reg.get(code, [])
        s_agents_ids = agents_by_reg.get(code, set())
        s_agents = [a for a in agents if a.get("id") in s_agents_ids]
        s_conflicts = conflicts_by_reg.get(code, [])
        s = score_standard(std, s_policies, s_agents, s_conflicts)
        standard_scores.append(s)

    # Overview
    overview = calculate_overview(agent_scores, standard_scores, conflicts)

    return {
        "overview": overview,
        "agent_scores": sorted(agent_scores, key=lambda x: x["final_score"]),
        "standard_scores": sorted(standard_scores, key=lambda x: x["final_score"]),
    }


async def compute_and_snapshot() -> dict:
    """Compute scores and save a snapshot for history tracking."""
    result = await compute_full_scores()
    now = datetime.now(timezone.utc).isoformat()

    snapshot = {
        "timestamp": now,
        "overall_score": result["overview"]["final_score"],
        "overall_band": result["overview"]["score_band"],
        "agent_avg": result["overview"]["agent_avg_score"],
        "standard_avg": result["overview"]["standard_avg_score"],
        "unresolved_conflicts": result["overview"]["unresolved_conflicts"],
        "agent_snapshots": [
            {"agent_id": a["agent_id"], "agent_name": a["agent_name"], "score": a["final_score"], "band": a["score_band"]}
            for a in result["agent_scores"]
        ],
        "standard_snapshots": [
            {"code": s["code"], "score": s["final_score"], "band": s["score_band"]}
            for s in result["standard_scores"]
        ],
    }

    # Save snapshot
    await db.score_history.insert_one({**snapshot, "_id_exclude": True})

    # Compute deltas from previous snapshot
    prev = await db.score_history.find({}, {"_id": 0}).sort("timestamp", -1).to_list(2)
    if len(prev) >= 2:
        previous = prev[1]  # second most recent
        result["overview"]["previous_score"] = previous.get("overall_score")
        result["overview"]["delta_score"] = result["overview"]["final_score"] - previous.get("overall_score", result["overview"]["final_score"])
        result["overview"]["trend_direction"] = "up" if result["overview"]["delta_score"] > 0 else ("down" if result["overview"]["delta_score"] < 0 else "stable")

        # Agent deltas
        prev_agent_map = {a["agent_id"]: a["score"] for a in previous.get("agent_snapshots", [])}
        for a in result["agent_scores"]:
            prev_score = prev_agent_map.get(a["agent_id"])
            if prev_score is not None:
                a["previous_score"] = prev_score
                a["delta_score"] = a["final_score"] - prev_score
                a["trend_direction"] = "up" if a["delta_score"] > 0 else ("down" if a["delta_score"] < 0 else "stable")

        # Standard deltas
        prev_std_map = {s["code"]: s["score"] for s in previous.get("standard_snapshots", [])}
        for s in result["standard_scores"]:
            prev_s = prev_std_map.get(s["code"])
            if prev_s is not None:
                s["previous_score"] = prev_s
                s["delta_score"] = s["final_score"] - prev_s
                s["trend_direction"] = "up" if s["delta_score"] > 0 else ("down" if s["delta_score"] < 0 else "stable")
    else:
        result["overview"]["previous_score"] = None
        result["overview"]["delta_score"] = 0
        result["overview"]["trend_direction"] = "stable"

    return result
