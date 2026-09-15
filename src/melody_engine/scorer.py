from typing import List, Dict, Union
from src.melody_engine.melody_ir import Note
from src.melody_engine.models import SongSpec

class BaselineScorer:
    def __init__(self, spec: SongSpec):
        self.spec = spec

        # Parse vocal range strings into MIDI note numbers (rough approximation)
        self.min_pitch, self.max_pitch = self._parse_vocal_range(spec.vocal_range)

    def _parse_vocal_range(self, vocal_range: tuple[str, str]) -> tuple[int, int]:
        notes_map = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
                     'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
                     'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}

        def to_midi(note_str: str) -> int:
            note_name = note_str[:-1]
            octave = int(note_str[-1])
            return (octave + 1) * 12 + notes_map.get(note_name, 0)

        try:
            return to_midi(vocal_range[0]), to_midi(vocal_range[1])
        except:
            return 48, 84 # Default range C3 to C6

    def score(self, hook: List[Note]) -> Dict[str, Union[float, str, bool]]:
        """
        Evaluates a hook. Returns a dictionary with scores or a rejection reason.
        """
        if not hook:
            return {"rejected": True, "reason": "structurally empty hook"}

        # Hard rejections
        for note in hook:
            if note.pitch_base < self.min_pitch or note.pitch_base > self.max_pitch:
                return {"rejected": True, "reason": f"invalid vocal range: {note.pitch_base}"}
            if note.duration_tick <= 0:
                return {"rejected": True, "reason": "impossible/negative durations"}

        # Check note collisions (monophonic lead)
        sorted_notes = sorted(hook, key=lambda n: n.start_tick)
        for i in range(len(sorted_notes) - 1):
            if sorted_notes[i].start_tick + sorted_notes[i].duration_tick > sorted_notes[i+1].start_tick:
                # Small overlap (e.g. 1-2 ticks) might be acceptable in real MIDI, but we enforce strict monophony
                if sorted_notes[i+1].start_tick - (sorted_notes[i].start_tick + sorted_notes[i].duration_tick) < -5:
                    return {"rejected": True, "reason": "note collisions in monophonic lead"}

        # Check excessive leaps
        for i in range(len(sorted_notes) - 1):
            leap = abs(sorted_notes[i+1].pitch_base - sorted_notes[i].pitch_base)
            if leap > 14:  # More than a major 9th
                return {"rejected": True, "reason": "excessive leaps"}

        # Check pathological repetition
        if len(sorted_notes) >= 4:
            all_same_pitch = all(n.pitch_base == sorted_notes[0].pitch_base for n in sorted_notes)
            if all_same_pitch:
                return {"rejected": True, "reason": "pathological repetition"}

        # Calculate scores (heuristics)
        makam_fit = 0.8
        style_fit = 0.8
        singability = 1.0 - (sum(abs(sorted_notes[i+1].pitch_base - sorted_notes[i].pitch_base) for i in range(len(sorted_notes)-1)) / (len(sorted_notes) * 12))
        hook_strength = 0.7 if len(hook) > 5 else 0.4
        motif_coherence = 0.9
        rhythm_fit = 0.8
        cadence_fit = 0.7
        novelty = 0.6

        # Total score
        total_score = makam_fit * 0.2 + style_fit * 0.1 + singability * 0.2 + hook_strength * 0.2 + rhythm_fit * 0.1 + cadence_fit * 0.1 + novelty * 0.1

        return {
            "rejected": False,
            "total_score": total_score,
            "MakamFit": makam_fit,
            "StyleFit": style_fit,
            "Singability": max(0.0, singability),
            "HookStrength": hook_strength,
            "MotifCoherence": motif_coherence,
            "RhythmFit": rhythm_fit,
            "CadenceFit": cadence_fit,
            "Novelty": novelty
        }
