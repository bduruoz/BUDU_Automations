# core/interfaces.py
from typing import Protocol, runtime_checkable

@runtime_checkable
class ContentGenerator(Protocol):
    def generate(self, row: dict, cfg) -> dict: ...