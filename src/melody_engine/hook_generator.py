import random
from typing import List, Optional
from src.melody_engine.models import SongSpec
from src.melody_engine.melody_ir import Note, MelodyIR
from src.melody_engine.makam import get_makam, MakamInfo
from src.melody_engine.style import get_style, StylePack

class HookGenerator:
    def __init__(self, spec: SongSpec):
        self.spec = spec
        self.makam_info = get_makam(spec.makam)
        self.style_pack = get_style(spec.style)
        self.rng = random.Random(spec.seed)

        # Parse tonic
        notes_map = {'C': 60, 'C#': 61, 'Db': 61, 'D': 62, 'D#': 63, 'Eb': 63,
                     'E': 64, 'F': 65, 'F#': 66, 'Gb': 66, 'G': 67, 'G#': 68,
                     'Ab': 68, 'A': 69, 'A#': 70, 'Bb': 70, 'B': 71}
        tonic_base_octave = notes_map.get(spec.tonic, 60)

        # Convert degrees to absolute pitches around middle C
        self.scale_pitches = []
        for octave in range(-1, 2):  # Build a 3-octave scale
            for degree_idx, (semitone_offset, cents) in enumerate(self.makam_info.degrees):
                pitch = tonic_base_octave + (octave * 12) + semitone_offset
                self.scale_pitches.append({
                    "degree": degree_idx,
                    "pitch": pitch,
                    "cents": cents,
                    "octave": octave
                })

        # Sort by pitch
        self.scale_pitches.sort(key=lambda x: x["pitch"])

    def _get_pitch_by_degree(self, degree: int, octave: int = 0) -> dict:
        """Find the scale pitch dict for a given degree and octave relative to tonic."""
        # Find tonic
        tonic_pitches = [p for p in self.scale_pitches if p["degree"] == self.makam_info.karar_degree and p["octave"] == 0]
        if not tonic_pitches:
            return self.scale_pitches[len(self.scale_pitches) // 2]

        for p in self.scale_pitches:
            if p["degree"] == degree and p["octave"] == octave:
                return p

        # Fallback to closest if out of range
        closest = min(self.scale_pitches, key=lambda p: abs(p["degree"] - degree) + abs(p["octave"] - octave) * 7)
        return closest

    def generate_motif_cell(self, start_tick: int = 0, phrase_id: int = 1, motif_id: int = 1) -> List[Note]:
        """Generates a motif cell of 2-4 seconds (3-7 core notes)."""
        # Duration depends on BPM. Let's aim for 1 to 2 bars.
        # For simplicity, 1 bar = 4 beats = 1920 ticks (at 480 PPQ)

        target_notes = self.rng.randint(3, 7)
        notes = []

        current_tick = start_tick

        # Start degree (often guclu or tonic)
        start_degree = self.rng.choice([self.makam_info.karar_degree, self.makam_info.guclu_degree])
        current_degree = start_degree
        current_octave = 0

        for i in range(target_notes):
            pitch_info = self._get_pitch_by_degree(current_degree % 7, current_octave)

            # Duration logic (e.g., 240=8th, 480=quarter, 960=half)
            durations = [240, 480, 480, 960]
            if self.rng.random() < self.style_pack.syncopation_tendency:
                durations.append(120) # 16th note for syncopation
            duration = self.rng.choice(durations)

            # Sustain logic
            if i == target_notes - 1 or self.rng.random() < self.style_pack.sustain_ratio:
                duration = max(duration, 960) # Longer note

            velocity = self.rng.randint(80, 110)

            note = Note(
                pitch_base=pitch_info["pitch"],
                pitch_cents=pitch_info["cents"],
                start_tick=current_tick,
                duration_tick=duration,
                velocity=velocity,
                section="motif",
                phrase_id=phrase_id,
                motif_id=motif_id
            )
            notes.append(note)

            current_tick += duration

            # Move to next degree
            step = self.rng.choice([-1, 0, 1, 1, -2, 2])
            current_degree += step

            # Keep within reasonable bounds
            if current_degree > 6:
                current_degree -= 7
                current_octave += 1
            elif current_degree < 0:
                current_degree += 7
                current_octave -= 1

        return notes


    def generate_audition_hook(self, phrase_id: int = 1) -> List[Note]:
        """Generates an audition hook of 4-8 seconds (5-12 main notes).
        Uses a motif cell and applies transformations to build a complete phrase.
        """
        motif = self.generate_motif_cell(start_tick=0, phrase_id=phrase_id, motif_id=1)

        # Decide how to complete the hook based on style tendencies
        transformations = ["literal_repeat", "rhythmic_variation", "answer_phrase", "extension"]
        chosen_transform = self.rng.choices(
            transformations,
            weights=[self.style_pack.hook_repetition_tendency, 0.5, 0.8, 0.4],
            k=1
        )[0]

        # Determine the tick where the motif ends
        motif_end_tick = motif[-1].start_tick + motif[-1].duration_tick

        # We usually want hooks to align to standard bar boundaries (e.g. 1920 ticks = 1 bar)
        # We'll align the next part to the next half-bar or bar.
        align_tick = ((motif_end_tick // 960) + 1) * 960
        if align_tick - motif_end_tick > 960:
            align_tick = motif_end_tick

        hook_notes = list(motif)

        if chosen_transform == "literal_repeat":
            for n in motif:
                new_note = Note(
                    pitch_base=n.pitch_base, pitch_cents=n.pitch_cents,
                    start_tick=n.start_tick + align_tick, duration_tick=n.duration_tick,
                    velocity=n.velocity, section="hook", phrase_id=phrase_id, motif_id=2
                )
                hook_notes.append(new_note)

        elif chosen_transform == "rhythmic_variation":
            for n in motif:
                new_dur = n.duration_tick
                if self.rng.random() < 0.5:
                    new_dur = new_dur // 2 if new_dur > 240 else new_dur * 2
                new_note = Note(
                    pitch_base=n.pitch_base, pitch_cents=n.pitch_cents,
                    start_tick=n.start_tick + align_tick, duration_tick=new_dur,
                    velocity=n.velocity, section="hook", phrase_id=phrase_id, motif_id=2
                )
                hook_notes.append(new_note)

        elif chosen_transform == "answer_phrase":
            # Generate a new motif cell that ideally descends to karar (cadence)
            answer_motif = self.generate_motif_cell(start_tick=align_tick, phrase_id=phrase_id, motif_id=2)
            # Force the last note to be the karar (tonic)
            tonic_pitch = self._get_pitch_by_degree(self.makam_info.karar_degree, 0)
            answer_motif[-1].pitch_base = tonic_pitch["pitch"]
            answer_motif[-1].pitch_cents = tonic_pitch["cents"]
            answer_motif[-1].duration_tick = max(answer_motif[-1].duration_tick, 960)
            hook_notes.extend(answer_motif)

        elif chosen_transform == "extension":
            # Just add a few more notes extending the first motif
            extension = self.generate_motif_cell(start_tick=align_tick, phrase_id=phrase_id, motif_id=2)
            # Truncate extension to just 2-3 notes
            hook_notes.extend(extension[:3])

        # Ensure section is set to hook for all
        for n in hook_notes:
            n.section = "hook"

        return hook_notes

    def generate_candidates(self, count: int = 32) -> List[List[Note]]:
        """Generates N deterministic audition hook candidates."""
        candidates = []
        for i in range(count):
            # The rng is stateful, so generating sequentially guarantees deterministic variations
            hook = self.generate_audition_hook(phrase_id=i+1)
            candidates.append(hook)
        return candidates
