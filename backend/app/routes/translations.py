"""
TriageX Translation Routes
Serve translation files for multi-language support.
"""
import json
import os
from fastapi import APIRouter, HTTPException

from app.config import settings

router = APIRouter(prefix="/api/i18n", tags=["Translations"])


@router.get("/{language}")
async def get_translations(language: str):
    """Get translation file for specified language."""
    filepath = os.path.join(settings.DATA_DIR, "translations", f"{language}.json")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"Language '{language}' not supported")

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/")
async def list_languages():
    """List available languages."""
    translations_dir = os.path.join(settings.DATA_DIR, "translations")
    languages = []
    for f in os.listdir(translations_dir):
        if f.endswith(".json"):
            lang_code = f.replace(".json", "")
            languages.append({
                "code": lang_code,
                "name": {"en": "English", "ta": "Tamil"}.get(lang_code, lang_code)
            })
    return {"languages": languages}
