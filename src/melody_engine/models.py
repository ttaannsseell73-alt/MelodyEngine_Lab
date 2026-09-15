from dataclasses import dataclass
from typing import Optional

@dataclass
class SongSpec:
    style: str
    makam: str
    tonic: str
    bpm: int
    meter: str
    energy: float
    vocal_range: tuple[str, str]  # e.g., ("G3", "C5")
    seed: int
