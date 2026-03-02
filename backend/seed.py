import random
import uuid
import logging
from datetime import datetime, timezone
from passlib.context import CryptContext

from database import db
from models import (
    Agent, AgentCreate, Policy, PolicyCreate, AuditLog, ComplianceStandard,
    RiskLevel, AgentStatus, DataClassification, RuleType,
    PolicySeverity, PolicyEnforcement, AuditOutcome,
)

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def seed_admin():
    existing = await db.users.find_one({"username": "admin"})
    if not existing:
        admin = {
            "id": str(uuid.uuid4()),
            "username": "admin",
            "email": "admin@govern.ai",
            "password_hash": pwd_context.hash("AdminGovern2026!"),
            "role": "admin",
            "full_name": "System Administrator",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.insert_one(admin)
        logger.info("Seeded default admin user")


async def seed_compliance_standards():
    count = await db.compliance_standards.count_documents({})
    if count == 0:
        standards = [
            ComplianceStandard(name="EU AI Act", code="EU-AI-ACT", description="European Union Artificial Intelligence Act - Regulation on harmonised rules for AI systems", status="in_progress", progress=68, requirements_total=42, requirements_met=28, category="regulation", next_review="2026-06-01T00:00:00Z"),
            ComplianceStandard(name="GDPR", code="GDPR", description="General Data Protection Regulation - Data protection and privacy regulation", status="compliant", progress=92, requirements_total=35, requirements_met=32, category="regulation", next_review="2026-04-15T00:00:00Z"),
            ComplianceStandard(name="ISO 27001", code="ISO-27001", description="Information Security Management Systems - International standard for managing information security", status="in_progress", progress=75, requirements_total=28, requirements_met=21, category="standard", next_review="2026-05-20T00:00:00Z"),
            ComplianceStandard(name="ISO 42001", code="ISO-42001", description="AI Management System - International standard for responsible AI governance", status="in_progress", progress=45, requirements_total=30, requirements_met=13, category="standard", next_review="2026-07-01T00:00:00Z"),
            ComplianceStandard(name="DORA", code="DORA", description="Digital Operational Resilience Act - Financial sector digital resilience", status="non_compliant", progress=32, requirements_total=25, requirements_met=8, category="regulation", next_review="2026-03-30T00:00:00Z"),
            ComplianceStandard(name="NIS2", code="NIS2", description="Network and Information Security Directive 2 - Cybersecurity obligations", status="in_progress", progress=58, requirements_total=20, requirements_met=11, category="directive", next_review="2026-05-01T00:00:00Z"),
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
        actions_list = ["data_access", "model_inference", "api_call", "policy_check", "document_scan", "user_query", "report_generation", "data_export"]
        outcomes = [AuditOutcome.allowed, AuditOutcome.blocked, AuditOutcome.logged, AuditOutcome.escalated]
        resources = ["/data/customers", "/models/gpt5", "/api/external/crm", "/documents/legal", "/reports/quarterly", "/data/transactions"]
        agent_names = ["Customer Service Bot", "Document Analyzer", "Risk Assessment Engine", "HR Onboarding Assistant"]
        users = ["m.rossi@company.it", "g.bianchi@company.it", "l.ferrari@company.it", "system", "a.romano@company.it"]
        risk_levels = [RiskLevel.low, RiskLevel.medium, RiskLevel.high, RiskLevel.critical]
        for i in range(25):
            log = AuditLog(agent_name=random.choice(agent_names), action=random.choice(actions_list), resource=random.choice(resources), outcome=random.choice(outcomes), details=f"Automated audit event #{i+1}", risk_level=random.choice(risk_levels), ip_address=f"10.0.{random.randint(1,5)}.{random.randint(1,254)}", user=random.choice(users))
            await db.audit_logs.insert_one(log.model_dump())
        logger.info("Seeded sample agents, policies, and audit logs")


async def seed_database():
    await seed_admin()
    await seed_compliance_standards()
    await seed_sample_data()
