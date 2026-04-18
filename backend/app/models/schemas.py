"""
Pydantic Schemas for TriageX API
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============ AUTH SCHEMAS ============

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    is_admin: bool = False
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ============ CHAT SCHEMAS ============

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    chat_history: Optional[List[ChatMessage]] = []
    language: str = "en"


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    chat_history: List[ChatMessage]
    is_complete: bool = False
    collected_data: Optional[Dict[str, Any]] = None


# ============ TRIAGE SCHEMAS ============

class SymptomInput(BaseModel):
    symptoms: str = Field(..., min_length=2, description="Comma-separated symptoms or natural language description")
    duration: Optional[str] = None
    intensity: Optional[int] = Field(None, ge=1, le=10)
    medical_history: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    language: str = "en"


class AffectedRegion(BaseModel):
    region: str  # head, chest, abdomen, left_arm, right_arm, left_leg, right_leg, back
    severity: str  # LOW, MEDIUM, HIGH
    color: str  # green, yellow, red
    symptoms: List[str]


class TriggeredRule(BaseModel):
    rule_id: str
    rule_name: str
    description: str
    severity_contribution: float
    matched_symptoms: List[str]


class TriageResult(BaseModel):
    session_id: str
    urgency_level: str  # LOW, MEDIUM, HIGH
    severity_score: float  # 0-100
    recommended_action: str  # self-care, consult-doctor, emergency
    is_emergency: bool = False

    # Extracted Data
    symptoms_extracted: List[str]
    symptom_categories: List[str]

    # Reasoning (XAI)
    triggered_rules: List[TriggeredRule]
    reasoning: str
    key_factors: List[str]

    # Visual Data
    affected_regions: List[AffectedRegion]
    condition_images: List[Dict[str, str]]

    # Summaries
    clinical_summary: str
    patient_summary: str

    # Metadata
    language: str = "en"
    timestamp: Optional[str] = None


# ============ ADMIN SCHEMAS ============

class CaseListItem(BaseModel):
    id: int
    session_id: str
    symptoms_raw: str
    urgency_level: Optional[str] = None
    severity_score: Optional[float] = None
    recommended_action: Optional[str] = None
    is_emergency: int = 0
    created_at: Optional[datetime] = None
    user_id: Optional[int] = None
    username: Optional[str] = None

    class Config:
        from_attributes = True


class CaseDetail(BaseModel):
    id: int
    session_id: str
    symptoms_raw: str
    symptoms_extracted: Optional[List[str]] = None
    duration: Optional[str] = None
    intensity: Optional[int] = None
    medical_history: Optional[str] = None
    chat_history: Optional[List[Dict[str, Any]]] = None
    urgency_level: Optional[str] = None
    severity_score: Optional[float] = None
    recommended_action: Optional[str] = None
    triggered_rules: Optional[List[Dict[str, Any]]] = None
    reasoning: Optional[str] = None
    affected_regions: Optional[List[Dict[str, Any]]] = None
    condition_images: Optional[List[Dict[str, str]]] = None
    is_emergency: int = 0
    language: str = "en"
    created_at: Optional[datetime] = None
    user_id: Optional[int] = None
    username: Optional[str] = None

    class Config:
        from_attributes = True


class AdminStats(BaseModel):
    total_cases: int
    high_severity: int
    medium_severity: int
    low_severity: int
    emergencies: int
    recent_cases: List[CaseListItem]
