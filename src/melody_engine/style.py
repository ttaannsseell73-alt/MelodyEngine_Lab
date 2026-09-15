from dataclasses import dataclass
from typing import Dict

@dataclass
class StylePack:
    name: str
    phrase_length_tendency: int      # Target ticks for a standard phrase (e.g., 1920 for 1 bar at 480 PPQ)
    note_density: float              # Notes per beat on average
    syncopation_tendency: float      # Probability of syncopated rhythm (0.0 - 1.0)
    sustain_ratio: float             # Ratio of sustained notes to short notes
    repetition_probability: float    # Probability of repeating a previous motif/rhythm
    interval_preference: str         # E.g., 'steps', 'leaps', 'mixed'
    cadence_strength: float          # Likelihood to strongly land on karar (0.0 - 1.0)
    register_curve: str              # E.g., 'arch', 'descending', 'ascending'
    ornament_density: float          # Probability of adding grace notes/turns
    hook_repetition_tendency: float  # How likely a hook is an exact repeat vs varied

STYLES: Dict[str, StylePack] = {
    "ARABESK_POP": StylePack(
        name="ARABESK_POP",
        phrase_length_tendency=3840, # 2 bars
        note_density=3.0,
        syncopation_tendency=0.4,
        sustain_ratio=0.3,
        repetition_probability=0.7,
        interval_preference="mixed",
        cadence_strength=0.9,
        register_curve="descending",
        ornament_density=0.6,
        hook_repetition_tendency=0.8
    ),
    "POP_BALLAD": StylePack(
        name="POP_BALLAD",
        phrase_length_tendency=3840,
        note_density=1.5,
        syncopation_tendency=0.2,
        sustain_ratio=0.6,
        repetition_probability=0.5,
        interval_preference="steps",
        cadence_strength=0.8,
        register_curve="arch",
        ornament_density=0.2,
        hook_repetition_tendency=0.9
    ),
    "ANATOLIAN_ROCK": StylePack(
        name="ANATOLIAN_ROCK",
        phrase_length_tendency=3840,
        note_density=2.5,
        syncopation_tendency=0.7,
        sustain_ratio=0.4,
        repetition_probability=0.6,
        interval_preference="mixed",
        cadence_strength=0.7,
        register_curve="arch",
        ornament_density=0.4,
        hook_repetition_tendency=0.6
    ),
    "DARK_RNB_ALTPOP": StylePack(
        name="DARK_RNB_ALTPOP",
        phrase_length_tendency=1920, # 1 bar fragments
        note_density=2.0,
        syncopation_tendency=0.8,
        sustain_ratio=0.2,
        repetition_probability=0.8,
        interval_preference="steps",
        cadence_strength=0.5,
        register_curve="descending",
        ornament_density=0.1,
        hook_repetition_tendency=0.9
    ),
    "FANTEZI": StylePack(
        name="FANTEZI",
        phrase_length_tendency=3840,
        note_density=3.5,
        syncopation_tendency=0.5,
        sustain_ratio=0.3,
        repetition_probability=0.5,
        interval_preference="leaps",
        cadence_strength=0.8,
        register_curve="arch",
        ornament_density=0.8,
        hook_repetition_tendency=0.7
    ),
    "SUFI_ELECTRONIC": StylePack(
        name="SUFI_ELECTRONIC",
        phrase_length_tendency=7680, # 4 bars
        note_density=1.0,
        syncopation_tendency=0.3,
        sustain_ratio=0.8,
        repetition_probability=0.9,
        interval_preference="steps",
        cadence_strength=0.6,
        register_curve="ascending",
        ornament_density=0.5,
        hook_repetition_tendency=0.9
    )
}

def get_style(name: str) -> StylePack:
    if name not in STYLES:
        raise ValueError(f"Unknown style: {name}")
    return STYLES[name]
