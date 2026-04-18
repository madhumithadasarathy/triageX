"""
TriageX Visual Mapper
Maps symptoms to body regions and condition illustrations for visual rendering.
"""
import json
import os
from typing import List, Dict, Any

from app.config import settings


class VisualMapper:
    def __init__(self):
        self.body_regions = {}
        self.condition_images = {}
        self._load_data()

    def _load_data(self):
        """Load body region and condition image mappings."""
        map_path = os.path.join(settings.DATA_DIR, "body_region_map.json")
        with open(map_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.body_regions = data.get("body_regions", {})
            self.condition_images = data.get("condition_images", {})

    def get_affected_regions(self, symptoms: List[str], urgency_level: str = "LOW") -> List[Dict[str, Any]]:
        """
        Determine which body regions are affected by the given symptoms.
        Returns list of region objects with severity and color coding.
        """
        region_symptoms = {}

        for symptom in symptoms:
            symptom_lower = symptom.lower()
            for region_key, region_data in self.body_regions.items():
                region_symptom_list = [s.lower() for s in region_data["symptoms"]]
                if symptom_lower in region_symptom_list or any(
                    symptom_lower in rs or rs in symptom_lower for rs in region_symptom_list
                ):
                    if region_key not in region_symptoms:
                        region_symptoms[region_key] = []
                    if symptom not in region_symptoms[region_key]:
                        region_symptoms[region_key].append(symptom)

        # Build affected regions list
        affected = []
        severity_colors = {
            "LOW": "#22C55E",     # Green
            "MEDIUM": "#EAB308",  # Yellow
            "HIGH": "#EF4444"     # Red
        }

        for region_key, matched_symptoms in region_symptoms.items():
            region_data = self.body_regions[region_key]
            # Determine per-region severity based on number of symptoms and overall urgency
            if urgency_level == "HIGH" or len(matched_symptoms) >= 3:
                severity = "HIGH"
            elif urgency_level == "MEDIUM" or len(matched_symptoms) >= 2:
                severity = "MEDIUM"
            else:
                severity = "LOW"

            affected.append({
                "region": region_key,
                "display_name": region_data["display_name"],
                "svg_id": region_data["svg_id"],
                "severity": severity,
                "color": severity_colors[severity],
                "symptoms": matched_symptoms
            })

        return affected

    def get_condition_images(self, symptoms: List[str]) -> List[Dict[str, str]]:
        """
        Map symptoms to condition illustration images.
        Returns list of image objects with metadata.
        """
        images = []
        seen = set()

        for symptom in symptoms:
            symptom_lower = symptom.lower()
            # Direct match
            if symptom_lower in self.condition_images:
                img = self.condition_images[symptom_lower]
                if img["image"] not in seen:
                    images.append({
                        "symptom": symptom,
                        "image": img["image"],
                        "label": img["label"],
                        "description": img["description"]
                    })
                    seen.add(img["image"])
            else:
                # Partial match
                for key, img in self.condition_images.items():
                    if key in symptom_lower or symptom_lower in key:
                        if img["image"] not in seen:
                            images.append({
                                "symptom": symptom,
                                "image": img["image"],
                                "label": img["label"],
                                "description": img["description"]
                            })
                            seen.add(img["image"])

        return images


# Singleton instance
visual_mapper = VisualMapper()
