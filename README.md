# MelodyEngine_Lab V0.1

This is the deterministic baseline engine for generating Turkish-style melody hooks, based on Makam and Style parameters.

## Setup

Requires Python 3.9+.

```bash
pip install mido pytest
```

## Running Tests

Ensure `PYTHONPATH` is set to the repository root.

```bash
PYTHONPATH=. pytest tests/
```

## Usage

Generate candidates via the CLI:

```bash
python -m src.melody_engine.cli generate \
  --style ARABESK_POP \
  --makam NIHAVENT \
  --bpm 92 \
  --tonic D \
  --seed 42 \
  --count 32 \
  --output out/
```

Check the `out/` folder for the top candidate JSON, MIDI, and 8-bar chorus MIDI, along with the ranking report.

See `docs/TME2_V0_1.md` for more details on the implementation.
