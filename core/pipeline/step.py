# core/pipeline/step.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any


class Step(ABC):
    """Paso de pipeline: recibe y devuelve un 'context' mutado."""

    @abstractmethod
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
