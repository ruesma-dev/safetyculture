# application/steps/export_csv_step.py
from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict, Any, Iterable
from core.pipeline.step import Step
from infrastructure.filesystem.csv_writer import CsvWriter
from domain.models.inspection import Inspection


class ExportCsvStep(Step):
    def __init__(self, writer: CsvWriter) -> None:
        self.writer = writer

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        inspections: Iterable[Inspection] = context.get("inspections", [])
        now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        path = self.writer.write_dicts((i.to_row() for i in inspections), f"inspections_{now}.csv")
        context["csv_path"] = str(path)
        return context
