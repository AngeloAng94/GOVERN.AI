import random
import uuid
import logging
from datetime import datetime, timezone, timedelta
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
        now = datetime.now(timezone.utc)
        standards = [
            ComplianceStandard(
                name="GDPR",
                code="GDPR",
                description="General Data Protection Regulation - Data protection and privacy regulation for EU citizens",
                status="in_progress",
                progress=78,
                requirements_total=36,
                requirements_met=28,
                category="regulation",
                last_assessment=(now - timedelta(days=15)).isoformat(),
                next_review=(now + timedelta(days=45)).isoformat()
            ),
            ComplianceStandard(
                name="EU AI Act",
                code="EU-AI-ACT",
                description="European Union Artificial Intelligence Act - Regulation on harmonised rules for AI systems",
                status="in_progress",
                progress=45,
                requirements_total=42,
                requirements_met=19,
                category="regulation",
                last_assessment=(now - timedelta(days=7)).isoformat(),
                next_review=(now + timedelta(days=23)).isoformat()
            ),
            ComplianceStandard(
                name="ISO 27001",
                code="ISO-27001",
                description="Information Security Management Systems - International standard for managing information security",
                status="compliant",
                progress=92,
                requirements_total=114,
                requirements_met=107,
                category="standard",
                last_assessment=(now - timedelta(days=30)).isoformat(),
                next_review=(now + timedelta(days=335)).isoformat()
            ),
            ComplianceStandard(
                name="ISO 42001",
                code="ISO-42001",
                description="AI Management System - International standard for responsible AI governance",
                status="in_progress",
                progress=34,
                requirements_total=35,
                requirements_met=12,
                category="standard",
                last_assessment=(now - timedelta(days=3)).isoformat(),
                next_review=(now + timedelta(days=87)).isoformat()
            ),
            ComplianceStandard(
                name="DORA",
                code="DORA",
                description="Digital Operational Resilience Act - Financial sector digital resilience regulation",
                status="in_progress",
                progress=61,
                requirements_total=51,
                requirements_met=31,
                category="regulation",
                last_assessment=(now - timedelta(days=10)).isoformat(),
                next_review=(now + timedelta(days=20)).isoformat()
            ),
            ComplianceStandard(
                name="NIS2",
                code="NIS2",
                description="Network and Information Security Directive 2 - Cybersecurity obligations for essential services",
                status="in_progress",
                progress=83,
                requirements_total=53,
                requirements_met=44,
                category="directive",
                last_assessment=(now - timedelta(days=20)).isoformat(),
                next_review=(now + timedelta(days=40)).isoformat()
            ),
        ]
        for s in standards:
            await db.compliance_standards.insert_one(s.model_dump())
        logger.info("Seeded compliance standards (6 standards)")


