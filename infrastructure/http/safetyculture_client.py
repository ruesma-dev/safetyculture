# infrastructure/http/safetyculture_client.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Iterable
import requests


@dataclass(frozen=True)
class SafetyCultureClient:
    base_url: str
    token: str
    timeout: int = 30

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }

    def search_inspections(
        self,
        fields: Iterable[str] = ("audit_id", "modified_at", "template_id"),
        modified_after: str | None = None,
        modified_before: str | None = None,
        include_archived: bool = False,
        templates: Iterable[str] = (),
    ) -> Dict[str, Any]:
        """
        Llama a GET /audits/search. Devuelve el JSON crudo.
        Nota: el endpoint devuelve hasta 1000 inspecciones por defecto.
        """
        url = f"{self.base_url}/audits/search"
        params: list[tuple[str, str]] = []
        for f in fields:
            params.append(("field", f))
        if modified_after:
            params.append(("modified_after", modified_after))
        if modified_before:
            params.append(("modified_before", modified_before))
        if include_archived:
            params.append(("include_archived", "true"))
        for t in templates:
            params.append(("template", t))

        resp = requests.get(url, headers=self._headers(), params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()
