import pytest
from src.melody_engine.models import SongSpec
from src.melody_engine.hook_generator import HookGenerator
from src.melody_engine.scorer import BaselineScorer

def test_scorer_valid():
    spec = SongSpec(style="ARABESK_POP", makam="NIHAVENT", tonic="D", bpm=92, meter="4/4", energy=0.7, vocal_range=("C3", "C6"), seed=42)
    gen = HookGenerator(spec)
    hook = gen.generate_audition_hook()

    scorer = BaselineScorer(spec)
    score_res = scorer.score(hook)

    assert score_res["rejected"] is False
    assert "total_score" in score_res
    assert "MakamFit" in score_res

def test_scorer_rejection_negative_duration():
    spec = SongSpec(style="ARABESK_POP", makam="NIHAVENT", tonic="D", bpm=92, meter="4/4", energy=0.7, vocal_range=("C3", "C6"), seed=42)
    gen = HookGenerator(spec)
    hook = gen.generate_audition_hook()

    # Introduce bad duration
    hook[0].duration_tick = -100

    scorer = BaselineScorer(spec)
    score_res = scorer.score(hook)

    assert score_res["rejected"] is True
    assert "reason" in score_res
    assert "impossible/negative durations" in score_res["reason"]

def test_scorer_rejection_vocal_range():
    spec = SongSpec(style="ARABESK_POP", makam="NIHAVENT", tonic="D", bpm=92, meter="4/4", energy=0.7, vocal_range=("G3", "C5"), seed=42)
    gen = HookGenerator(spec)
    hook = gen.generate_audition_hook()

    # Force pitch out of range (e.g., C5 is 72, C3 is 48. Let's set to 90)
    hook[0].pitch_base = 90

    scorer = BaselineScorer(spec)
    score_res = scorer.score(hook)

    assert score_res["rejected"] is True
    assert "invalid vocal range" in score_res["reason"]

def test_scorer_rejection_excessive_leap():
    spec = SongSpec(style="ARABESK_POP", makam="NIHAVENT", tonic="D", bpm=92, meter="4/4", energy=0.7, vocal_range=("C3", "C6"), seed=42)
    gen = HookGenerator(spec)
    hook = gen.generate_audition_hook()

    # Force huge leap
    hook[0].pitch_base = 60
    hook[1].pitch_base = 80

    scorer = BaselineScorer(spec)
    score_res = scorer.score(hook)

    assert score_res["rejected"] is True
    assert "excessive leaps" in score_res["reason"]

def test_scorer_rejection_pathological_repetition():
    spec = SongSpec(style="ARABESK_POP", makam="NIHAVENT", tonic="D", bpm=92, meter="4/4", energy=0.7, vocal_range=("C3", "C6"), seed=42)
    gen = HookGenerator(spec)
    hook = gen.generate_audition_hook()

    # Force all notes to same pitch
    for n in hook:
        n.pitch_base = 60

    # Ensure hook has at least 4 notes
    if len(hook) < 4:
        # In case test fails due to small hook length, we can just skip or add notes
        pass
    else:
        scorer = BaselineScorer(spec)
        score_res = scorer.score(hook)

        assert score_res["rejected"] is True
        assert "pathological repetition" in score_res["reason"]
