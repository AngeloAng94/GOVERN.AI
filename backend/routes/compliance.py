from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone

from database import db
from routes.auth import require_role

router = APIRouter(prefix="/api/compliance", tags=["compliance"])


@router.get("")
async def list_compliance(user: dict = Depends(require_role("viewer"))):
    return await db.compliance_standards.find({}, {"_id": 0}).to_list(100)


@router.put("/{standard_id}")
async def update_compliance(standard_id: str, data: dict, user: dict = Depends(require_role("dpo"))):
    existing = await db.compliance_standards.find_one({"id": standard_id}, {"_id": 0})
    if not existing: raise HTTPException(status_code=404, detail="Standard not found")
    allowed_fields = {"status", "progress", "requirements_met", "next_review"}
    update = {k: v for k, v in data.items() if k in allowed_fields}
    update["last_assessment"] = datetime.now(timezone.utc).isoformat()
    await db.compliance_standards.update_one({"id": standard_id}, {"$set": update})
    return await db.compliance_standards.find_one({"id": standard_id}, {"_id": 0})
