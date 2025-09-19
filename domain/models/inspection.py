# domain/models/inspection.py
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Inspection:
    audit_id: str
    modified_at: str | None = None
    template_id: str | None = None

    @staticmethod
    def from_api(d: dict) -> "Inspection":
        return Inspection(
            audit_id=d.get("audit_id") or d.get("id") or "",
            modified_at=d.get("modified_at"),
            template_id=d.get("template_id"),
        )

    def to_row(self) -> dict:
        return {
            "audit_id": self.audit_id,
            "modified_at": self.modified_at,
            "template_id": self.template_id,
        }
