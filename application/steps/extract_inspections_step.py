# application/steps/extract_inspections_step.py
from __future__ import annotations
from typing import Dict, Any, List
from core.pipeline.step import Step
from infrastructure.http.safetyculture_client import SafetyCultureClient
from domain.models.inspection import Inspection


class ExtractInspectionsStep(Step):
    def __init__(self, client: SafetyCultureClient) -> None:
        self.client = client

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        payload = self.client.search_inspections(
            fields=("audit_id", "modified_at", "template_id"),
            modified_after=context.get("modified_after"),
            modified_before=context.get("modified_before"),
            include_archived=bool(context.get("include_archived", False)),
            templates=context.get("templates") or [],
        )
        audits: List[Inspection] = [Inspection.from_api(a) for a in payload.get("audits", [])]
        context["inspections"] = audits
        context["count"] = payload.get("count")
        context["total"] = payload.get("total")
        return context
