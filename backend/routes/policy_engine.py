from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone

from database import db
from models import (
    PolicyConflict, ConflictType, ConflictSeverity,
    AuditLog, AuditOutcome, RiskLevel,
)
from routes.auth import require_role

router = APIRouter(prefix="/policy-engine", tags=["policy-engine"])


async def detect_conflicts() -> list:
    """Run all conflict detection rules against live data."""
    policies = await db.policies.find({"status": "active"}, {"_id": 0}).to_list(1000)
    agents = await db.agents.find({"status": "active"}, {"_id": 0}).to_list(1000)
    conflicts = []

    agent_map = {a["id"]: a for a in agents}

    # Build agent -> policies index
    agent_policies_map = {}
    for p in policies:
        aid = p.get("agent_id")
        if aid:
            agent_policies_map.setdefault(aid, []).append(p)

    # ── RULE 1: Action Conflict ──
    # Two policies on same agent with overlapping conditions but opposing enforcement
    opposing = {
        ("block", "auto"), ("auto", "block"),
        ("block", "log"), ("log", "block"),
    }
    for aid, ap_list in agent_policies_map.items():
        agent = agent_map.get(aid, {})
        for i, p1 in enumerate(ap_list):
            for p2 in ap_list[i + 1:]:
                common = set(p1.get("conditions", [])) & set(p2.get("conditions", []))
                if common:
                    e1 = p1.get("enforcement", "")
                    e2 = p2.get("enforcement", "")
                    if (e1, e2) in opposing or (e2, e1) in opposing:
                        conflicts.append(PolicyConflict(
                            conflict_type=ConflictType.action_conflict,
                            severity=ConflictSeverity.critical,
                            title=f"Action conflict on agent '{agent.get('name', aid)}'",
                            description=(
                                f"Policies '{p1['name']}' and '{p2['name']}' prescribe opposing "
                                f"enforcement ({e1} vs {e2}) for shared conditions: "
                                f"{', '.join(common)}"
                            ),
                            policy_ids=[p1["id"], p2["id"]],
                            policy_names=[p1["name"], p2["name"]],
                            agent_ids=[aid],
                            agent_names=[agent.get("name", "")],
                            regulation=list({p1.get("regulation", ""), p2.get("regulation", "")} - {""}),
                            recommendation=(
                                f"Review and consolidate: decide which policy takes precedence "
                                f"for conditions: {', '.join(common)}"
                            ),
                        ))

    # ── RULE 2: Gap Detection ──
    # High/critical agents with no policy assigned
    for agent in agents:
        if agent.get("risk_level") in ("critical", "high"):
            if agent["id"] not in agent_policies_map:
                sev = (ConflictSeverity.critical
                       if agent["risk_level"] == "critical"
                       else ConflictSeverity.high)
                conflicts.append(PolicyConflict(
                    conflict_type=ConflictType.gap,
                    severity=sev,
                    title=f"No policy coverage for {agent['risk_level']}-risk agent '{agent['name']}'",
                    description=(
                        f"Agent '{agent['name']}' has risk level '{agent['risk_level']}' "
                        f"but no active policies are assigned. This creates an uncontrolled "
                        f"AI system operating without governance rules."
                    ),
                    agent_ids=[agent["id"]],
                    agent_names=[agent["name"]],
                    recommendation=(
                        f"Immediately assign at least one blocking policy to agent "
                        f"'{agent['name']}' covering its primary use case."
                    ),
                ))

    # ── RULE 3: Regulation Overlap ──
    # Same agent, same regulation, different rule_types
    for aid, ap_list in agent_policies_map.items():
        agent = agent_map.get(aid, {})
        by_reg = {}
        for p in ap_list:
            by_reg.setdefault(p.get("regulation", "none"), []).append(p)
        for reg, rp_list in by_reg.items():
            if len(rp_list) >= 2:
                rule_types = {p.get("rule_type", "") for p in rp_list}
                if len(rule_types) > 1:
                    conflicts.append(PolicyConflict(
                        conflict_type=ConflictType.overlap,
                        severity=ConflictSeverity.high,
                        title=f"Policy overlap for {reg} on agent '{agent.get('name', aid)}'",
                        description=(
                            f"{len(rp_list)} {reg} policies with different rule types "
                            f"({', '.join(rule_types)}) applied to the same agent. "
                            f"Execution order is undefined."
                        ),
                        policy_ids=[p["id"] for p in rp_list],
                        policy_names=[p["name"] for p in rp_list],
                        agent_ids=[aid],
                        agent_names=[agent.get("name", "")],
                        regulation=[reg],
                        recommendation=(
                            f"Define explicit priority order for {reg} policies "
                            f"or merge into a single comprehensive policy."
                        ),
                    ))

    # ── RULE 4: Redundancy ──
    # Same agent_id + identical conditions
    for i, p1 in enumerate(policies):
        for p2 in policies[i + 1:]:
            if (p1.get("agent_id") == p2.get("agent_id")
                    and p1.get("agent_id") is not None
                    and set(p1.get("conditions", [])) == set(p2.get("conditions", []))
                    and p1.get("conditions")):
                conflicts.append(PolicyConflict(
                    conflict_type=ConflictType.redundancy,
                    severity=ConflictSeverity.low,
                    title=f"Redundant policies: '{p1['name']}' and '{p2['name']}'",
                    description=(
                        f"Both policies have identical conditions: "
                        f"{', '.join(p1.get('conditions', []))}. "
                        f"One of them is unnecessary."
                    ),
                    policy_ids=[p1["id"], p2["id"]],
                    policy_names=[p1["name"], p2["name"]],
                    agent_ids=[p1.get("agent_id", "")],
                    recommendation="Remove or merge one of the redundant policies.",
                ))

    return conflicts


