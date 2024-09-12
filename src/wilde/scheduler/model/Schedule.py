from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Schedule:
    interval: int
    start: Optional[int] = None

    def __str__(self):
        return f"Every {self.interval} minutes, starting {self.start})"
    
    def __repr__(self) -> str:
        return f"(interval={self.interval}, start={self.start})"
