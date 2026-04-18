"""
Unit tests for TriageX Triage Engine
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.nlp_module import NLPModule
from app.services.triage_engine import TriageEngine
from app.services.explanation_engine import ExplanationEngine
from app.services.visual_mapper import VisualMapper


def test_nlp_extraction():
    nlp = NLPModule()

    # Test basic symptom extraction
    symptoms = nlp.extract_symptoms("I have a headache and fever")
    assert "headache" in symptoms, f"Expected 'headache' in {symptoms}"
    assert "fever" in symptoms, f"Expected 'fever' in {symptoms}"
    print("\u2705 NLP: Basic extraction passed")

    # Test synonym resolution
    symptoms = nlp.extract_symptoms("my tummy ache and I'm throwing up")
    assert "stomach pain" in symptoms or "abdominal pain" in symptoms, f"Synonym resolution failed: {symptoms}"
    assert "vomiting" in symptoms, f"Expected 'vomiting' in {symptoms}"
    print("\u2705 NLP: Synonym resolution passed")

    # Test categorization
    symptoms = nlp.extract_symptoms("chest pain and difficulty breathing")
    categories = nlp.get_category_names(symptoms)
    assert len(categories) > 0, "Expected at least one category"
    print(f"\u2705 NLP: Categorization passed -> {categories}")

    # Test body region mapping
    regions = nlp.get_body_regions(symptoms)
    assert "chest" in regions, f"Expected 'chest' in {regions}"
    print(f"\u2705 NLP: Body region mapping passed -> {regions}")


def test_triage_engine():
    engine = TriageEngine()

    # Test HIGH severity: chest pain + breathing difficulty
    result = engine.evaluate(["chest pain", "difficulty breathing"], intensity=8)
    assert result["urgency_level"] == "HIGH", f"Expected HIGH, got {result['urgency_level']}"
    assert result["severity_score"] >= 60, f"Score too low: {result['severity_score']}"
    assert result["recommended_action"] == "emergency"
    print(f"\u2705 Triage: High severity passed -> Score: {result['severity_score']}, Emergency: {result['is_emergency']}")

    # Test MEDIUM severity: fever
    result = engine.evaluate(["fever"], intensity=5)
    assert result["urgency_level"] == "MEDIUM", f"Expected MEDIUM, got {result['urgency_level']}"
    print(f"\u2705 Triage: Medium severity passed -> Score: {result['severity_score']}")

    # Test LOW severity: common cold symptoms
    result = engine.evaluate(["runny nose", "sneezing"], intensity=2)
    assert result["urgency_level"] == "LOW", f"Expected LOW, got {result['urgency_level']}"
    assert result["recommended_action"] == "self-care"
    print(f"\u2705 Triage: Low severity passed \u2192 Score: {result['severity_score']}")

    # Test intensity multiplier
    low_intensity = engine.evaluate(["chest pain"], intensity=2)
    high_intensity = engine.evaluate(["chest pain"], intensity=9)
    assert high_intensity["severity_score"] > low_intensity["severity_score"], \
        "Higher intensity should produce higher score"
    print(f"\u2705 Triage: Intensity multiplier passed -> Low: {low_intensity['severity_score']}, High: {high_intensity['severity_score']}")

    # Test emergency detection
    result = engine.evaluate(["chest pain", "difficulty breathing", "fever"], intensity=9)
    assert result["is_emergency"] == True, "Expected emergency"
    print("\u2705 Triage: Emergency detection passed")


def test_explanation_engine():
    engine = ExplanationEngine()

    rules = [
        {
            "rule_id": "R001",
            "rule_name": "Chest Pain + Breathing Difficulty",
            "description": "Critical cardiac/pulmonary concern",
            "severity_contribution": 85,
            "matched_symptoms": ["chest pain", "difficulty breathing"]
        }
    ]

    # Test reasoning generation
    reasoning = engine.generate_reasoning(rules, ["chest pain", "difficulty breathing"], 85, "HIGH", "emergency", 8)
    assert "TriageX AI Reasoning" in reasoning
    assert "Chest Pain" in reasoning
    print("[PASS] Explanation: Reasoning generation passed")

    # Test key factors
    factors = engine.generate_key_factors(rules, ["chest pain", "difficulty breathing"], 85, 8)
    assert len(factors) > 0
    print(f"[PASS] Explanation: Key factors passed -> {factors}")

    # Test clinical summary
    summary = engine.generate_clinical_summary(
        ["chest pain"], ["Cardiac"], 85, "HIGH", "emergency", rules
    )
    assert "CLINICAL TRIAGE SUMMARY" in summary
    print("[PASS] Explanation: Clinical summary passed")

    # Test patient summary
    patient = engine.generate_patient_summary(["chest pain"], 85, "HIGH", "emergency")
    assert "SERIOUS" in patient or "emergency" in patient.lower()
    print("[PASS] Explanation: Patient summary passed")


def test_visual_mapper():
    mapper = VisualMapper()

    # Test region mapping
    regions = mapper.get_affected_regions(["chest pain", "headache"], "HIGH")
    region_names = [r["region"] for r in regions]
    assert "chest" in region_names, f"Expected 'chest' in {region_names}"
    assert "head" in region_names, f"Expected 'head' in {region_names}"
    print(f"[PASS] Visual: Region mapping passed -> {region_names}")

    # Test color coding
    for region in regions:
        assert region["color"] in ["#22C55E", "#EAB308", "#EF4444"], f"Invalid color: {region['color']}"
    print("[PASS] Visual: Color coding passed")

    # Test condition images
    images = mapper.get_condition_images(["headache", "chest pain"])
    assert len(images) > 0, "Expected at least one condition image"
    print(f"[PASS] Visual: Condition images passed -> {len(images)} images")


if __name__ == "__main__":
    print("\nRunning TriageX Unit Tests\n" + "=" * 40)

    test_nlp_extraction()
    print()
    test_triage_engine()
    print()
    test_explanation_engine()
    print()
    test_visual_mapper()

    print("\n" + "=" * 40)
    print("All tests passed!")
