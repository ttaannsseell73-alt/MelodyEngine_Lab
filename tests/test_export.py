import os
import json
import pytest
from src.melody_engine.models import SongSpec
from src.melody_engine.hook_generator import HookGenerator
from src.melody_engine.phrase_builder import PhraseBuilder
from src.melody_engine.midi_export import Exporter
from mido import MidiFile

def test_expansion():
    spec = SongSpec(style="ARABESK_POP", makam="NIHAVENT", tonic="D", bpm=92, meter="4/4", energy=0.7, vocal_range=("G3", "C5"), seed=42)
    gen = HookGenerator(spec)
    hook = gen.generate_audition_hook()

    builder = PhraseBuilder(spec)
    chorus = builder.expand_to_chorus(hook)

    # Chorus should roughly be 4x the length of the hook for our simple A-A'-A-B structure
    assert len(chorus) >= len(hook) * 4

def test_export(tmpdir):
    spec = SongSpec(style="ARABESK_POP", makam="NIHAVENT", tonic="D", bpm=92, meter="4/4", energy=0.7, vocal_range=("G3", "C5"), seed=42)
    gen = HookGenerator(spec)
    hook = gen.generate_audition_hook()

    exporter = Exporter(bpm=spec.bpm)
    json_path = os.path.join(tmpdir, "test.json")
    midi_path = os.path.join(tmpdir, "test.mid")

    exporter.export_json(hook, json_path)
    exporter.export_midi(hook, midi_path)

    assert os.path.exists(json_path)
    assert os.path.exists(midi_path)

    # Verify JSON content
    with open(json_path, 'r') as f:
        data = json.load(f)
        assert len(data) == len(hook)

    # Verify MIDI content loads
    mid = MidiFile(midi_path)
    assert len(mid.tracks) > 0
