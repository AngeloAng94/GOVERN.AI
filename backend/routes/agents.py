from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional
from datetime import datetime, timezone

from database import db
from models import Agent, AgentCreate, AuditLog, AuditOutcome
from routes.auth import require_role
from rate_limiter import limiter

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.get("", response_model=List[Agent])
async def list_agents(status: Optional[str] = None, risk_level: Optional[str] = None, user: dict = Depends(require_role("viewer"))):
    query = {}
    if status: query["status"] = status
    if risk_level: query["risk_level"] = risk_level
    return await db.agents.find(query, {"_id": 0}).to_list(100)


@router.get("/{agent_id}")
async def get_agent(agent_id: str, user: dict = Depends(require_role("viewer"))):
    agent = await db.agents.find_one({"id": agent_id}, {"_id": 0})
    if not agent: raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.post("", response_model=Agent, status_code=201)
@limiter.limit("30/minute")
async def create_agent(request: Request, data: AgentCreate, user: dict = Depends(require_role("dpo"))):
    agent = Agent(**data.model_dump())
    await db.agents.insert_one(agent.model_dump())
    log = AuditLog(agent_name=agent.name, action="agent_created", resource=f"/agents/{agent.id}", outcome=AuditOutcome.allowed, details=f"Agent '{agent.name}' created", user=user["username"])
    await db.audit_logs.insert_one(log.model_dump())
    return await db.agents.find_one({"id": agent.id}, {"_id": 0})


@router.put("/{agent_id}", response_model=Agent)
async def update_agent(agent_id: str, data: AgentCreate, user: dict = Depends(require_role("dpo"))):
    existing = await db.agents.find_one({"id": agent_id}, {"_id": 0})
    if not existing: raise HTTPException(status_code=404, detail="Agent not found")
    update_data = data.model_dump()
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    await db.agents.update_one({"id": agent_id}, {"$set": update_data})
    log = AuditLog(agent_name=data.name, action="agent_updated", resource=f"/agents/{agent_id}", outcome=AuditOutcome.allowed, details=f"Agent '{data.name}' updated", user=user["username"])
    await db.audit_logs.insert_one(log.model_dump())
    return await db.agents.find_one({"id": agent_id}, {"_id": 0})


@router.delete("/{agent_id}")
@limiter.limit("10/minute")
async def delete_agent(request: Request, agent_id: str, user: dict = Depends(require_role("admin"))):
    existing = await db.agents.find_one({"id": agent_id}, {"_id": 0})
    if not existing: raise HTTPException(status_code=404, detail="Agent not found")
    await db.agents.delete_one({"id": agent_id})
    log = AuditLog(agent_name=existing.get("name", ""), action="agent_deleted", resource=f"/agents/{agent_id}", outcome=AuditOutcome.allowed, details=f"Agent '{existing.get('name', '')}' deleted", user=user["username"])
    await db.audit_logs.insert_one(log.model_dump())
    return {"status": "deleted", "id": agent_id}
