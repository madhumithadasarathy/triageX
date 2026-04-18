"""
TriageX Admin Routes
Dashboard APIs for viewing and managing triage cases.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional

from app.database import get_db
from app.models.triage_case import TriageCase
from app.models.user import User
from app.models.schemas import CaseListItem, CaseDetail, AdminStats

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stats", response_model=AdminStats)
async def get_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics."""
    total = db.query(func.count(TriageCase.id)).scalar() or 0
    high = db.query(func.count(TriageCase.id)).filter(TriageCase.urgency_level == "HIGH").scalar() or 0
    medium = db.query(func.count(TriageCase.id)).filter(TriageCase.urgency_level == "MEDIUM").scalar() or 0
    low = db.query(func.count(TriageCase.id)).filter(TriageCase.urgency_level == "LOW").scalar() or 0
    emergencies = db.query(func.count(TriageCase.id)).filter(TriageCase.is_emergency == 1).scalar() or 0

    recent = db.query(TriageCase).order_by(desc(TriageCase.created_at)).limit(10).all()
    recent_items = []
    for case in recent:
        username = None
        if case.user_id:
            user = db.query(User).filter(User.id == case.user_id).first()
            username = user.username if user else None
        recent_items.append(CaseListItem(
            id=case.id,
            session_id=case.session_id,
            symptoms_raw=case.symptoms_raw,
            urgency_level=case.urgency_level,
            severity_score=case.severity_score,
            recommended_action=case.recommended_action,
            is_emergency=case.is_emergency,
            created_at=case.created_at,
            user_id=case.user_id,
            username=username
        ))

    return AdminStats(
        total_cases=total,
        high_severity=high,
        medium_severity=medium,
        low_severity=low,
        emergencies=emergencies,
        recent_cases=recent_items
    )


@router.get("/cases")
async def list_cases(
    severity: Optional[str] = Query(None, description="Filter by urgency: LOW, MEDIUM, HIGH"),
    search: Optional[str] = Query(None, description="Search in symptoms"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """List all triage cases with filtering and pagination."""
    query = db.query(TriageCase)

    if severity:
        query = query.filter(TriageCase.urgency_level == severity.upper())

    if search:
        query = query.filter(TriageCase.symptoms_raw.ilike(f"%{search}%"))

    total = query.count()
    cases = query.order_by(desc(TriageCase.created_at)).offset(offset).limit(limit).all()

    items = []
    for case in cases:
        username = None
        if case.user_id:
            user = db.query(User).filter(User.id == case.user_id).first()
            username = user.username if user else None
        items.append({
            "id": case.id,
            "session_id": case.session_id,
            "symptoms_raw": case.symptoms_raw,
            "urgency_level": case.urgency_level,
            "severity_score": case.severity_score,
            "recommended_action": case.recommended_action,
            "is_emergency": case.is_emergency,
            "created_at": case.created_at.isoformat() if case.created_at else None,
            "user_id": case.user_id,
            "username": username
        })

    return {"total": total, "cases": items}


@router.get("/case/{session_id}", response_model=CaseDetail)
async def get_case(session_id: str, db: Session = Depends(get_db)):
    """Get detailed triage case by session ID."""
    case = db.query(TriageCase).filter(TriageCase.session_id == session_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    username = None
    if case.user_id:
        user = db.query(User).filter(User.id == case.user_id).first()
        username = user.username if user else None

    return CaseDetail(
        id=case.id,
        session_id=case.session_id,
        symptoms_raw=case.symptoms_raw,
        symptoms_extracted=case.symptoms_extracted,
        duration=case.duration,
        intensity=case.intensity,
        medical_history=case.medical_history,
        chat_history=case.chat_history,
        urgency_level=case.urgency_level,
        severity_score=case.severity_score,
        recommended_action=case.recommended_action,
        triggered_rules=case.triggered_rules,
        reasoning=case.reasoning,
        affected_regions=case.affected_regions,
        condition_images=case.condition_images,
        is_emergency=case.is_emergency,
        language=case.language,
        created_at=case.created_at,
        user_id=case.user_id,
        username=username
    )
