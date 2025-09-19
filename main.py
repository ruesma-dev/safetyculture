# main.py
from __future__ import annotations
import logging
from core.pipeline.pipeline import Pipeline
from application.steps.extract_inspections_step import ExtractInspectionsStep
from application.steps.export_csv_step import ExportCsvStep
from infrastructure.http.safetyculture_client import SafetyCultureClient
from infrastructure.filesystem.csv_writer import CsvWriter
from config.settings import Settings


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def build_pipeline(settings: Settings) -> Pipeline:
    client = SafetyCultureClient(
        base_url=settings.safetyculture_base_url,
        token=settings.safetyculture_token,
    )
    writer = CsvWriter(settings.output_dir)

    steps = [
        ExtractInspectionsStep(client),
        ExportCsvStep(writer),
    ]
    return Pipeline(steps)


if __name__ == "__main__":
    configure_logging()
    settings = Settings()
    logging.info("▶ Iniciando pipeline de exportación a CSV (inspecciones)")
    pipeline = build_pipeline(settings)
    context = {
        "modified_after": settings.modified_after,
        "modified_before": settings.modified_before,
        "include_archived": settings.include_archived,
        "templates": settings.templates,
    }
    result = pipeline.run(context)
    logging.info("✓ Exportación completada: %s", result.get("csv_path"))
    logging.info("count=%s total=%s", result.get("count"), result.get("total"))
