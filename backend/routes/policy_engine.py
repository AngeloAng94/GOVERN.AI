from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
import hashlib

from database import db
from models import (
    PolicyConflict, ConflictType, ConflictSeverity,
    ConflictResolution, AuditLog, AuditOutcome, RiskLevel,
)
from routes.auth import require_role

GUIDANCE = {
    "action_conflict": {
        "impact": (
            "Due policy applicano azioni opposte sullo stesso agente. "
            "Questo crea comportamenti imprevedibili e viola il principio di coerenza dei controlli."
        ),
        "guidance": (
            "Revisiona le due policy in conflitto e determina quale azione deve prevalere. "
            "Considera di unificarle in una singola policy con logica condizionale, oppure di "
            "limitare il perimetro di applicazione di una delle due. Documenta la decisione nell'audit trail."
        ),
    },
    "gap": {
        "impact": (
            "Un agente opera in un dominio non coperto da alcuna policy. "
            "Questo crea un'area di rischio non monitorata e potenzialmente non conforme "
            "agli standard normativi applicabili."
        ),
        "guidance": (
            "Crea una nuova policy che copra il dominio esposto oppure estendi il perimetro "
            "di una policy esistente. Valuta il livello di rischio dell'agente prima di procedere."
        ),
    },
    "overlap": {
        "impact": (
            "Due o piu policy si sovrappongono sullo stesso agente e dominio, causando "
            "ridondanza nei controlli e potenziale ambiguita nell'enforcement."
        ),
        "guidance": (
            "Verifica se le policy sovrapposte hanno lo stesso scopo. Se si, consolidale in "
            "una sola mantenendo la copertura normativa. Se hanno scopi diversi, ridefinisci i "
            "perimetri di applicazione."
        ),
    },
    "redundancy": {
        "impact": (
            "Esistono policy duplicate o quasi identiche. Questo aumenta il debito di governance "
            "e rende difficile la manutenzione dei controlli nel tempo."
        ),
        "guidance": (
            "Identifica la policy canonica da mantenere e depreca le altre. Assicurati che la "
            "policy mantenuta copra tutti i requisiti normativi delle policy rimosse."
        ),
    },
}

router = APIRouter(prefix="/policy-engine", tags=["policy-engine"])


def stable_conflict_id(conflict_type: str, policy_ids: list, agent_ids: list) -> str:
    """Generate a deterministic ID for a conflict based on its key properties."""
    key = f"{conflict_type}|{'|'.join(sorted(policy_ids))}|{'|'.join(sorted(agent_ids))}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]


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
                            id=stable_conflict_id("action_conflict", [p1["id"], p2["id"]], [aid]),
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
                            impact_description=GUIDANCE["action_conflict"]["impact"],
                            guidance=GUIDANCE["action_conflict"]["guidance"],
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
                    id=stable_conflict_id("gap", [], [agent["id"]]),
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
                    impact_description=GUIDANCE["gap"]["impact"],
                    guidance=GUIDANCE["gap"]["guidance"],
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
                        id=stable_conflict_id("overlap", [p["id"] for p in rp_list], [aid]),
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
                        impact_description=GUIDANCE["overlap"]["impact"],
                        guidance=GUIDANCE["overlap"]["guidance"],
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
                    id=stable_conflict_id("redundancy", [p1["id"], p2["id"]], [p1.get("agent_id", "")]),
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
                    impact_description=GUIDANCE["redundancy"]["impact"],
                    guidance=GUIDANCE["redundancy"]["guidance"],
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
    body: ConflictResolution,
    user: dict = Depends(require_role("dpo")),
):
    """Resolve a conflict with mandatory notes and audit trail."""
    now = datetime.now(timezone.utc).isoformat()

    # Save resolution
    await db.resolved_conflicts.update_one(
        {"id": conflict_id},
        {"$set": {
            "id": conflict_id,
            "resolved": True,
            "resolved_at": now,
            "resolved_by": body.resolved_by,
            "resolution_notes": body.resolution_notes,
        }},
        upsert=True,
    )

    # Look up conflict details for audit log context
    # Run a quick scan to find the conflict by id
    all_conflicts = await detect_conflicts()
    conflict_match = next((c for c in all_conflicts if c.id == conflict_id), None)
    policy_names_str = ", ".join(conflict_match.policy_names) if conflict_match else conflict_id
    severity_val = conflict_match.severity.value if conflict_match else "medium"
    risk_map = {"critical": RiskLevel.critical, "high": RiskLevel.high, "medium": RiskLevel.medium, "low": RiskLevel.low}

    # Audit log
    log = AuditLog(
        action="POLICY_CONFLICT_RESOLVED",
        resource=policy_names_str,
        outcome=AuditOutcome.allowed,
        details=body.resolution_notes,
        risk_level=risk_map.get(severity_val, RiskLevel.medium),
        user=body.resolved_by,
        agent_name="Policy Engine",
    )
    await db.audit_logs.insert_one(log.model_dump())

    return {"status": "resolved", "conflict_id": conflict_id, "resolved_at": now}


@router.get("/conflicts/{conflict_id}/guidance")
async def get_conflict_guidance(
    conflict_id: str,
    user: dict = Depends(require_role("viewer")),
):
    """Get guidance and impact description for a specific conflict."""
    all_conflicts = await detect_conflicts()
    conflict = next((c for c in all_conflicts if c.id == conflict_id), None)
    if not conflict:
        raise HTTPException(status_code=404, detail="Conflict not found")

    # Check if already resolved
    resolved_doc = await db.resolved_conflicts.find_one(
        {"id": conflict_id}, {"_id": 0}
    )

    result = {
        "id": conflict.id,
        "conflict_type": conflict.conflict_type.value,
        "severity": conflict.severity.value,
        "title": conflict.title,
        "description": conflict.description,
        "guidance": conflict.guidance,
        "impact_description": conflict.impact_description,
        "recommendation": conflict.recommendation,
        "policy_ids": conflict.policy_ids,
        "policy_names": conflict.policy_names,
        "agent_ids": conflict.agent_ids,
        "agent_names": conflict.agent_names,
        "regulation": conflict.regulation,
        "resolved": False,
        "resolved_by": None,
        "resolved_at": None,
        "resolution_notes": None,
    }

    if resolved_doc and resolved_doc.get("resolved"):
        result["resolved"] = True
        result["resolved_by"] = resolved_doc.get("resolved_by", "")
        result["resolved_at"] = resolved_doc.get("resolved_at", "")
        result["resolution_notes"] = resolved_doc.get("resolution_notes", "")

    return result


@router.get("/scan-history")
async def scan_history(user: dict = Depends(require_role("viewer"))):
    """Return last 10 conflict scans."""
    scans = (
        await db.conflict_scans.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .to_list(10)
    )
    return scans
