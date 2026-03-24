from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from datetime import datetime, timezone
import io

from database import db
from routes.auth import require_role
from rate_limiter import limiter
from exporters import generate_compliance_pdf

router = APIRouter(prefix="/api/compliance", tags=["compliance"])


@router.get("")
async def list_compliance(user: dict = Depends(require_role("viewer"))):
    return await db.compliance_standards.find({}, {"_id": 0}).to_list(100)


@router.get("/export/pdf")
@limiter.limit("5/minute")
async def export_compliance_pdf(
    request: Request,
    user: dict = Depends(require_role("auditor"))
):
    """Export compliance status as PDF report"""
    standards = await db.compliance_standards.find({}, {"_id": 0}).to_list(100)
    pdf_bytes = generate_compliance_pdf(standards)
    
    filename = f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.put("/{standard_id}")
async def update_compliance(standard_id: str, data: dict, user: dict = Depends(require_role("dpo"))):
    existing = await db.compliance_standards.find_one({"id": standard_id}, {"_id": 0})
    if not existing: raise HTTPException(status_code=404, detail="Standard not found")
    allowed_fields = {"status", "progress", "requirements_met", "next_review"}
    update = {k: v for k, v in data.items() if k in allowed_fields}
    update["last_assessment"] = datetime.now(timezone.utc).isoformat()
    await db.compliance_standards.update_one({"id": standard_id}, {"$set": update})
    return await db.compliance_standards.find_one({"id": standard_id}, {"_id": 0})