async def seed_sample_data():
    agent_count = await db.agents.count_documents({})
    if agent_count == 0:
        # 12 Enterprise Banking Agents
        agents = [
            AgentCreate(
                name="Customer Due Diligence Bot",
                description="Automated KYC document analysis and identity verification for onboarding",
                model_type="GPT-5.2",
                risk_level=RiskLevel.high,
                status=AgentStatus.active,
                allowed_actions=["analyze_documents", "verify_identity", "flag_suspicious_activity"],
                restricted_domains=["personal_data_export", "external_api_calls"],
                data_classification=DataClassification.confidential,
                owner="Compliance Dept"
            ),
            AgentCreate(
                name="AML Transaction Monitor",
                description="Real-time anti-money laundering surveillance for suspicious transaction patterns",
                model_type="GPT-5.2",
                risk_level=RiskLevel.critical,
                status=AgentStatus.active,
                allowed_actions=["monitor_transactions", "generate_sar", "freeze_account_request"],
                restricted_domains=["customer_communication", "account_modification"],
                data_classification=DataClassification.restricted,
                owner="AML Team"
            ),
            AgentCreate(
                name="Credit Risk Assessor",
                description="Evaluates creditworthiness using financial data and behavioral analytics",
                model_type="Claude-3.5",
                risk_level=RiskLevel.high,
                status=AgentStatus.active,
                allowed_actions=["analyze_creditworthiness", "generate_report"],
                restricted_domains=["loan_approval", "external_data"],
                data_classification=DataClassification.confidential,
                owner="Credit Risk Dept"
            ),
            AgentCreate(
                name="Customer Service Assistant",
                description="Handles routine customer inquiries via digital banking channels",
                model_type="GPT-5.2",
                risk_level=RiskLevel.low,
                status=AgentStatus.active,
                allowed_actions=["answer_faq", "escalate_ticket", "check_balance_info"],
                restricted_domains=["account_modification", "personal_data_export"],
                data_classification=DataClassification.internal,
                owner="Digital Banking"
            ),
            AgentCreate(
                name="Regulatory Reporting Agent",
                description="Compiles and validates regulatory reports for Bank of Italy and ECB",
                model_type="GPT-4o",
                risk_level=RiskLevel.medium,
                status=AgentStatus.active,
                allowed_actions=["compile_reports", "validate_data", "submit_to_regulator"],
                restricted_domains=["external_communication"],
                data_classification=DataClassification.confidential,
                owner="Regulatory Affairs"
            ),
            AgentCreate(
                name="HR Policy Assistant",
                description="Assists employees with HR policies, leave requests and benefits queries",
                model_type="GPT-5.2",
                risk_level=RiskLevel.low,
                status=AgentStatus.active,
                allowed_actions=["answer_hr_queries", "process_leave_requests"],
                restricted_domains=["salary_data", "personal_records"],
                data_classification=DataClassification.internal,
                owner="Human Resources"
            ),
            AgentCreate(
                name="Fraud Detection Engine",
                description="ML-based real-time fraud detection for card and digital transactions",
                model_type="Custom-ML-v3",
                risk_level=RiskLevel.critical,
                status=AgentStatus.active,
                allowed_actions=["analyze_patterns", "block_transaction", "alert_human_reviewer"],
                restricted_domains=["customer_communication"],
                data_classification=DataClassification.restricted,
                owner="Fraud Team"
            ),
            AgentCreate(
                name="Investment Advisory Bot",
                description="Provides personalized investment recommendations for wealth management clients",
                model_type="GPT-5.2",
                risk_level=RiskLevel.high,
                status=AgentStatus.suspended,
                allowed_actions=["analyze_portfolio", "generate_recommendations"],
                restricted_domains=["execute_trades", "direct_customer_contact"],
                data_classification=DataClassification.confidential,
                owner="Wealth Management"
            ),
            AgentCreate(
                name="Document Classifier",
                description="Automatically classifies and routes incoming documents to appropriate departments",
                model_type="Claude-3.5",
                risk_level=RiskLevel.low,
                status=AgentStatus.active,
                allowed_actions=["classify_documents", "extract_data", "route_to_department"],
                restricted_domains=["external_storage"],
                data_classification=DataClassification.internal,
                owner="Operations"
            ),
            AgentCreate(
                name="DORA Incident Responder",
                description="Monitors ICT incidents and generates DORA-compliant incident reports",
                model_type="GPT-5.2",
                risk_level=RiskLevel.high,
                status=AgentStatus.active,
                allowed_actions=["detect_incidents", "notify_stakeholders", "generate_incident_report"],
                restricted_domains=["system_modification"],
                data_classification=DataClassification.confidential,
                owner="IT Security"
            ),
            AgentCreate(
                name="KYC Verification Agent",
                description="Cross-references identity documents with sanctions and PEP lists",
                model_type="GPT-4o",
                risk_level=RiskLevel.high,
                status=AgentStatus.active,
                allowed_actions=["verify_identity_documents", "cross_reference_sanctions_list"],
                restricted_domains=["personal_data_export", "external_api_calls"],
                data_classification=DataClassification.restricted,
                owner="Compliance Dept"
            ),
            AgentCreate(
                name="Executive Report Generator",
                description="Aggregates KPIs and generates board-ready executive dashboards",
                model_type="GPT-5.2",
                risk_level=RiskLevel.medium,
                status=AgentStatus.active,
                allowed_actions=["aggregate_kpis", "generate_board_report", "format_presentation"],
                restricted_domains=["external_communication", "raw_data_export"],
                data_classification=DataClassification.confidential,
                owner="C-Suite Office"
            ),
        ]
        
        for a in agents:
            agent_obj = Agent(**a.model_dump())
            await db.agents.insert_one(agent_obj.model_dump())
        
        # 15 Enterprise Policies
        policies = [
            # GDPR Policies (3)
            PolicyCreate(
                name="PII Data Minimization",
                description="Enforce data minimization principle - collect only necessary personal data",
                rule_type=RuleType.restriction,
                conditions=["data_request_exceeds_scope", "unnecessary_pii_collection"],
                actions=["block_request", "log_violation", "notify_dpo"],
                severity=PolicySeverity.high,
                regulation="GDPR",
                enforcement=PolicyEnforcement.block,
                violations_count=3
            ),
            PolicyCreate(
                name="Consent Verification",
                description="Verify valid consent before processing personal data for secondary purposes",
                rule_type=RuleType.approval,
                conditions=["secondary_data_use", "marketing_purpose"],
                actions=["request_consent_verification", "pause_processing"],
                severity=PolicySeverity.critical,
                regulation="GDPR",
                enforcement=PolicyEnforcement.block,
                violations_count=1
            ),
            PolicyCreate(
                name="Data Breach Notification",
                description="Automatic notification workflow for personal data breaches within 72 hours",
                rule_type=RuleType.logging,
                conditions=["data_breach_detected", "pii_exposure"],
                actions=["alert_dpo", "initiate_breach_protocol", "log_incident"],
                severity=PolicySeverity.critical,
                regulation="GDPR",
                enforcement=PolicyEnforcement.auto,
                violations_count=0
            ),
            # EU AI Act Policies (3)
            PolicyCreate(
                name="High-Risk AI Oversight",
                description="Mandatory human oversight for AI systems classified as high-risk under EU AI Act",
                rule_type=RuleType.approval,
                conditions=["ai_classification_high_risk", "automated_decision"],
                actions=["require_human_approval", "log_decision_chain", "store_explainability"],
                severity=PolicySeverity.critical,
                regulation="EU-AI-ACT",
                enforcement=PolicyEnforcement.block,
                violations_count=7
            ),
            PolicyCreate(
                name="AI Transparency Disclosure",
                description="Ensure users are informed when interacting with AI systems",
                rule_type=RuleType.logging,
                conditions=["user_interaction_start", "chatbot_session"],
                actions=["display_ai_disclosure", "log_acknowledgment"],
                severity=PolicySeverity.medium,
                regulation="EU-AI-ACT",
                enforcement=PolicyEnforcement.log,
                violations_count=2
            ),
            PolicyCreate(
                name="Human-in-the-Loop Critical Decisions",
                description="Require human approval for financial decisions exceeding thresholds",
                rule_type=RuleType.approval,
                conditions=["financial_decision", "amount_exceeds_threshold", "credit_decision"],
                actions=["pause_execution", "request_supervisor_approval", "log_decision"],
                severity=PolicySeverity.critical,
                regulation="EU-AI-ACT",
                enforcement=PolicyEnforcement.block,
                violations_count=12
            ),
            # DORA Policies (2)
            PolicyCreate(
                name="ICT Incident Reporting",
                description="Automatic reporting of major ICT incidents to competent authorities",
                rule_type=RuleType.logging,
                conditions=["ict_incident_major", "service_disruption"],
                actions=["generate_incident_report", "notify_regulator", "escalate_to_ciso"],
                severity=PolicySeverity.high,
                regulation="DORA",
                enforcement=PolicyEnforcement.auto,
                violations_count=0
            ),
            PolicyCreate(
                name="Digital Resilience Testing",
                description="Enforce regular threat-led penetration testing for critical systems",
                rule_type=RuleType.retention,
                conditions=["critical_system_change", "quarterly_review"],
                actions=["schedule_tlpt", "document_results", "remediate_findings"],
                severity=PolicySeverity.medium,
                regulation="DORA",
                enforcement=PolicyEnforcement.log,
                violations_count=1
            ),
            # NIS2 Policies (2)
            PolicyCreate(
                name="Security Measures Implementation",
                description="Ensure baseline security measures for network and information systems",
                rule_type=RuleType.restriction,
                conditions=["system_deployment", "configuration_change"],
                actions=["validate_security_baseline", "block_if_non_compliant"],
                severity=PolicySeverity.high,
                regulation="NIS2",
                enforcement=PolicyEnforcement.block,
                violations_count=4
            ),
            PolicyCreate(
                name="Incident Notification 24h",
                description="Notify CSIRT within 24 hours of significant cyber incidents",
                rule_type=RuleType.logging,
                conditions=["cyber_incident_significant", "data_breach"],
                actions=["immediate_notification", "preserve_evidence", "initiate_response"],
                severity=PolicySeverity.critical,
                regulation="NIS2",
                enforcement=PolicyEnforcement.auto,
                violations_count=0
            ),
            # ISO 42001 Policies (2)
            PolicyCreate(
                name="AI Risk Assessment",
                description="Conduct risk assessment before deploying new AI agents or updating existing ones",
                rule_type=RuleType.approval,
                conditions=["new_ai_deployment", "ai_model_update"],
                actions=["initiate_risk_assessment", "document_risks", "require_approval"],
                severity=PolicySeverity.medium,
                regulation="ISO-42001",
                enforcement=PolicyEnforcement.block,
                violations_count=5
            ),
            PolicyCreate(
                name="AI System Documentation",
                description="Maintain comprehensive documentation for all AI systems in production",
                rule_type=RuleType.logging,
                conditions=["ai_system_active", "documentation_outdated"],
                actions=["flag_documentation_gap", "schedule_update"],
                severity=PolicySeverity.low,
                regulation="ISO-42001",
                enforcement=PolicyEnforcement.log,
                violations_count=8
            ),
            # ISO 27001 Policies (2)
            PolicyCreate(
                name="Access Control Enforcement",
                description="Enforce least-privilege access and regular access reviews",
                rule_type=RuleType.restriction,
                conditions=["access_request", "privilege_escalation"],
                actions=["verify_authorization", "log_access_attempt", "block_if_unauthorized"],
                severity=PolicySeverity.high,
                regulation="ISO-27001",
                enforcement=PolicyEnforcement.block,
                violations_count=6
            ),
            PolicyCreate(
                name="Audit Log Integrity",
                description="Ensure immutability and retention of security audit logs",
                rule_type=RuleType.logging,
                conditions=["log_modification_attempt", "log_deletion_request"],
                actions=["block_modification", "alert_soc", "preserve_original"],
                severity=PolicySeverity.critical,
                regulation="ISO-27001",
                enforcement=PolicyEnforcement.block,
                violations_count=0
            ),
            # Cross-regulatory Policy (1)
            PolicyCreate(
                name="Data Retention 7 Years",
                description="Retain financial and compliance data for minimum 7 years as per regulatory requirements",
                rule_type=RuleType.retention,
                conditions=["data_age_check", "deletion_request"],
                actions=["verify_retention_period", "block_premature_deletion", "archive_if_expired"],
                severity=PolicySeverity.medium,
                regulation="GDPR",
                enforcement=PolicyEnforcement.auto,
                violations_count=2
            ),
        ]
        
        for p in policies:
            policy_obj = Policy(**p.model_dump())
            await db.policies.insert_one(policy_obj.model_dump())
        
        # 150 Audit Logs over last 30 days
        agent_names = [
            "Customer Due Diligence Bot", "AML Transaction Monitor", "Credit Risk Assessor",
            "Customer Service Assistant", "Regulatory Reporting Agent", "HR Policy Assistant",
            "Fraud Detection Engine", "Investment Advisory Bot", "Document Classifier",
            "DORA Incident Responder", "KYC Verification Agent", "Executive Report Generator"
        ]
        
        # Define agent-specific behavior patterns
        agent_profiles = {
            "Customer Service Assistant": {"allowed": 0.95, "blocked": 0.03, "escalated": 0.02},
            "HR Policy Assistant": {"allowed": 0.92, "blocked": 0.05, "escalated": 0.03},
            "Document Classifier": {"allowed": 0.90, "blocked": 0.07, "escalated": 0.03},
            "AML Transaction Monitor": {"allowed": 0.55, "blocked": 0.30, "escalated": 0.15},
            "Fraud Detection Engine": {"allowed": 0.50, "blocked": 0.35, "escalated": 0.15},
            "Credit Risk Assessor": {"allowed": 0.65, "blocked": 0.20, "escalated": 0.15},
            "Customer Due Diligence Bot": {"allowed": 0.70, "blocked": 0.18, "escalated": 0.12},
            "KYC Verification Agent": {"allowed": 0.68, "blocked": 0.22, "escalated": 0.10},
            "Investment Advisory Bot": {"allowed": 0.60, "blocked": 0.25, "escalated": 0.15},
            "Regulatory Reporting Agent": {"allowed": 0.85, "blocked": 0.10, "escalated": 0.05},
            "DORA Incident Responder": {"allowed": 0.75, "blocked": 0.15, "escalated": 0.10},
            "Executive Report Generator": {"allowed": 0.88, "blocked": 0.08, "escalated": 0.04},
        }
        
        actions_by_agent = {
            "AML Transaction Monitor": ["transaction_analysis", "sar_generation", "account_freeze_request", "pattern_detection"],
            "Fraud Detection Engine": ["fraud_check", "transaction_block", "alert_generation", "risk_scoring"],
            "Credit Risk Assessor": ["credit_evaluation", "report_generation", "data_analysis", "risk_calculation"],
            "Customer Service Assistant": ["inquiry_response", "ticket_creation", "balance_check", "faq_lookup"],
            "Customer Due Diligence Bot": ["document_verification", "identity_check", "sanction_screening", "risk_flagging"],
            "KYC Verification Agent": ["document_analysis", "pep_check", "sanction_list_query", "verification_report"],
            "HR Policy Assistant": ["policy_inquiry", "leave_processing", "benefits_query", "document_request"],
            "Document Classifier": ["document_classification", "data_extraction", "routing_decision", "metadata_tagging"],
            "Regulatory Reporting Agent": ["report_compilation", "data_validation", "submission_preparation", "compliance_check"],
            "DORA Incident Responder": ["incident_detection", "stakeholder_notification", "report_generation", "severity_assessment"],
            "Investment Advisory Bot": ["portfolio_analysis", "recommendation_generation", "market_research", "risk_assessment"],
            "Executive Report Generator": ["kpi_aggregation", "dashboard_update", "report_formatting", "data_consolidation"],
        }
        
        resources_by_agent = {
            "AML Transaction Monitor": ["/transactions/wire", "/transactions/card", "/accounts/high-value", "/data/sanctions"],
            "Fraud Detection Engine": ["/transactions/realtime", "/fraud/patterns", "/alerts/queue", "/models/fraud-v3"],
            "Credit Risk Assessor": ["/credit/applications", "/data/bureau", "/reports/risk", "/models/credit-scoring"],
            "Customer Service Assistant": ["/faq/database", "/tickets/queue", "/accounts/summary", "/chat/sessions"],
            "Customer Due Diligence Bot": ["/kyc/documents", "/identity/verification", "/sanctions/screening", "/customers/onboarding"],
            "KYC Verification Agent": ["/kyc/documents", "/pep/database", "/sanctions/lists", "/verification/queue"],
            "HR Policy Assistant": ["/hr/policies", "/leave/requests", "/benefits/info", "/employees/directory"],
            "Document Classifier": ["/documents/incoming", "/classification/models", "/routing/rules", "/metadata/store"],
            "Regulatory Reporting Agent": ["/reports/regulatory", "/data/validation", "/submissions/ecb", "/compliance/status"],
            "DORA Incident Responder": ["/incidents/log", "/ict/monitoring", "/notifications/queue", "/reports/dora"],
            "Investment Advisory Bot": ["/portfolios/clients", "/market/data", "/recommendations/queue", "/research/reports"],
            "Executive Report Generator": ["/kpis/realtime", "/dashboards/executive", "/reports/board", "/data/consolidated"],
        }
        
        users = [
            "m.rossi@bancaenterprise.it", "g.bianchi@bancaenterprise.it", 
            "l.ferrari@bancaenterprise.it", "a.romano@bancaenterprise.it",
            "p.conti@bancaenterprise.it", "s.moretti@bancaenterprise.it",
            "f.ricci@bancaenterprise.it", "system"
        ]
        
        now = datetime.now(timezone.utc)
        
        # Generate 150 audit logs
        audit_logs = []
        
        # First, create 5 incident clusters (sequences of related events)
        incident_clusters = [
            # Cluster 1: AML suspicious activity detected and escalated (Day -5)
            {
                "agent": "AML Transaction Monitor",
                "day_offset": -5,
                "events": [
                    ("transaction_analysis", "/transactions/wire", AuditOutcome.allowed, RiskLevel.medium, "Routine wire transfer analysis"),
                    ("pattern_detection", "/transactions/wire", AuditOutcome.escalated, RiskLevel.high, "Suspicious pattern detected - multiple small transfers"),
                    ("sar_generation", "/data/sanctions", AuditOutcome.allowed, RiskLevel.high, "SAR report initiated"),
                    ("account_freeze_request", "/accounts/high-value", AuditOutcome.blocked, RiskLevel.critical, "Freeze request pending supervisor approval"),
                    ("account_freeze_request", "/accounts/high-value", AuditOutcome.allowed, RiskLevel.critical, "Account frozen after supervisor approval"),
                ]
            },
            # Cluster 2: GDPR data export attempt blocked (Day -12)
            {
                "agent": "Customer Due Diligence Bot",
                "day_offset": -12,
                "events": [
                    ("document_verification", "/kyc/documents", AuditOutcome.allowed, RiskLevel.low, "Standard document verification"),
                    ("identity_check", "/customers/onboarding", AuditOutcome.allowed, RiskLevel.medium, "Identity verified"),
                    ("sanction_screening", "/data/sanctions", AuditOutcome.blocked, RiskLevel.high, "Attempted export of PII - blocked by GDPR policy"),
                    ("risk_flagging", "/customers/onboarding", AuditOutcome.escalated, RiskLevel.high, "Incident escalated to DPO"),
                ]
            },
            # Cluster 3: Fraud detection and response (Day -3)
            {
                "agent": "Fraud Detection Engine",
                "day_offset": -3,
                "events": [
                    ("fraud_check", "/transactions/realtime", AuditOutcome.allowed, RiskLevel.low, "Routine transaction check"),
                    ("fraud_check", "/transactions/realtime", AuditOutcome.allowed, RiskLevel.low, "Routine transaction check"),
                    ("risk_scoring", "/models/fraud-v3", AuditOutcome.escalated, RiskLevel.high, "High fraud score detected"),
                    ("transaction_block", "/transactions/realtime", AuditOutcome.blocked, RiskLevel.critical, "Transaction blocked - suspected card fraud"),
                    ("alert_generation", "/alerts/queue", AuditOutcome.allowed, RiskLevel.high, "Alert sent to fraud investigation team"),
                ]
            },
            # Cluster 4: Credit decision requiring human approval (Day -8)
            {
                "agent": "Credit Risk Assessor",
                "day_offset": -8,
                "events": [
                    ("data_analysis", "/data/bureau", AuditOutcome.allowed, RiskLevel.medium, "Credit bureau data retrieved"),
                    ("credit_evaluation", "/credit/applications", AuditOutcome.allowed, RiskLevel.medium, "Creditworthiness analysis completed"),
                    ("risk_calculation", "/models/credit-scoring", AuditOutcome.escalated, RiskLevel.high, "High-value loan - human approval required"),
                    ("report_generation", "/reports/risk", AuditOutcome.blocked, RiskLevel.high, "Awaiting supervisor decision"),
                    ("report_generation", "/reports/risk", AuditOutcome.allowed, RiskLevel.high, "Credit report finalized after approval"),
                ]
            },
            # Cluster 5: DORA incident response (Day -1)
            {
                "agent": "DORA Incident Responder",
                "day_offset": -1,
                "events": [
                    ("incident_detection", "/ict/monitoring", AuditOutcome.allowed, RiskLevel.medium, "Minor service degradation detected"),
                    ("severity_assessment", "/incidents/log", AuditOutcome.escalated, RiskLevel.high, "Severity upgraded - affects critical services"),
                    ("stakeholder_notification", "/notifications/queue", AuditOutcome.allowed, RiskLevel.high, "CISO and CTO notified"),
                    ("report_generation", "/reports/dora", AuditOutcome.allowed, RiskLevel.high, "DORA incident report generated"),
                ]
            },
        ]
        
        # Add incident cluster events
        for cluster in incident_clusters:
            base_time = now + timedelta(days=cluster["day_offset"], hours=random.randint(9, 17))
            for i, (action, resource, outcome, risk, details) in enumerate(cluster["events"]):
                event_time = base_time + timedelta(minutes=i * random.randint(5, 30))
                log = AuditLog(
                    agent_name=cluster["agent"],
                    action=action,
                    resource=resource,
                    outcome=outcome,
                    details=details,
                    risk_level=risk,
                    ip_address=f"10.0.{random.randint(1,5)}.{random.randint(1,254)}",
                    user=random.choice(users),
                    timestamp=event_time.isoformat()
                )
                audit_logs.append(log)
        
        # Generate remaining random logs to reach 150 total
        remaining_count = 150 - len(audit_logs)
        for _ in range(remaining_count):
            agent_name = random.choice(agent_names)
            profile = agent_profiles.get(agent_name, {"allowed": 0.70, "blocked": 0.20, "escalated": 0.10})
            
            # Determine outcome based on agent profile
            rand = random.random()
            if rand < profile["allowed"]:
                outcome = AuditOutcome.allowed
            elif rand < profile["allowed"] + profile["blocked"]:
                outcome = AuditOutcome.blocked
            else:
                outcome = AuditOutcome.escalated
            
            # Set risk level based on outcome
            if outcome == AuditOutcome.blocked:
                risk = random.choices(
                    [RiskLevel.medium, RiskLevel.high, RiskLevel.critical],
                    weights=[0.3, 0.5, 0.2]
                )[0]
            elif outcome == AuditOutcome.escalated:
                risk = random.choices(
                    [RiskLevel.medium, RiskLevel.high, RiskLevel.critical],
                    weights=[0.2, 0.5, 0.3]
                )[0]
            else:
                risk = random.choices(
                    [RiskLevel.low, RiskLevel.medium, RiskLevel.high],
                    weights=[0.5, 0.35, 0.15]
                )[0]
            
            actions = actions_by_agent.get(agent_name, ["data_access", "api_call"])
            resources = resources_by_agent.get(agent_name, ["/data/generic"])
            
            # Random timestamp in last 30 days
            days_ago = random.randint(0, 30)
            hours_offset = random.randint(0, 23)
            minutes_offset = random.randint(0, 59)
            event_time = now - timedelta(days=days_ago, hours=hours_offset, minutes=minutes_offset)
            
            log = AuditLog(
                agent_name=agent_name,
                action=random.choice(actions),
                resource=random.choice(resources),
                outcome=outcome,
                details=f"Automated audit event - {agent_name.split()[0]} operation",
                risk_level=risk,
                ip_address=f"10.0.{random.randint(1,5)}.{random.randint(1,254)}",
                user=random.choice(users),
                timestamp=event_time.isoformat()
            )
            audit_logs.append(log)
        
        # Insert all audit logs
        for log in audit_logs:
            await db.audit_logs.insert_one(log.model_dump())
        
        logger.info(f"Seeded enterprise data: 12 agents, 15 policies, {len(audit_logs)} audit logs")


async def seed_database():
    await seed_admin()
    await seed_compliance_standards()
    await seed_sample_data()
