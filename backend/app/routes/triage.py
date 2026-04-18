"""
TriageX Triage Routes
Core API endpoints for symptom analysis and conversational triage.
"""
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.triage_case import TriageCase
from app.models.schemas import (
    SymptomInput, TriageResult, ChatRequest, ChatResponse,
    ChatMessage, AffectedRegion, TriggeredRule
)
from app.services.nlp_module import nlp_module
from app.services.triage_engine import triage_engine
from app.services.explanation_engine import explanation_engine
from app.services.visual_mapper import visual_mapper
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/triage", tags=["Triage"])


# ============ CHAT CONVERSATION STATE (in-memory for simplicity) ============
chat_sessions = {}


CHAT_STEPS = ["symptoms", "duration", "intensity", "history", "complete"]

CHAT_PROMPTS = {
    "en": {
        "welcome": "Hello! I'm your TriageX assistant. I'll help assess your symptoms.\n\nPlease describe your symptoms in detail. For example: 'I have a headache, sore throat, and mild fever.'",
        "ask_duration": "How long have you been experiencing these symptoms? (e.g., '2 days', 'a few hours', '1 week')",
        "ask_intensity": "On a scale of 1-10, how intense are your symptoms?\n(1 = very mild, 10 = extremely severe)",
        "ask_history": "Do you have any relevant medical history? (e.g., chronic conditions, allergies, current medications)\n\nType 'none' or 'no' to skip.",
        "processing": "Thank you! Analyzing your symptoms now...",
        "invalid_intensity": "Please enter a number between 1 and 10.",
    },
    "ta": {
        "welcome": "வணக்கம்! நான் உங்கள் TriageX உதவியாளர்.\n\nஉங்கள் அறிகுறிகளை விவரமாக விவரிக்கவும்.",
        "ask_duration": "இந்த அறிகுறிகளை எவ்வளவு காலமாக அனுபவிக்கிறீர்கள்?",
        "ask_intensity": "1-10 அளவில், உங்கள் அறிகுறிகள் எவ்வளவு தீவிரமானவை?",
        "ask_history": "ஏதேனும் மருத்துவ வரலாறு உள்ளதா? இல்லையென்றால் 'இல்லை' என தட்டச்சு செய்யவும்.",
        "processing": "நன்றி! உங்கள் அறிகுறிகளை பகுப்பாய்வு செய்கிறது...",
        "invalid_intensity": "1 முதல் 10 வரை ஒரு எண்ணை உள்ளிடவும்.",
    }
}


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Conversational symptom intake.
    Guides user through steps: symptoms → duration → intensity → history → analysis.
    """
    session_id = request.session_id or str(uuid.uuid4())
    lang = request.language if request.language in CHAT_PROMPTS else "en"
    prompts = CHAT_PROMPTS[lang]

    # Initialize session if new
    if session_id not in chat_sessions:
        chat_sessions[session_id] = {
            "step": "symptoms",
            "data": {},
            "history": []
        }
        # Send welcome message
        welcome_msg = ChatMessage(role="assistant", content=prompts["welcome"],
                                   timestamp=datetime.now(timezone.utc).isoformat())
        chat_sessions[session_id]["history"].append(welcome_msg.model_dump())

        return ChatResponse(
            reply=prompts["welcome"],
            session_id=session_id,
            chat_history=[welcome_msg],
            is_complete=False
        )

    session = chat_sessions[session_id]
    step = session["step"]

    # Add user message to history
    user_msg = ChatMessage(role="user", content=request.message,
                            timestamp=datetime.now(timezone.utc).isoformat())
    session["history"].append(user_msg.model_dump())

    reply = ""
    is_complete = False
    collected_data = None

    if step == "symptoms":
        session["data"]["symptoms"] = request.message
        session["step"] = "duration"
        reply = prompts["ask_duration"]

    elif step == "duration":
        session["data"]["duration"] = request.message
        session["step"] = "intensity"
        reply = prompts["ask_intensity"]

    elif step == "intensity":
        # Try to parse intensity
        try:
            intensity = int(request.message.strip())
            if 1 <= intensity <= 10:
                session["data"]["intensity"] = intensity
                session["step"] = "history"
                reply = prompts["ask_history"]
            else:
                reply = prompts["invalid_intensity"]
        except ValueError:
            reply = prompts["invalid_intensity"]

    elif step == "history":
        session["data"]["history"] = request.message
        session["step"] = "complete"

        # Process the triage
        data = session["data"]
        result = _process_triage(
            symptoms_text=data["symptoms"],
            duration=data.get("duration"),
            intensity=data.get("intensity", 5),
            medical_history=data.get("history"),
            language=lang,
            session_id=session_id,
            chat_history=session["history"],
            db=db
        )

        reply = prompts["processing"] + "\n\n" + result["patient_summary"]
        is_complete = True
        collected_data = {
            "session_id": session_id,
            "severity_score": result["severity_score"],
            "urgency_level": result["urgency_level"],
            "recommended_action": result["recommended_action"]
        }

    # Add assistant reply to history
    assistant_msg = ChatMessage(role="assistant", content=reply,
                                 timestamp=datetime.now(timezone.utc).isoformat())
    session["history"].append(assistant_msg.model_dump())

    history = [ChatMessage(**m) for m in session["history"]]

    return ChatResponse(
        reply=reply,
        session_id=session_id,
        chat_history=history,
        is_complete=is_complete,
        collected_data=collected_data
    )


@router.post("/analyze", response_model=TriageResult)
async def analyze(input_data: SymptomInput, db: Session = Depends(get_db)):
    """
    Direct symptom analysis (non-conversational).
    Accepts symptoms text and returns full triage result.
    """
    session_id = str(uuid.uuid4())
    result = _process_triage(
        symptoms_text=input_data.symptoms,
        duration=input_data.duration,
        intensity=input_data.intensity or 5,
        medical_history=input_data.medical_history,
        language=input_data.language,
        session_id=session_id,
        db=db
    )
    return result


@router.get("/result/{session_id}", response_model=TriageResult)
async def get_result(session_id: str, db: Session = Depends(get_db)):
    """Get triage result by session ID."""
    case = db.query(TriageCase).filter(TriageCase.session_id == session_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Triage case not found")

    return TriageResult(
        session_id=case.session_id,
        urgency_level=case.urgency_level or "LOW",
        severity_score=case.severity_score or 0,
        recommended_action=case.recommended_action or "self-care",
        is_emergency=bool(case.is_emergency),
        symptoms_extracted=case.symptoms_extracted or [],
        symptom_categories=[],
        triggered_rules=[TriggeredRule(**r) for r in (case.triggered_rules or [])],
        reasoning=case.reasoning or "",
        key_factors=[],
        affected_regions=[AffectedRegion(**r) for r in (case.affected_regions or [])],
        condition_images=case.condition_images or [],
        clinical_summary="",
        patient_summary="",
        language=case.language,
        timestamp=case.created_at.isoformat() if case.created_at else None
    )


def _process_triage(symptoms_text: str, duration: str = None, intensity: int = 5,
                     medical_history: str = None, language: str = "en",
                     session_id: str = None, chat_history: list = None,
                     db: Session = None) -> dict:
    """
    Core triage processing pipeline.
    1. NLP extraction
    2. Rule-based scoring
    3. Explanation generation
    4. Visual mapping
    5. Database save
    """
    # Step 1: Extract symptoms
    symptoms = nlp_module.extract_symptoms(symptoms_text)
    categories = nlp_module.get_category_names(symptoms)

    # Step 2: Triage evaluation
    triage_result = triage_engine.evaluate(symptoms, intensity)

    # Step 3: Generate explanations
    reasoning = explanation_engine.generate_reasoning(
        triggered_rules=triage_result["triggered_rules"],
        symptoms=symptoms,
        severity_score=triage_result["severity_score"],
        urgency_level=triage_result["urgency_level"],
        recommended_action=triage_result["recommended_action"],
        intensity=intensity
    )

    key_factors = explanation_engine.generate_key_factors(
        triggered_rules=triage_result["triggered_rules"],
        symptoms=symptoms,
        severity_score=triage_result["severity_score"],
        intensity=intensity
    )

    clinical_summary = explanation_engine.generate_clinical_summary(
        symptoms=symptoms, categories=categories,
        severity_score=triage_result["severity_score"],
        urgency_level=triage_result["urgency_level"],
        recommended_action=triage_result["recommended_action"],
        triggered_rules=triage_result["triggered_rules"],
        duration=duration, intensity=intensity,
        medical_history=medical_history
    )

    patient_summary = explanation_engine.generate_patient_summary(
        symptoms=symptoms,
        severity_score=triage_result["severity_score"],
        urgency_level=triage_result["urgency_level"],
        recommended_action=triage_result["recommended_action"],
        language=language
    )

    # Step 4: Visual mapping
    affected_regions = visual_mapper.get_affected_regions(
        symptoms, triage_result["urgency_level"]
    )
    condition_images = visual_mapper.get_condition_images(symptoms)

    # Step 5: Save to database
    if db:
        case = TriageCase(
            session_id=session_id,
            symptoms_raw=symptoms_text,
            symptoms_extracted=symptoms,
            duration=duration,
            intensity=intensity,
            medical_history=medical_history,
            chat_history=chat_history,
            urgency_level=triage_result["urgency_level"],
            severity_score=triage_result["severity_score"],
            recommended_action=triage_result["recommended_action"],
            triggered_rules=triage_result["triggered_rules"],
            reasoning=reasoning,
            affected_regions=[r for r in affected_regions],
            condition_images=condition_images,
            language=language,
            is_emergency=1 if triage_result["is_emergency"] else 0
        )
        db.add(case)
        db.commit()

    # Build response
    triggered_rule_models = [
        TriggeredRule(**r) for r in triage_result["triggered_rules"]
    ]
    affected_region_models = [
        AffectedRegion(
            region=r["region"],
            severity=r["severity"],
            color=r["color"],
            symptoms=r["symptoms"]
        ) for r in affected_regions
    ]

    return {
        "session_id": session_id,
        "urgency_level": triage_result["urgency_level"],
        "severity_score": triage_result["severity_score"],
        "recommended_action": triage_result["recommended_action"],
        "is_emergency": triage_result["is_emergency"],
        "symptoms_extracted": symptoms,
        "symptom_categories": categories,
        "triggered_rules": triggered_rule_models,
        "reasoning": reasoning,
        "key_factors": key_factors,
        "affected_regions": affected_region_models,
        "condition_images": condition_images,
        "clinical_summary": clinical_summary,
        "patient_summary": patient_summary,
        "language": language,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
