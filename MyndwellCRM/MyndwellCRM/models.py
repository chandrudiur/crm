from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class SurveyStatus(Enum):
    DRAFT = "draft"
    READY = "ready"
    ARCHIVED = "archived"

class DeploymentStatus(Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class QuestionType(Enum):
    SINGLE = "single"
    MULTI = "multi"
    SCALE = "scale"
    FREE = "free"

@dataclass
class Company:
    id: str
    name: str
    domains: List[str]
    status: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class Person:
    id: str
    company_id: str
    email: str
    name: str
    roles: List[str]
    status: UserStatus
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class QuestionChoice:
    code: str
    label: str
    weight: Optional[float] = None

@dataclass
class QuestionValidation:
    required: bool = False
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    regex: Optional[str] = None

@dataclass
class Question:
    id: str
    code: str
    text: str
    type: QuestionType
    choices: List[QuestionChoice] = field(default_factory=list)
    validation: QuestionValidation = field(default_factory=QuestionValidation)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class SurveyQuestion:
    id: str
    survey_template_id: str
    question_id: str
    order: int
    section: str
    branching: Dict[str, Any] = field(default_factory=dict)
    weights: Dict[str, float] = field(default_factory=dict)

@dataclass
class SurveyTemplate:
    id: str
    name: str
    version: str
    program: str
    status: SurveyStatus
    description: str = ""
    questions: List[SurveyQuestion] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class EmailTemplate:
    subject: str
    body: str
    preview_text: str = ""

@dataclass
class Deployment:
    id: str
    company_id: str
    survey_template_id: str
    name: str
    status: DeploymentStatus
    audience_type: str  # 'all', 'segment', 'csv'
    audience_data: Dict[str, Any] = field(default_factory=dict)
    channel: str = "email"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    email_template: Optional[EmailTemplate] = None
    reminders: List[Dict[str, Any]] = field(default_factory=list)
    max_attempts: int = 1
    metrics: Dict[str, int] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class AuditLog:
    id: str
    actor: str
    action: str
    entity_type: str
    entity_id: str
    diff: Dict[str, Any]
    ip_address: str
    user_agent: str
    timestamp: datetime = field(default_factory=datetime.now)
