# core/pipeline/pipeline.py
from __future__ import annotations
from typing import Dict, Any, Iterable
from .step import Step


class Pipeline:
    def __init__(self, steps: Iterable[Step]) -> None:
        self.steps = list(steps)

    def run(self, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        ctx: Dict[str, Any] = {} if context is None else dict(context)
        for step in self.steps:
            ctx = step.run(ctx)
        return ctx