@router.get("/conflicts")
async def get_conflicts(user: dict = Depends(require_role("auditor"))):
    """Run real-time conflict detection scan on all active policies."""
    conflicts = await detect_conflicts()

    # Save scan to history
    scan_doc = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_conflicts": len(conflicts),
        "by_type": {},
        "by_severity": {},
    }
    for c in conflicts:
        ct = c.conflict_type.value
        cs = c.severity.value
        scan_doc["by_type"][ct] = scan_doc["by_type"].get(ct, 0) + 1
        scan_doc["by_severity"][cs] = scan_doc["by_severity"].get(cs, 0) + 1
    await db.conflict_scans.insert_one(scan_doc)

    # Build summary
    agents_impacted = set()
    policies_impacted = set()
    for c in conflicts:
        agents_impacted.update(c.agent_ids)
        policies_impacted.update(c.policy_ids)

    by_type = {}
    by_severity = {}
    for c in conflicts:
        by_type[c.conflict_type.value] = by_type.get(c.conflict_type.value, 0) + 1
        by_severity[c.severity.value] = by_severity.get(c.severity.value, 0) + 1

    return {
        "conflicts": [c.model_dump() for c in conflicts],
        "summary": {
            "total": len(conflicts),
            "by_type": by_type,
            "by_severity": by_severity,
            "agents_impacted": len(agents_impacted),
            "policies_impacted": len(policies_impacted),
            "scan_timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


@router.post("/conflicts/{conflict_id}/resolve")
async def resolve_conflict(
    conflict_id: str,
    body: dict,
    user: dict = Depends(require_role("dpo")),
):
    """Mark a conflict as resolved and log to audit trail."""
    resolved_by = body.get("resolved_by", user["username"])
    resolution_note = body.get("resolution_note", "")

    # Save resolution
    now = datetime.now(timezone.utc).isoformat()
    await db.resolved_conflicts.update_one(
        {"id": conflict_id},
        {"$set": {
            "id": conflict_id,
            "resolved": True,
            "resolved_at": now,
            "resolved_by": resolved_by,
            "resolution_note": resolution_note,
        }},
        upsert=True,
    )

    # Audit log
    log = AuditLog(
        action="conflict_resolved",
        resource=conflict_id,
        outcome=AuditOutcome.allowed,
        details=resolution_note or f"Conflict {conflict_id} resolved by {resolved_by}",
        risk_level=RiskLevel.medium,
        user=user["username"],
        agent_name="Policy Engine",
    )
    await db.audit_logs.insert_one(log.model_dump())

    return {"status": "resolved", "conflict_id": conflict_id, "resolved_at": now}


@router.get("/scan-history")
async def scan_history(user: dict = Depends(require_role("viewer"))):
    """Return last 10 conflict scans."""
    scans = (
        await db.conflict_scans.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .to_list(10)
    )
    return scans
