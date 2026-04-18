"""
TriageX Explanation Engine
Generates human-readable explanations for triage results (Explainable AI).
"""
from typing import List, Dict, Any


class ExplanationEngine:

    def generate_reasoning(self, triggered_rules: List[Dict], symptoms: List[str],
                           severity_score: float, urgency_level: str,
                           recommended_action: str, intensity: int = 5) -> str:
        """
        Generate a clear, detailed reasoning string explaining why
        a particular triage result was produced.
        """
        lines = []
        lines.append("=== TriageX AI Reasoning ===\n")

        # Summarize what was analyzed
        lines.append(f"Analyzed {len(symptoms)} symptom(s): {', '.join(symptoms)}")
        lines.append(f"Reported intensity: {intensity}/10\n")

        if triggered_rules:
            lines.append(f"{len(triggered_rules)} clinical rule(s) were triggered:\n")
            for i, rule in enumerate(triggered_rules, 1):
                lines.append(f"  Rule {i}: {rule['rule_name']}")
                lines.append(f"    → {rule['description']}")
                lines.append(f"    → Matched symptoms: {', '.join(rule['matched_symptoms'])}")
                lines.append(f"    → Severity contribution: {rule['severity_contribution']}/100\n")
        else:
            lines.append("No specific clinical rules were triggered.")
            lines.append("Assessment is based on general symptom severity and intensity.\n")

        lines.append(f"Final Severity Score: {severity_score}/100")
        lines.append(f"Urgency Level: {urgency_level}")
        lines.append(f"Recommended Action: {self._action_label(recommended_action)}")

        return "\n".join(lines)

    def generate_key_factors(self, triggered_rules: List[Dict], symptoms: List[str],
                              severity_score: float, intensity: int = 5) -> List[str]:
        """Generate a list of key factors that influenced the result."""
        factors = []

        if triggered_rules:
            # Most critical rule
            top_rule = max(triggered_rules, key=lambda r: r["severity_contribution"])
            factors.append(f"Primary concern: {top_rule['rule_name']} (severity: {top_rule['severity_contribution']}/100)")

            # Count high-severity rules
            high_rules = [r for r in triggered_rules if r["severity_contribution"] >= 60]
            if len(high_rules) > 1:
                factors.append(f"Multiple high-severity patterns detected ({len(high_rules)} rules)")

        if intensity >= 8:
            factors.append(f"High symptom intensity reported ({intensity}/10)")
        elif intensity >= 5:
            factors.append(f"Moderate symptom intensity ({intensity}/10)")
        else:
            factors.append(f"Mild symptom intensity ({intensity}/10)")

        if len(symptoms) >= 4:
            factors.append(f"Multiple symptoms present ({len(symptoms)} symptoms)")

        if severity_score >= 70:
            factors.append("Severity score exceeds critical threshold")
        elif severity_score >= 40:
            factors.append("Severity score indicates moderate concern")

        return factors

    def generate_clinical_summary(self, symptoms: List[str], categories: List[str],
                                   severity_score: float, urgency_level: str,
                                   recommended_action: str, triggered_rules: List[Dict],
                                   duration: str = None, intensity: int = 5,
                                   medical_history: str = None) -> str:
        """Generate a structured clinical summary for healthcare providers."""
        lines = []
        lines.append("CLINICAL TRIAGE SUMMARY")
        lines.append("=" * 40)
        lines.append("")

        lines.append("PRESENTING SYMPTOMS:")
        for s in symptoms:
            lines.append(f"  • {s.title()}")
        lines.append("")

        if categories:
            lines.append(f"AFFECTED SYSTEMS: {', '.join(categories)}")
            lines.append("")

        if duration:
            lines.append(f"DURATION: {duration}")
        lines.append(f"REPORTED INTENSITY: {intensity}/10")
        lines.append("")

        if medical_history and medical_history.lower() not in ["none", "no", "n/a", ""]:
            lines.append(f"MEDICAL HISTORY: {medical_history}")
            lines.append("")

        lines.append(f"TRIAGE ASSESSMENT:")
        lines.append(f"  Severity Score: {severity_score}/100")
        lines.append(f"  Urgency Level: {urgency_level}")
        lines.append(f"  Recommendation: {self._action_label(recommended_action)}")
        lines.append("")

        if triggered_rules:
            lines.append("TRIGGERED RULES:")
            for rule in triggered_rules:
                lines.append(f"  [{rule['rule_id']}] {rule['rule_name']}: {rule['description']}")
            lines.append("")

        lines.append("NOTE: This is an AI-assisted pre-triage assessment.")
        lines.append("Clinical correlation and professional medical evaluation are required.")

        return "\n".join(lines)

    def generate_patient_summary(self, symptoms: List[str], severity_score: float,
                                  urgency_level: str, recommended_action: str,
                                  language: str = "en") -> str:
        """Generate a patient-friendly summary in simple language."""
        if language == "ta":
            return self._patient_summary_tamil(symptoms, severity_score, urgency_level, recommended_action)

        lines = []

        if urgency_level == "HIGH":
            lines.append("⚠️ Your symptoms suggest a SERIOUS concern that needs prompt medical attention.")
        elif urgency_level == "MEDIUM":
            lines.append("Your symptoms suggest a MODERATE concern. We recommend consulting a doctor.")
        else:
            lines.append("Your symptoms appear to be MILD. Self-care at home should help.")

        lines.append("")
        lines.append(f"We detected the following symptoms: {', '.join(symptoms)}.")
        lines.append(f"Your severity score is {severity_score} out of 100.")
        lines.append("")

        if recommended_action == "emergency":
            lines.append("🚨 RECOMMENDATION: Please seek emergency medical care immediately.")
            lines.append("If symptoms worsen, call emergency services (112/108).")
        elif recommended_action == "consult-doctor":
            lines.append("📋 RECOMMENDATION: Please schedule an appointment with your doctor.")
            lines.append("If symptoms worsen significantly, consider visiting an urgent care facility.")
        else:
            lines.append("🏠 RECOMMENDATION: Rest, stay hydrated, and monitor your symptoms.")
            lines.append("If symptoms persist for more than a few days or worsen, consult a doctor.")

        lines.append("")
        lines.append("⚕️ Remember: This is NOT a medical diagnosis. Always consult a healthcare professional.")

        return "\n".join(lines)

    def _patient_summary_tamil(self, symptoms, severity_score, urgency_level, recommended_action):
        """Tamil version of patient summary."""
        lines = []

        if urgency_level == "HIGH":
            lines.append("⚠️ உங்கள் அறிகுறிகள் உடனடி மருத்துவ கவனிப்பு தேவைப்படும் தீவிரமான கவலையை குறிக்கின்றன.")
        elif urgency_level == "MEDIUM":
            lines.append("உங்கள் அறிகுறிகள் நடுத்தரமான கவலையை குறிக்கின்றன. மருத்துவரை அணுகுவதை பரிந்துரைக்கிறோம்.")
        else:
            lines.append("உங்கள் அறிகுறிகள் லேசானவை. வீட்டில் சுய பராமரிப்பு உதவும்.")

        lines.append("")
        lines.append(f"கண்டறியப்பட்ட அறிகுறிகள்: {', '.join(symptoms)}.")
        lines.append(f"தீவிரத்தன்மை மதிப்பெண்: 100-ல் {severity_score}.")
        lines.append("")

        if recommended_action == "emergency":
            lines.append("🚨 பரிந்துரை: உடனடியாக அவசர மருத்துவ சிகிச்சையை நாடுங்கள்.")
        elif recommended_action == "consult-doctor":
            lines.append("📋 பரிந்துரை: உங்கள் மருத்துவரிடம் சந்திப்பை ஏற்படுத்துங்கள்.")
        else:
            lines.append("🏠 பரிந்துரை: ஓய்வு எடுங்கள், நீரேற்றமாக இருங்கள், அறிகுறிகளை கவனியுங்கள்.")

        lines.append("")
        lines.append("⚕️ நினைவில் கொள்ளுங்கள்: இது மருத்துவ நோயறிதல் அல்ல.")

        return "\n".join(lines)

    def _action_label(self, action: str) -> str:
        labels = {
            "self-care": "Self-Care at Home",
            "consult-doctor": "Consult a Doctor",
            "emergency": "Seek Emergency Care"
        }
        return labels.get(action, action)


# Singleton instance
explanation_engine = ExplanationEngine()
