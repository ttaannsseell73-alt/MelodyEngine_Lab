import json
from dataclasses import dataclass, asdict
from typing import Optional, List

@dataclass
class Note:
    pitch_base: int         # MIDI note number (0-127)
    pitch_cents: float      # Microtonal offset in cents (-50 to +50 typically)
    start_tick: int         # Start time in ticks (assuming 480 PPQ for standard usage)
    duration_tick: int      # Duration in ticks
    velocity: int           # Velocity (0-127)
    section: str            # E.g., 'motif', 'hook', 'chorus'
    phrase_id: int          # To group notes by phrase
    motif_id: int           # To group notes by motif
    syllable: Optional[str] = None
    stress: Optional[float] = None

@dataclass
class MelodyIR:
    notes: List[Note]

    def to_json(self) -> str:
        return json.dumps([asdict(note) for note in self.notes], indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'MelodyIR':
        data = json.loads(json_str)
        notes = [Note(**note_data) for note_data in data]
        return cls(notes=notes)
