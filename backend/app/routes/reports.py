"""
TriageX Report Routes
PDF report generation and download endpoints.
"""
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.triage_case import TriageCase
from app.services.report_generator import report_generator
from app.config import settings

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/{session_id}/pdf")
async def download_report(session_id: str, db: Session = Depends(get_db)):
    """Generate and download PDF report for a triage case."""
    case = db.query(TriageCase).filter(TriageCase.session_id == session_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Triage case not found")

    # Prepare data for report
    triage_data = {
        "session_id": case.session_id,
        "symptoms_extracted": case.symptoms_extracted or [],
        "duration": case.duration,
        "intensity": case.intensity,
        "medical_history": case.medical_history,
        "severity_score": case.severity_score,
        "urgency_level": case.urgency_level,
        "recommended_action": case.recommended_action,
        "is_emergency": bool(case.is_emergency),
        "triggered_rules": case.triggered_rules or [],
        "reasoning": case.reasoning,
        "affected_regions": case.affected_regions or [],
        "condition_images": case.condition_images or [],
        "language": case.language,
        "patient_summary": ""
    }

    # Generate patient summary for the report
    from app.services.explanation_engine import explanation_engine
    triage_data["patient_summary"] = explanation_engine.generate_patient_summary(
        symptoms=triage_data["symptoms_extracted"],
        severity_score=triage_data["severity_score"] or 0,
        urgency_level=triage_data["urgency_level"] or "LOW",
        recommended_action=triage_data["recommended_action"] or "self-care",
        language=triage_data["language"]
    )

    # Generate PDF
    try:
        filepath = report_generator.generate_report(triage_data, session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

    if not os.path.exists(filepath):
        raise HTTPException(status_code=500, detail="Report file not created")

    return FileResponse(
        filepath,
        media_type="application/pdf",
        filename=f"triagex_report_{session_id}.pdf",
        headers={"Content-Disposition": f"attachment; filename=triagex_report_{session_id}.pdf"}
    )


@router.get("/{session_id}/data")
async def get_report_data(session_id: str, db: Session = Depends(get_db)):
    """Get report data as JSON (for frontend report preview)."""
    case = db.query(TriageCase).filter(TriageCase.session_id == session_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Triage case not found")

    from app.services.explanation_engine import explanation_engine
    from app.services.nlp_module import nlp_module

    symptoms = case.symptoms_extracted or []
    categories = nlp_module.get_category_names(symptoms)

    patient_summary = explanation_engine.generate_patient_summary(
        symptoms=symptoms,
        severity_score=case.severity_score or 0,
        urgency_level=case.urgency_level or "LOW",
        recommended_action=case.recommended_action or "self-care",
        language=case.language
    )

    clinical_summary = explanation_engine.generate_clinical_summary(
        symptoms=symptoms,
        categories=categories,
        severity_score=case.severity_score or 0,
        urgency_level=case.urgency_level or "LOW",
        recommended_action=case.recommended_action or "self-care",
        triggered_rules=case.triggered_rules or [],
        duration=case.duration,
        intensity=case.intensity,
        medical_history=case.medical_history
    )

    return {
        "session_id": case.session_id,
        "symptoms_raw": case.symptoms_raw,
        "symptoms_extracted": symptoms,
        "symptom_categories": categories,
        "duration": case.duration,
        "intensity": case.intensity,
        "medical_history": case.medical_history,
        "severity_score": case.severity_score,
        "urgency_level": case.urgency_level,
        "recommended_action": case.recommended_action,
        "is_emergency": bool(case.is_emergency),
        "triggered_rules": case.triggered_rules or [],
        "reasoning": case.reasoning,
        "affected_regions": case.affected_regions or [],
        "condition_images": case.condition_images or [],
        "patient_summary": patient_summary,
        "clinical_summary": clinical_summary,
        "language": case.language,
        "created_at": case.created_at.isoformat() if case.created_at else None
    }
