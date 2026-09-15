import pytest
import json
from src.melody_engine.melody_ir import Note, MelodyIR

def test_note_creation():
    n = Note(pitch_base=60, pitch_cents=10.5, start_tick=0, duration_tick=480, velocity=100, section="A", phrase_id=1, motif_id=1)
    assert n.pitch_base == 60
    assert n.pitch_cents == 10.5

def test_melody_ir_json_roundtrip():
    n1 = Note(pitch_base=60, pitch_cents=10.5, start_tick=0, duration_tick=480, velocity=100, section="A", phrase_id=1, motif_id=1)
    n2 = Note(pitch_base=62, pitch_cents=-14.0, start_tick=480, duration_tick=480, velocity=90, section="A", phrase_id=1, motif_id=1)

    ir = MelodyIR(notes=[n1, n2])
    json_str = ir.to_json()

    # Verify pitch_cents preserved in json text
    assert "10.5" in json_str
    assert "-14.0" in json_str

    ir2 = MelodyIR.from_json(json_str)

    assert len(ir2.notes) == 2
    assert ir2.notes[0].pitch_cents == 10.5
    assert ir2.notes[1].pitch_cents == -14.0
