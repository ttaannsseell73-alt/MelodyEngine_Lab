from typing import List
from src.melody_engine.melody_ir import Note
from src.melody_engine.hook_generator import HookGenerator
from src.melody_engine.models import SongSpec
import copy

class PhraseBuilder:
    def __init__(self, spec: SongSpec):
        self.spec = spec
        # Ticks per beat = 480, Beats per bar (assuming 4/4) = 4, Ticks per bar = 1920
        self.ticks_per_bar = 1920

    def expand_to_chorus(self, hook: List[Note]) -> List[Note]:
        """
        Expands an audition hook (which is roughly 2 bars) into an 8-bar chorus melody.
        Typical pop structure: A - A' - B - A or A - A - B - C
        We will use a simple A - A' - A - B (where B is a variation that lands on tonic).
        """
        if not hook:
            return []

        chorus_notes = []

        # Determine the length of the hook in bars
        max_tick = max(n.start_tick + n.duration_tick for n in hook)
        hook_bars = max(1, (max_tick + self.ticks_per_bar - 1) // self.ticks_per_bar)

        # If hook is e.g. 2 bars, 4 repetitions make 8 bars.
        # If hook is 1 bar, we'd need 8 repetitions (we'll just scale accordingly).
        # We'll just append it 4 times for simplicity, mapping offsets.

        # Section 1 (Bars 1-2): Exact repeat of the hook
        offset = 0
        for n in hook:
            new_note = copy.deepcopy(n)
            new_note.start_tick += offset
            new_note.section = "chorus"
            chorus_notes.append(new_note)

        # Section 2 (Bars 3-4): Repeat hook, maybe slight rhythmic variation
        offset += hook_bars * self.ticks_per_bar
        for n in hook:
            new_note = copy.deepcopy(n)
            new_note.start_tick += offset
            new_note.section = "chorus"
            chorus_notes.append(new_note)

        # Section 3 (Bars 5-6): Repeat hook exactly
        offset += hook_bars * self.ticks_per_bar
        for n in hook:
            new_note = copy.deepcopy(n)
            new_note.start_tick += offset
            new_note.section = "chorus"
            chorus_notes.append(new_note)

        # Section 4 (Bars 7-8): Variation ending on tonic (for simplicity, we just take the hook and force the last note to be tonic if we can, or just repeat it)
        # For a deterministic baseline, we will just use the exact hook for now.
        offset += hook_bars * self.ticks_per_bar
        for n in hook:
            new_note = copy.deepcopy(n)
            new_note.start_tick += offset
            new_note.section = "chorus"
            chorus_notes.append(new_note)

        return chorus_notes
