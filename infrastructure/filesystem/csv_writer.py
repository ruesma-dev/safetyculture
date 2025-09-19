# infrastructure/filesystem/csv_writer.py
from __future__ import annotations
import csv
from pathlib import Path
from typing import Iterable, Mapping


class CsvWriter:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write_dicts(self, rows: Iterable[Mapping[str, object]], filename: str) -> Path:
        rows = list(rows)
        if not rows:
            p = self.base_dir / filename
            # crear CSV vacío con cabeceras mínimas
            with p.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["audit_id", "modified_at", "template_id"])
                writer.writeheader()
            return p

        headers = list(rows[0].keys())
        p = self.base_dir / filename
        with p.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)
        return p
