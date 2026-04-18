"""
TriageX PDF Report Generator
Generates structured clinical PDF reports using ReportLab.
"""
import os
from datetime import datetime, timezone
from typing import Dict, Any, List

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from app.config import settings


class ReportGenerator:

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        """Configure custom styles for the report."""
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor("#2563EB"),
            spaceAfter=6,
            alignment=TA_CENTER
        ))
        self.styles.add(ParagraphStyle(
            name='ReportSubtitle',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor("#64748B"),
            spaceAfter=20,
            alignment=TA_CENTER
        ))
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor("#0F172A"),
            spaceBefore=16,
            spaceAfter=8
        ))
        self.styles.add(ParagraphStyle(
            name='ReportBody',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor("#334155"),
            spaceAfter=4
        ))
        self.styles.add(ParagraphStyle(
            name='ReportDisclaimer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor("#94A3B8"),
            alignment=TA_CENTER,
            spaceBefore=20
        ))

    def generate_report(self, triage_data: Dict[str, Any], session_id: str) -> str:
        """
        Generate a PDF report and return the file path.
        """
        filename = f"triagex_report_{session_id}.pdf"
        filepath = os.path.join(settings.REPORTS_DIR, filename)
        os.makedirs(settings.REPORTS_DIR, exist_ok=True)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=25 * mm,
            leftMargin=25 * mm,
            topMargin=25 * mm,
            bottomMargin=25 * mm
        )

        story = []

        # ---- HEADER ----
        story.append(Paragraph("TriageX Report", self.styles['ReportTitle']))
        story.append(Paragraph("AI-Powered Medical Triage Assessment", self.styles['ReportSubtitle']))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2563EB")))
        story.append(Spacer(1, 12))

        # ---- META INFO ----
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        meta_data = [
            ["Report ID:", session_id],
            ["Generated:", now],
            ["Language:", triage_data.get("language", "en").upper()],
        ]
        meta_table = Table(meta_data, colWidths=[120, 350])
        meta_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor("#64748B")),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor("#0F172A")),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 16))

        # ---- SEVERITY SUMMARY ----
        story.append(Paragraph("Triage Assessment", self.styles['SectionHeader']))

        severity_score = triage_data.get("severity_score", 0)
        urgency_level = triage_data.get("urgency_level", "LOW")
        recommended_action = triage_data.get("recommended_action", "self-care")

        severity_color = {
            "LOW": colors.HexColor("#22C55E"),
            "MEDIUM": colors.HexColor("#EAB308"),
            "HIGH": colors.HexColor("#EF4444")
        }.get(urgency_level, colors.grey)

        assessment_data = [
            ["Severity Score:", f"{severity_score}/100"],
            ["Urgency Level:", urgency_level],
            ["Recommendation:", self._action_label(recommended_action)],
        ]

        if triage_data.get("is_emergency"):
            assessment_data.append(["EMERGENCY:", "IMMEDIATE MEDICAL ATTENTION REQUIRED"])

        assess_table = Table(assessment_data, colWidths=[140, 330])
        assess_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (1, 0), (1, 0), severity_color),
            ('TEXTCOLOR', (1, 1), (1, 1), severity_color),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(assess_table)
        story.append(Spacer(1, 16))

        # ---- SYMPTOMS ----
        story.append(Paragraph("Symptoms Detected", self.styles['SectionHeader']))
        symptoms = triage_data.get("symptoms_extracted", [])
        for s in symptoms:
            story.append(Paragraph(f"  {s.title()}", self.styles['ReportBody']))
        story.append(Spacer(1, 8))

        # Duration & Intensity
        if triage_data.get("duration"):
            story.append(Paragraph(f"<b>Duration:</b> {triage_data['duration']}", self.styles['ReportBody']))
        if triage_data.get("intensity"):
            story.append(Paragraph(f"<b>Intensity:</b> {triage_data['intensity']}/10", self.styles['ReportBody']))
        if triage_data.get("medical_history"):
            story.append(Paragraph(f"<b>Medical History:</b> {triage_data['medical_history']}", self.styles['ReportBody']))
        story.append(Spacer(1, 12))

        # ---- AI REASONING ----
        story.append(Paragraph("AI Reasoning", self.styles['SectionHeader']))
        triggered_rules = triage_data.get("triggered_rules", [])
        if triggered_rules:
            for rule in triggered_rules:
                rule_text = f"<b>[{rule.get('rule_id', 'R')}] {rule.get('rule_name', '')}:</b> {rule.get('description', '')}"
                story.append(Paragraph(rule_text, self.styles['ReportBody']))
                matched = ", ".join(rule.get("matched_symptoms", []))
                story.append(Paragraph(f"  Matched: {matched} (Score: {rule.get('severity_contribution', 0)}/100)", self.styles['ReportBody']))
        else:
            story.append(Paragraph("No specific clinical rules were triggered. Assessment based on general symptom analysis.", self.styles['ReportBody']))
        story.append(Spacer(1, 12))

        # ---- AFFECTED BODY REGIONS ----
        regions = triage_data.get("affected_regions", [])
        if regions:
            story.append(Paragraph("Affected Body Regions", self.styles['SectionHeader']))
            for region in regions:
                r_name = region.get("display_name", region.get("region", ""))
                r_severity = region.get("severity", "")
                r_symptoms = ", ".join(region.get("symptoms", []))
                story.append(Paragraph(f"<b>{r_name}</b> ({r_severity}): {r_symptoms}", self.styles['ReportBody']))
            story.append(Spacer(1, 12))

        # ---- PATIENT SUMMARY ----
        patient_summary = triage_data.get("patient_summary", "")
        if patient_summary:
            story.append(Paragraph("Patient-Friendly Summary", self.styles['SectionHeader']))
            for line in patient_summary.split("\n"):
                if line.strip():
                    # Strip emoji characters for PDF compatibility
                    clean_line = line.encode('ascii', 'ignore').decode('ascii').strip()
                    if clean_line:
                        story.append(Paragraph(clean_line, self.styles['ReportBody']))
            story.append(Spacer(1, 12))

        # ---- DISCLAIMER ----
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1")))
        story.append(Paragraph(
            "DISCLAIMER: TriageX is an AI-assisted pre-triage tool and is NOT a substitute for professional medical diagnosis. "
            "Always consult a qualified healthcare provider. This report is auto-generated and should be reviewed by clinical staff.",
            self.styles['ReportDisclaimer']
        ))

        # Build PDF
        doc.build(story)
        return filepath

    def _action_label(self, action: str) -> str:
        labels = {
            "self-care": "Self-Care at Home",
            "consult-doctor": "Consult a Doctor",
            "emergency": "Seek Emergency Care Immediately"
        }
        return labels.get(action, action)


# Singleton instance
report_generator = ReportGenerator()
