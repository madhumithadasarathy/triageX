"""
TriageX Triage Engine
Rule-based severity scoring system with intensity multipliers.
"""
import json
import os
from typing import List, Dict, Any, Tuple

from app.config import settings
from app.services.nlp_module import nlp_module


class TriageEngine:
    def __init__(self):
        self.rules = []
        self.intensity_multipliers = {}
        self.urgency_thresholds = {}
        self._load_rules()

    def _load_rules(self):
        """Load triage rules from JSON."""
        rules_path = os.path.join(settings.DATA_DIR, "symptom_rules.json")
        with open(rules_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.rules = data.get("rules", [])
            self.intensity_multipliers = data.get("intensity_multipliers", {})
            self.urgency_thresholds = data.get("urgency_thresholds", {})

    def evaluate(self, symptoms: List[str], intensity: int = 5) -> Dict[str, Any]:
        """
        Evaluate symptoms against all rules and compute severity.
        
        Args:
            symptoms: List of extracted symptom keywords
            intensity: Pain/symptom intensity (1-10)
            
        Returns:
            Dict with severity_score, urgency_level, recommended_action,
            triggered_rules, and is_emergency.
        """
        triggered_rules = []
        max_score = 0
        is_emergency = False
        highest_action = "self-care"

        action_priority = {"self-care": 0, "consult-doctor": 1, "emergency": 2}

        for rule in self.rules:
            matched = self._check_rule(rule, symptoms)
            if matched:
                matched_symptoms = matched
                triggered_rules.append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "description": rule["description"],
                    "severity_contribution": rule["score_contribution"],
                    "matched_symptoms": matched_symptoms
                })

                if rule["score_contribution"] > max_score:
                    max_score = rule["score_contribution"]

                if rule.get("emergency", False):
                    is_emergency = True

                if action_priority.get(rule["action"], 0) > action_priority.get(highest_action, 0):
                    highest_action = rule["action"]

        # Apply intensity multiplier
        multiplier = self.intensity_multipliers.get(str(intensity), 0.7)
        severity_score = min(100, max_score * multiplier)

        # Handle case where no rules matched but symptoms exist
        if not triggered_rules and symptoms:
            severity_score = max(10, intensity * 3)
            highest_action = "self-care" if severity_score < 30 else "consult-doctor"

        # Determine urgency level
        urgency_level = self._get_urgency_level(severity_score)

        # Override urgency if emergency
        if is_emergency:
            urgency_level = "HIGH"
            if severity_score < 61:
                severity_score = 65

        return {
            "severity_score": round(severity_score, 1),
            "urgency_level": urgency_level,
            "recommended_action": highest_action,
            "triggered_rules": triggered_rules,
            "is_emergency": is_emergency
        }

    def _check_rule(self, rule: Dict, symptoms: List[str]) -> List[str]:
        """
        Check if a rule matches the given symptoms.
        Returns list of matched symptoms if rule fires, empty list otherwise.
        """
        conditions = rule.get("conditions", {})
        symptoms_lower = [s.lower() for s in symptoms]
        matched = []

        # Check 'symptoms_any' - at least one must match
        symptoms_any = conditions.get("symptoms_any", [])
        any_matched = False
        for keyword in symptoms_any:
            if any(keyword.lower() in s or s in keyword.lower() for s in symptoms_lower):
                any_matched = True
                matched.append(keyword)

        if symptoms_any and not any_matched:
            return []

        # Check 'symptoms_and' - if present, at least one from this group must also match
        symptoms_and = conditions.get("symptoms_and", [])
        if symptoms_and:
            and_matched = False
            for keyword in symptoms_and:
                if any(keyword.lower() in s or s in keyword.lower() for s in symptoms_lower):
                    and_matched = True
                    matched.append(keyword)
            if not and_matched:
                return []

        return matched

    def _get_urgency_level(self, score: float) -> str:
        """Determine urgency level from severity score."""
        for level, (low, high) in self.urgency_thresholds.items():
            if low <= score <= high:
                return level
        if score > 60:
            return "HIGH"
        elif score > 30:
            return "MEDIUM"
        return "LOW"


# Singleton instance
triage_engine = TriageEngine()
