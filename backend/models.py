from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone

# ============ ENUMS ============

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

class UserRole(str, Enum):
    admin = "admin"
    dpo = "dpo"
    auditor = "auditor"
    viewer = "viewer"

ROLE_HIERARCHY = {"admin": 4, "dpo": 3, "auditor": 2, "viewer": 1}

# ============ USER MODELS ============

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.viewer
    full_name: str = ""

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    username: str
    email: str
    role: str
    full_name: str = ""
    created_at: str = ""

# ============ AGENT MODELS ============

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

# ============ POLICY MODELS ============

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

# ============ AUDIT MODEL ============

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

# ============ COMPLIANCE MODEL ============

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

# ============ SOX WIZARD MODEL ============

class ControlStatus(str, Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"
    not_applicable = "not_applicable"

class SoxControl(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    domain: str
    control_id: str
    title: str
    description: str
    section: str = "404"
    status: ControlStatus = ControlStatus.not_started
    evidence: str = ""
    assignee: str = ""
    due_date: str = ""
    completed_date: str = ""
    risk_level: str = "medium"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

# ============ CHAT MODEL ============

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
