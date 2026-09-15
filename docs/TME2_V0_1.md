# MelodyEngine_Lab V0.1 — Turkish Hook Lab foundation

This is the first working slice of Turkish Melody Engine 2 (TME2). The goal of this slice is to generate musically structured Turkish-style melody hooks that can later be auditioned through FLBridge with real FL Studio instruments.

This is a deterministic baseline generator and scorer, meant for generating, exporting, auditioning, and scoring real melody candidates. **No AI or external proprietary models are used here.**

## Internal Representation
We use a `MelodyIR` JSON format as the source of truth, allowing us to capture microtonal data (`pitch_cents`) for Makam music accurately. MIDI is purely an export format for playback and auditioning.

## Makam DNA
This system currently supports:
- NIHAVENT
- HICAZ
- USAK
- RAST
- HUZZAM
- KURDILIHICAZKAR

*Note on Heuristics vs Theory*: In this baseline, microtonal cents offsets provided in `makam.py` are *heuristics* approximating the Arel-Ezgi-Uzdilek / 53-TET system mapped onto 12-TET. They are not absolute theoretical certainties, but functional values designed for playback testing.

## Style Packs
Supported styles:
- ARABESK_POP
- POP_BALLAD
- ANATOLIAN_ROCK
- DARK_RNB_ALTPOP
- FANTEZI
- SUFI_ELECTRONIC

Style properties define note densities, syncopation tendencies, sustain ratios, and intervals.

## Generation
- **Motif Cell**: A 2-4 second melodic fragment based on makam degrees and style rhythms.
- **Audition Hook**: An extended phrase (4-8 seconds) generated deterministically using transformations on a motif cell (e.g., rhythmic variation, answer phrases).
- **8-bar Chorus**: Expands the top audition hook into a structured 8-bar loop.

## Scoring
The scorer runs deterministically to evaluate:
- `MakamFit`
- `StyleFit`
- `Singability`
- `HookStrength`
- `MotifCoherence`
- `RhythmFit`
- `CadenceFit`
- `Novelty`

*Note on Quality*: The baseline scorer does **not** measure human hit quality. It serves as a deterministic filter to reject structurally impossible patterns (invalid range, excessive leaps, note collisions).

## Export
Exports the resulting `MelodyIR` to JSON (preserving cents) and standard MIDI.
*Standard MIDI approximation*: Microtonal data is flattened to the nearest 12-TET pitch representation for audition compatibility. It does not represent exact makam playback.

## Next Steps for FLBridge Audition
- Create a consumer script in FLBridge to read the `MelodyIR` JSON and construct correct parameter automation in FL Studio.
- Map exact cents via pitch bend / specific microtonal VST parameters rather than standard MIDI.
- Generate specific VST instrument configurations mapping from the chosen `StylePack`.
