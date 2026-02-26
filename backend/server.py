from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from enum import Enum
import os
import re
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# LLM setup
from emergentintegrations.llm.chat import LlmChat, UserMessage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============ ENUMS (Fix 1.5) ============

class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class AgentStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"

class PolicySeverity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class PolicyEnforcement(str, Enum):
    block = "block"
    log = "log"
    throttle = "throttle"
    auto = "auto"

class RuleType(str, Enum):
    restriction = "restriction"
    approval = "approval"
    rate_limit = "rate_limit"
    logging = "logging"
    retention = "retention"

class AuditOutcome(str, Enum):
    allowed = "allowed"
    blocked = "blocked"
    logged = "logged"
    escalated = "escalated"

class DataClassification(str, Enum):
    public = "public"
    internal = "internal"
    confidential = "confidential"
    restricted = "restricted"

# ============ MODELS ============

class AgentCreate(BaseModel):
    name: str
    description: str
    model_type: str = "GPT-5.2"
    risk_level: RiskLevel = RiskLevel.medium
    status: AgentStatus = AgentStatus.active
    allowed_actions: List[str] = []
    restricted_domains: List[str] = []
    data_classification: DataClassification = DataClassification.internal
    owner: str = ""

class Agent(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    model_type: str = "GPT-5.2"
    risk_level: RiskLevel = RiskLevel.medium
    status: AgentStatus = AgentStatus.active
    allowed_actions: List[str] = []
    restricted_domains: List[str] = []
    data_classification: DataClassification = DataClassification.internal
    owner: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    policy_count: int = 0
    last_audit: Optional[str] = None

class PolicyCreate(BaseModel):
    name: str
    description: str
    agent_id: Optional[str] = None
    rule_type: RuleType = RuleType.restriction
    conditions: List[str] = []
    actions: List[str] = []
    severity: PolicySeverity = PolicySeverity.medium
    regulation: str = "GDPR"
    enforcement: PolicyEnforcement = PolicyEnforcement.block

class Policy(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    agent_id: Optional[str] = None
    rule_type: RuleType = RuleType.restriction
    conditions: List[str] = []
    actions: List[str] = []
    severity: PolicySeverity = PolicySeverity.medium
    regulation: str = "GDPR"
    enforcement: PolicyEnforcement = PolicyEnforcement.block
    status: str = "active"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    violations_count: int = 0

class AuditLog(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    agent_id: Optional[str] = None
    agent_name: str = ""
    action: str = ""
    resource: str = ""
    outcome: AuditOutcome = AuditOutcome.allowed
    policy_id: Optional[str] = None
    policy_name: str = ""
    details: str = ""
    risk_level: RiskLevel = RiskLevel.low
    ip_address: str = ""
    user: str = "system"

class ComplianceStandard(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    code: str
    description: str
    status: str = "in_progress"
    progress: int = 0
    requirements_total: int = 0
    requirements_met: int = 0
    last_assessment: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    next_review: str = ""
    category: str = "regulation"

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

# ============ INDEX CREATION (Fix 1.1) ============

async def create_indexes():
    # agents
    await db.agents.create_index("id", unique=True, background=True)
    logger.info("Created index: agents.id (unique)")
    await db.agents.create_index("status", background=True)
    logger.info("Created index: agents.status")
    await db.agents.create_index("risk_level", background=True)
    logger.info("Created index: agents.risk_level")

    # policies
    await db.policies.create_index("id", unique=True, background=True)
    logger.info("Created index: policies.id (unique)")
    await db.policies.create_index("regulation", background=True)
    logger.info("Created index: policies.regulation")
    await db.policies.create_index("agent_id", background=True)
    logger.info("Created index: policies.agent_id")

    # audit_logs
    await db.audit_logs.create_index("id", unique=True, background=True)
    logger.info("Created index: audit_logs.id (unique)")
    await db.audit_logs.create_index([("timestamp", -1)], background=True)
    logger.info("Created index: audit_logs.timestamp (desc)")
    await db.audit_logs.create_index("outcome", background=True)
    logger.info("Created index: audit_logs.outcome")
    await db.audit_logs.create_index("risk_level", background=True)
    logger.info("Created index: audit_logs.risk_level")
    await db.audit_logs.create_index("agent_name", background=True)
    logger.info("Created index: audit_logs.agent_name")

    # compliance_standards
    await db.compliance_standards.create_index("id", unique=True, background=True)
    logger.info("Created index: compliance_standards.id (unique)")
    await db.compliance_standards.create_index("code", unique=True, background=True)
    logger.info("Created index: compliance_standards.code (unique)")

    # chat_messages (compound)
    await db.chat_messages.create_index([("session_id", 1), ("timestamp", 1)], background=True)
    logger.info("Created index: chat_messages.session_id+timestamp (compound)")

# ============ SEED DATA ============

async def seed_compliance_standards():
    count = await db.compliance_standards.count_documents({})
    if count == 0:
        standards = [
            ComplianceStandard(
                name="EU AI Act", code="EU-AI-ACT",
                description="European Union Artificial Intelligence Act - Regulation on harmonised rules for AI systems",
                status="in_progress", progress=68, requirements_total=42, requirements_met=28,
                category="regulation", next_review="2026-06-01T00:00:00Z"
            ),
            ComplianceStandard(
                name="GDPR", code="GDPR",
                description="General Data Protection Regulation - Data protection and privacy regulation",
                status="compliant", progress=92, requirements_total=35, requirements_met=32,
                category="regulation", next_review="2026-04-15T00:00:00Z"
            ),
            ComplianceStandard(
                name="ISO 27001", code="ISO-27001",
                description="Information Security Management Systems - International standard for managing information security",
                status="in_progress", progress=75, requirements_total=28, requirements_met=21,
                category="standard", next_review="2026-05-20T00:00:00Z"
            ),
            ComplianceStandard(
                name="ISO 42001", code="ISO-42001",
                description="AI Management System - International standard for responsible AI governance",
                status="in_progress", progress=45, requirements_total=30, requirements_met=13,
                category="standard", next_review="2026-07-01T00:00:00Z"
            ),
            ComplianceStandard(
                name="DORA", code="DORA",
                description="Digital Operational Resilience Act - Financial sector digital resilience",
                status="non_compliant", progress=32, requirements_total=25, requirements_met=8,
                category="regulation", next_review="2026-03-30T00:00:00Z"
            ),
            ComplianceStandard(
                name="NIS2", code="NIS2",
                description="Network and Information Security Directive 2 - Cybersecurity obligations",
                status="in_progress", progress=58, requirements_total=20, requirements_met=11,
                category="directive", next_review="2026-05-01T00:00:00Z"
            ),
        ]
        for s in standards:
            await db.compliance_standards.insert_one(s.model_dump())
        logger.info("Seeded compliance standards")

async def seed_sample_data():
    agent_count = await db.agents.count_documents({})
    if agent_count == 0:
        agents = [
            AgentCreate(name="Customer Service Bot", description="Handles customer inquiries via chat", model_type="GPT-5.2", risk_level=RiskLevel.medium, status=AgentStatus.active, allowed_actions=["read_faq", "create_ticket", "escalate"], restricted_domains=["financial_data", "medical_records"], data_classification=DataClassification.public, owner="Operations Team"),
            AgentCreate(name="Document Analyzer", description="Analyzes legal and compliance documents", model_type="Claude-Sonnet", risk_level=RiskLevel.high, status=AgentStatus.active, allowed_actions=["read_document", "extract_data", "generate_summary"], restricted_domains=["external_sharing"], data_classification=DataClassification.confidential, owner="Legal Dept"),
            AgentCreate(name="Risk Assessment Engine", description="Evaluates financial risk profiles", model_type="GPT-5.2", risk_level=RiskLevel.critical, status=AgentStatus.suspended, allowed_actions=["read_portfolio", "calculate_risk", "generate_report"], restricted_domains=["trading", "external_api"], data_classification=DataClassification.restricted, owner="Risk Management"),
            AgentCreate(name="HR Onboarding Assistant", description="Guides new employees through onboarding", model_type="Gemini-3", risk_level=RiskLevel.low, status=AgentStatus.active, allowed_actions=["send_email", "create_account", "schedule_meeting"], restricted_domains=["salary_data", "performance_reviews"], data_classification=DataClassification.internal, owner="HR Department"),
        ]
        for a in agents:
            agent_obj = Agent(**a.model_dump())
            await db.agents.insert_one(agent_obj.model_dump())
        
        # Seed some policies
        policies = [
            PolicyCreate(name="PII Data Access Control", description="Restricts access to personally identifiable information", rule_type=RuleType.restriction, conditions=["data_contains_pii", "agent_risk_level_high"], actions=["block_access", "log_attempt", "notify_dpo"], severity=PolicySeverity.critical, regulation="GDPR", enforcement=PolicyEnforcement.block),
            PolicyCreate(name="Model Output Logging", description="All AI model outputs must be logged for audit purposes", rule_type=RuleType.logging, conditions=["any_model_output"], actions=["log_output", "store_trace"], severity=PolicySeverity.medium, regulation="EU-AI-ACT", enforcement=PolicyEnforcement.log),
            PolicyCreate(name="External API Rate Limit", description="Limits external API calls to prevent data exfiltration", rule_type=RuleType.rate_limit, conditions=["external_api_call"], actions=["rate_limit_100_per_hour", "alert_on_exceed"], severity=PolicySeverity.high, regulation="ISO-27001", enforcement=PolicyEnforcement.throttle),
            PolicyCreate(name="Human-in-the-Loop for Critical Decisions", description="Requires human approval for high-impact decisions", rule_type=RuleType.approval, conditions=["decision_impact_high", "financial_threshold_exceeded"], actions=["pause_execution", "request_approval", "notify_supervisor"], severity=PolicySeverity.critical, regulation="EU-AI-ACT", enforcement=PolicyEnforcement.block),
            PolicyCreate(name="Data Retention Policy", description="Automatic deletion of processed data after 90 days", rule_type=RuleType.retention, conditions=["data_age_90_days"], actions=["schedule_deletion", "anonymize_logs"], severity=PolicySeverity.medium, regulation="GDPR", enforcement=PolicyEnforcement.auto),
        ]
        for p in policies:
            policy_obj = Policy(**p.model_dump())
            await db.policies.insert_one(policy_obj.model_dump())

        # Seed audit logs
        import random
        actions_list = ["data_access", "model_inference", "api_call", "policy_check", "document_scan", "user_query", "report_generation", "data_export"]
        outcomes = [AuditOutcome.allowed, AuditOutcome.blocked, AuditOutcome.logged, AuditOutcome.escalated]
        resources = ["/data/customers", "/models/gpt5", "/api/external/crm", "/documents/legal", "/reports/quarterly", "/data/transactions"]
        agent_names = ["Customer Service Bot", "Document Analyzer", "Risk Assessment Engine", "HR Onboarding Assistant"]
        users = ["m.rossi@company.it", "g.bianchi@company.it", "l.ferrari@company.it", "system", "a.romano@company.it"]
        risk_levels = [RiskLevel.low, RiskLevel.medium, RiskLevel.high, RiskLevel.critical]

        for i in range(25):
            log = AuditLog(
                agent_name=random.choice(agent_names),
                action=random.choice(actions_list),
                resource=random.choice(resources),
                outcome=random.choice(outcomes),
                details=f"Automated audit event #{i+1}",
                risk_level=random.choice(risk_levels),
                ip_address=f"10.0.{random.randint(1,5)}.{random.randint(1,254)}",
                user=random.choice(users)
            )
            await db.audit_logs.insert_one(log.model_dump())
        logger.info("Seeded sample agents, policies, and audit logs")

# ============ LIFESPAN (Fix 1.8) ============

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await create_indexes()
    await seed_compliance_standards()
    await seed_sample_data()
    logger.info("GOVERN.AI startup complete")
    yield
    # Shutdown
    client.close()
    logger.info("GOVERN.AI shutdown complete")

app = FastAPI(lifespan=lifespan)
api_router = APIRouter(prefix="/api")

# ============ DASHBOARD ============

@api_router.get("/dashboard/stats")
async def get_dashboard_stats():
    agents_total = await db.agents.count_documents({})
    agents_active = await db.agents.count_documents({"status": "active"})
    policies_total = await db.policies.count_documents({})
    policies_active = await db.policies.count_documents({"status": "active"})
    audit_total = await db.audit_logs.count_documents({})
    audit_blocked = await db.audit_logs.count_documents({"outcome": "blocked"})
    audit_escalated = await db.audit_logs.count_documents({"outcome": "escalated"})
    compliance_list = await db.compliance_standards.find({}, {"_id": 0, "progress": 1}).to_list(100)
    avg_compliance = sum(c["progress"] for c in compliance_list) / len(compliance_list) if compliance_list else 0

    recent_audit = await db.audit_logs.find({}, {"_id": 0}).sort("timestamp", -1).to_list(5)
    
    # Risk distribution
    risk_dist = {}
    agents_cursor = db.agents.find({}, {"_id": 0, "risk_level": 1})
    async for a in agents_cursor:
        rl = a.get("risk_level", "unknown")
        risk_dist[rl] = risk_dist.get(rl, 0) + 1

    return {
        "agents": {"total": agents_total, "active": agents_active},
        "policies": {"total": policies_total, "active": policies_active},
        "audit": {"total": audit_total, "blocked": audit_blocked, "escalated": audit_escalated},
        "compliance_avg": round(avg_compliance, 1),
        "recent_audit": recent_audit,
        "risk_distribution": risk_dist
    }

# ============ AGENTS CRUD ============

@api_router.get("/agents", response_model=List[Agent])
async def list_agents(status: Optional[str] = None, risk_level: Optional[str] = None):
    query = {}
    if status:
        query["status"] = status
    if risk_level:
        query["risk_level"] = risk_level
    agents = await db.agents.find(query, {"_id": 0}).to_list(100)
    return agents

@api_router.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    agent = await db.agents.find_one({"id": agent_id}, {"_id": 0})
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@api_router.post("/agents", response_model=Agent)
async def create_agent(data: AgentCreate):
    agent = Agent(**data.model_dump())
    doc = agent.model_dump()
    await db.agents.insert_one(doc)
    log = AuditLog(agent_name=agent.name, action="agent_created", resource=f"/agents/{agent.id}", outcome=AuditOutcome.allowed, details=f"Agent '{agent.name}' created", user="admin")
    await db.audit_logs.insert_one(log.model_dump())
    result = await db.agents.find_one({"id": agent.id}, {"_id": 0})
    return result

@api_router.put("/agents/{agent_id}", response_model=Agent)
async def update_agent(agent_id: str, data: AgentCreate):
    existing = await db.agents.find_one({"id": agent_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Agent not found")
    update_data = data.model_dump()
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    await db.agents.update_one({"id": agent_id}, {"$set": update_data})
    log = AuditLog(agent_name=data.name, action="agent_updated", resource=f"/agents/{agent_id}", outcome=AuditOutcome.allowed, details=f"Agent '{data.name}' updated", user="admin")
    await db.audit_logs.insert_one(log.model_dump())
    result = await db.agents.find_one({"id": agent_id}, {"_id": 0})
    return result

@api_router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    existing = await db.agents.find_one({"id": agent_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Agent not found")
    await db.agents.delete_one({"id": agent_id})
    log = AuditLog(agent_name=existing.get("name", ""), action="agent_deleted", resource=f"/agents/{agent_id}", outcome=AuditOutcome.allowed, details=f"Agent '{existing.get('name', '')}' deleted", user="admin")
    await db.audit_logs.insert_one(log.model_dump())
    return {"status": "deleted", "id": agent_id}

# ============ POLICIES CRUD ============

@api_router.get("/policies", response_model=List[Policy])
async def list_policies(regulation: Optional[str] = None, severity: Optional[str] = None):
    query = {}
    if regulation:
        query["regulation"] = regulation
    if severity:
        query["severity"] = severity
    policies = await db.policies.find(query, {"_id": 0}).to_list(100)
    return policies

@api_router.post("/policies", response_model=Policy)
async def create_policy(data: PolicyCreate):
    policy = Policy(**data.model_dump())
    doc = policy.model_dump()
    await db.policies.insert_one(doc)
    log = AuditLog(policy_name=policy.name, action="policy_created", resource=f"/policies/{policy.id}", outcome=AuditOutcome.allowed, details=f"Policy '{policy.name}' created", user="admin")
    await db.audit_logs.insert_one(log.model_dump())
    result = await db.policies.find_one({"id": policy.id}, {"_id": 0})
    return result

@api_router.put("/policies/{policy_id}", response_model=Policy)
async def update_policy(policy_id: str, data: PolicyCreate):
    existing = await db.policies.find_one({"id": policy_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Policy not found")
    update_data = data.model_dump()
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    await db.policies.update_one({"id": policy_id}, {"$set": update_data})
    log = AuditLog(policy_name=data.name, action="policy_updated", resource=f"/policies/{policy_id}", outcome=AuditOutcome.allowed, details=f"Policy '{data.name}' updated", user="admin")
    await db.audit_logs.insert_one(log.model_dump())
    result = await db.policies.find_one({"id": policy_id}, {"_id": 0})
    return result

@api_router.delete("/policies/{policy_id}")
async def delete_policy(policy_id: str):
    existing = await db.policies.find_one({"id": policy_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Policy not found")
    await db.policies.delete_one({"id": policy_id})
    log = AuditLog(policy_name=existing.get("name", ""), action="policy_deleted", resource=f"/policies/{policy_id}", outcome=AuditOutcome.allowed, details=f"Policy '{existing.get('name', '')}' deleted", user="admin")
    await db.audit_logs.insert_one(log.model_dump())
    return {"status": "deleted", "id": policy_id}

# ============ AUDIT TRAIL ============

@api_router.get("/audit")
async def list_audit_logs(
    outcome: Optional[str] = None,
    risk_level: Optional[str] = None,
    action: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(default=50, le=200),
    skip: int = 0
):
    query = {}
    if outcome:
        query["outcome"] = outcome
    if risk_level:
        query["risk_level"] = risk_level
    if action:
        query["action"] = action
    if search:
        # Fix 1.2: sanitize regex to prevent ReDoS
        safe_search = re.escape(search)
        query["$or"] = [
            {"agent_name": {"$regex": safe_search, "$options": "i"}},
            {"details": {"$regex": safe_search, "$options": "i"}},
            {"user": {"$regex": safe_search, "$options": "i"}},
            {"resource": {"$regex": safe_search, "$options": "i"}},
        ]
    total = await db.audit_logs.count_documents(query)
    logs = await db.audit_logs.find(query, {"_id": 0}).sort("timestamp", -1).skip(skip).limit(limit).to_list(limit)
    return {"total": total, "logs": logs}

# ============ COMPLIANCE ============

@api_router.get("/compliance")
async def list_compliance():
    standards = await db.compliance_standards.find({}, {"_id": 0}).to_list(100)
    return standards

@api_router.put("/compliance/{standard_id}")
async def update_compliance(standard_id: str, data: dict):
    existing = await db.compliance_standards.find_one({"id": standard_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Standard not found")
    allowed_fields = {"status", "progress", "requirements_met", "next_review"}
    update = {k: v for k, v in data.items() if k in allowed_fields}
    update["last_assessment"] = datetime.now(timezone.utc).isoformat()
    await db.compliance_standards.update_one({"id": standard_id}, {"$set": update})
    result = await db.compliance_standards.find_one({"id": standard_id}, {"_id": 0})
    return result

# ============ AI CHAT (Fix 1.4 — history passed to LLM) ============

@api_router.post("/chat")
async def chat_compliance(req: ChatRequest):
    api_key = os.environ.get("EMERGENT_LLM_KEY", "")
    
    system_msg = """You are GOVERN.AI Compliance Assistant, an expert in European AI regulation, data protection, and enterprise governance. You help compliance officers, DPOs, CISOs, and CTOs with:

- EU AI Act compliance (risk classification, obligations, documentation)
- GDPR data protection requirements for AI systems
- ISO 27001 & ISO 42001 standards implementation
- DORA digital operational resilience for financial institutions
- NIS2 cybersecurity obligations
- AI agent governance policies and best practices
- Audit trail requirements and explainability
- Risk assessment for AI deployments

Respond in the same language as the user's message (Italian or English). Be precise, reference specific articles/requirements when possible, and provide actionable guidance. Format responses with clear structure using markdown."""

    # Fix 1.4: Build initial_messages from DB history for conversation memory
    history = await db.chat_messages.find(
        {"session_id": req.session_id}, {"_id": 0}
    ).sort("timestamp", 1).to_list(20)

    initial_messages = [{"role": "system", "content": system_msg}]
    for msg in history:
        if msg["role"] == "user":
            initial_messages.append({"role": "user", "content": [{"type": "text", "text": msg["content"]}]})
        elif msg["role"] == "assistant":
            initial_messages.append({"role": "assistant", "content": msg["content"]})

    chat = LlmChat(
        api_key=api_key,
        session_id=f"govern_ai_{req.session_id}",
        system_message=system_msg,
        initial_messages=initial_messages
    )
    chat.with_model("openai", "gpt-5.2")

    # Save user message BEFORE calling LLM
    now = datetime.now(timezone.utc).isoformat()
    await db.chat_messages.insert_one({
        "id": str(uuid.uuid4()), "session_id": req.session_id,
        "role": "user", "content": req.message, "timestamp": now
    })

    user_message = UserMessage(text=req.message)

    try:
        response = await chat.send_message(user_message)
    except Exception as e:
        # Fix 1.9: Log full error internally, return generic message to client
        logger.error(f"LLM error for session {req.session_id}: {e}")
        raise HTTPException(status_code=500, detail="AI service temporarily unavailable. Please try again.")

    # Save assistant response AFTER LLM call
    now_resp = datetime.now(timezone.utc).isoformat()
    await db.chat_messages.insert_one({
        "id": str(uuid.uuid4()), "session_id": req.session_id,
        "role": "assistant", "content": response, "timestamp": now_resp
    })

    # Audit log for AI interaction
    log = AuditLog(
        action="ai_chat_query", resource="/chat/compliance",
        outcome=AuditOutcome.allowed, details=f"Compliance query: {req.message[:100]}",
        user="admin", agent_name="GOVERN.AI Assistant"
    )
    await db.audit_logs.insert_one(log.model_dump())

    return {"response": response, "session_id": req.session_id}

@api_router.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    messages = await db.chat_messages.find(
        {"session_id": session_id}, {"_id": 0}
    ).sort("timestamp", 1).to_list(100)
    return messages

@api_router.get("/")
async def root():
    return {"message": "GOVERN.AI API - Sovereign AI Control Plane"}

# Include router
app.include_router(api_router)

# Fix 1.3: CORS with allowed origins from env (fallback to wildcard for dev)
allowed_origins_str = os.environ.get('ALLOWED_ORIGINS', '')
if allowed_origins_str:
    cors_origins = [origin.strip() for origin in allowed_origins_str.split(',') if origin.strip()]
else:
    cors_origins = os.environ.get('CORS_ORIGINS', '*').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
