import json
from typing import List
from mido import Message, MidiFile, MidiTrack, MetaMessage
from src.melody_engine.melody_ir import Note

class Exporter:
    def __init__(self, bpm: int = 120, ppq: int = 480):
        self.bpm = bpm
        self.ppq = ppq

    def export_json(self, notes: List[Note], filepath: str):
        """Exports the MelodyIR notes to JSON, preserving all microtonal data."""
        data = [
            {
                "pitch_base": n.pitch_base,
                "pitch_cents": n.pitch_cents,
                "start_tick": n.start_tick,
                "duration_tick": n.duration_tick,
                "velocity": n.velocity,
                "section": n.section,
                "phrase_id": n.phrase_id,
                "motif_id": n.motif_id,
                "syllable": n.syllable,
                "stress": n.stress
            }
            for n in notes
        ]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def export_midi(self, notes: List[Note], filepath: str):
        """
        Exports the notes to standard MIDI format for auditioning.
        NOTE: This flattens cents information to nearest 12-TET representations.
        This is strictly an approximation for audition purposes.
        """
        mid = MidiFile(ticks_per_beat=self.ppq)
        track = MidiTrack()
        mid.tracks.append(track)

        # Set tempo
        tempo = int(60000000 / self.bpm) # Microseconds per beat
        track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

        # Prepare events: (tick, 'note_on'/'note_off', note, velocity)
        events = []
        for n in notes:
            # We map the microtonal pitch to the closest standard MIDI note.
            # E.g. pitch_base=60, pitch_cents=40 -> 60
            # E.g. pitch_base=60, pitch_cents=60 -> 61 (if we wanted to strictly round,
            # but usually pitch_base is the intended key and cents is just offset.
            # We will just use pitch_base for standard MIDI).
            pitch = n.pitch_base
            if n.pitch_cents > 50:
                pitch += 1
            elif n.pitch_cents < -50:
                pitch -= 1

            events.append({"tick": n.start_tick, "type": "note_on", "pitch": pitch, "velocity": n.velocity})
            events.append({"tick": n.start_tick + n.duration_tick, "type": "note_off", "pitch": pitch, "velocity": 0})

        # Sort events by tick, then note_off before note_on
        events.sort(key=lambda e: (e["tick"], 0 if e["type"] == "note_off" else 1))

        last_tick = 0
        for e in events:
            delta = e["tick"] - last_tick
            if e["type"] == "note_on":
                track.append(Message('note_on', note=e["pitch"], velocity=e["velocity"], time=delta))
            else:
                track.append(Message('note_off', note=e["pitch"], velocity=e["velocity"], time=delta))
            last_tick = e["tick"]

        mid.save(filepath)
