import pytest
from src.melody_engine.models import SongSpec
from src.melody_engine.hook_generator import HookGenerator
from src.melody_engine.scorer import BaselineScorer

def test_deterministic_generation():
    spec1 = SongSpec(style="ARABESK_POP", makam="NIHAVENT", tonic="D", bpm=92, meter="4/4", energy=0.7, vocal_range=("G3", "C5"), seed=42)
    gen1 = HookGenerator(spec1)
    hooks1 = gen1.generate_candidates(2)

    spec2 = SongSpec(style="ARABESK_POP", makam="NIHAVENT", tonic="D", bpm=92, meter="4/4", energy=0.7, vocal_range=("G3", "C5"), seed=42)
    gen2 = HookGenerator(spec2)
    hooks2 = gen2.generate_candidates(2)

    # Check that identical seeds produce identical hooks
    assert len(hooks1) == len(hooks2)
    for h1, h2 in zip(hooks1, hooks2):
        assert len(h1) == len(h2)
        for n1, n2 in zip(h1, h2):
            assert n1.pitch_base == n2.pitch_base
            assert n1.start_tick == n2.start_tick

def test_different_seeds_produce_different_results():
    spec1 = SongSpec(style="ARABESK_POP", makam="NIHAVENT", tonic="D", bpm=92, meter="4/4", energy=0.7, vocal_range=("G3", "C5"), seed=42)
    gen1 = HookGenerator(spec1)
    hooks1 = gen1.generate_candidates(1)[0]

    spec2 = SongSpec(style="ARABESK_POP", makam="NIHAVENT", tonic="D", bpm=92, meter="4/4", energy=0.7, vocal_range=("G3", "C5"), seed=99)
    gen2 = HookGenerator(spec2)
    hooks2 = gen2.generate_candidates(1)[0]

    # Ideally they differ.
    assert [n.pitch_base for n in hooks1] != [n.pitch_base for n in hooks2]

def test_lengths():
    spec = SongSpec(style="ARABESK_POP", makam="NIHAVENT", tonic="D", bpm=92, meter="4/4", energy=0.7, vocal_range=("G3", "C5"), seed=42)
    gen = HookGenerator(spec)

    # Motif cell usually has 3-7 notes
    motif = gen.generate_motif_cell()
    assert 3 <= len(motif) <= 7

    # Hook should typically have multiple notes
    hook = gen.generate_audition_hook()
    assert len(hook) >= 3 # Some transformations might be small, but generally >3
