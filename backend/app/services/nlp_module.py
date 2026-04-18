"""
TriageX NLP Module
Extracts symptom keywords from natural language input using keyword matching
and synonym resolution. Works fully offline.
"""
import json
import os
import re
import difflib
from typing import List, Dict, Tuple

from app.config import settings


class NLPModule:
    def __init__(self):
        self.categories = {}
        self.synonyms = {}
        self._load_data()

    def _load_data(self):
        """Load symptom categories and synonyms from JSON."""
        categories_path = os.path.join(settings.DATA_DIR, "symptom_categories.json")
        with open(categories_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.categories = data.get("categories", {})
            self.synonyms = data.get("symptom_synonyms", {})

    def normalize_text(self, text: str) -> str:
        """Normalize input text: lowercase, strip, resolve synonyms."""
        text = text.lower().strip()
        # Replace synonyms
        for synonym, canonical in self.synonyms.items():
            if synonym in text:
                text = text.replace(synonym, canonical)
        return text

    def extract_symptoms(self, text: str) -> List[str]:
        """
        Extract symptom keywords from natural language text using fuzzy matching.
        """
        normalized = self.normalize_text(text)
        found_symptoms = []
        
        # Collect all keywords from all categories
        all_keywords = []
        for cat_name, cat_data in self.categories.items():
            for keyword in cat_data["keywords"]:
                all_keywords.append(keyword)

        # Sort by keyword length (longest first)
        all_keywords.sort(key=lambda x: len(x), reverse=True)

        remaining_text = normalized

        # 1. Substring matching for phrases/keywords
        for keyword in all_keywords:
            if len(keyword) > 3 and keyword in remaining_text:
                found_symptoms.append(keyword)
                remaining_text = remaining_text.replace(keyword, " " * len(keyword))

        # 2. Token-based fuzzy matching
        remaining_words = [w for w in remaining_text.split() if len(w) > 3]
        for word in remaining_words:
            matches = difflib.get_close_matches(word, all_keywords, n=1, cutoff=0.85)
            if matches:
                found_symptoms.append(matches[0])

        return list(set(found_symptoms))

    def categorize_symptoms(self, symptoms: List[str]) -> Dict[str, List[str]]:
        """
        Map extracted symptoms to their medical categories.
        Returns dict of category -> [symptoms].
        """
        categorized = {}
        for symptom in symptoms:
            for cat_name, cat_data in self.categories.items():
                if symptom in cat_data["keywords"]:
                    if cat_name not in categorized:
                        categorized[cat_name] = []
                    if symptom not in categorized[cat_name]:
                        categorized[cat_name].append(symptom)
        return categorized

    def get_category_names(self, symptoms: List[str]) -> List[str]:
        """Get list of category display names for given symptoms."""
        categorized = self.categorize_symptoms(symptoms)
        names = []
        for cat_name in categorized:
            display = self.categories[cat_name].get("display_name", cat_name)
            if display not in names:
                names.append(display)
        return names

    def get_body_regions(self, symptoms: List[str]) -> List[str]:
        """Get list of body regions affected by given symptoms."""
        regions = set()
        for symptom in symptoms:
            for cat_name, cat_data in self.categories.items():
                if symptom in cat_data["keywords"]:
                    regions.add(cat_data["body_region"])
        return list(regions)


# Singleton instance
nlp_module = NLPModule()
