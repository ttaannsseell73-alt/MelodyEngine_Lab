from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class MakamInfo:
    name: str
    # Degrees represented as (semitone_offset_from_tonic, cents_offset)
    # E.g., minor third might be (3, 0), while Ussak second might be (1, -15) approximately.
    # Note: These cents offsets are heuristics for standard 53-TET / Arel-Ezgi-Uzdilek approximations,
    # mapping to 12-TET base + cents.
    degrees: List[Tuple[int, float]]
    karar_degree: int # Index in the degrees list (usually 0)
    guclu_degree: int # Dominant degree index
    yeden_degree: int # Leading tone degree index
    preferred_regions: List[str] # E.g., ["lower", "middle", "upper"]
    characteristic_intervals: List[Tuple[int, int]] # Pair of degree indices that are characteristic
    cadence_tendencies: List[List[int]] # Sequences of degree indices for cadences

MAKAMS: Dict[str, MakamInfo] = {
    "NIHAVENT": MakamInfo(
        name="NIHAVENT",
        degrees=[(0, 0), (2, 0), (3, 0), (5, 0), (7, 0), (8, 0), (11, 0)], # Minor scale approximation
        karar_degree=0,
        guclu_degree=4, # 5th degree
        yeden_degree=6,
        preferred_regions=["middle", "upper"],
        characteristic_intervals=[(4, 3), (2, 0)],
        cadence_tendencies=[[4, 3, 2, 1, 0], [2, 1, 0]]
    ),
    "HICAZ": MakamInfo(
        name="HICAZ",
        # Hicaz tetrachord: 1, b2(+cents), 3(-cents), 4
        # Approximations: b2 is around 1 semitone but slightly sharp (e.g. +14c or -14c from next),
        # Here we use heuristic simplified cents.
        degrees=[(0, 0), (1, 14), (4, -14), (5, 0), (7, 0), (8, 14), (10, -14)],
        karar_degree=0,
        guclu_degree=3, # 4th degree
        yeden_degree=6,
        preferred_regions=["middle"],
        characteristic_intervals=[(1, 2), (2, 1), (3, 0)],
        cadence_tendencies=[[3, 2, 1, 0]]
    ),
    "USAK": MakamInfo(
        name="USAK",
        # Usak: 1, 2(approx -25c), b3, 4, 5, b6, b7
        degrees=[(0, 0), (2, -25), (3, 0), (5, 0), (7, 0), (8, 0), (10, 0)],
        karar_degree=0,
        guclu_degree=3,
        yeden_degree=6,
        preferred_regions=["lower", "middle"],
        characteristic_intervals=[(1, 0), (3, 2)],
        cadence_tendencies=[[3, 2, 1, 0]]
    ),
    "RAST": MakamInfo(
        name="RAST",
        # Rast: 1, 2, 3(approx -25c), 4, 5, 6, 7(approx -25c)
        degrees=[(0, 0), (2, 0), (4, -25), (5, 0), (7, 0), (9, 0), (11, -25)],
        karar_degree=0,
        guclu_degree=4,
        yeden_degree=6,
        preferred_regions=["middle", "upper"],
        characteristic_intervals=[(2, 0), (4, 2)],
        cadence_tendencies=[[4, 3, 2, 1, 0], [2, 1, 0]]
    ),
    "HUZZAM": MakamInfo(
        name="HUZZAM",
        # Huzzam: tonic is segah (often E half flat). We'll map tonic to 0 relative.
        # 1, 2, b3(+cents), 4, 5, 6, b7
        degrees=[(0, 0), (2, -14), (3, 14), (5, 0), (7, 0), (8, 14), (11, -14)], # Heuristic mapping
        karar_degree=0,
        guclu_degree=4,
        yeden_degree=6,
        preferred_regions=["upper"],
        characteristic_intervals=[(4, 3), (3, 2)],
        cadence_tendencies=[[4, 3, 2, 1, 0]]
    ),
    "KURDILIHICAZKAR": MakamInfo(
        name="KURDILIHICAZKAR",
        # Natural minor roughly, with different melodic progression
        degrees=[(0, 0), (1, 0), (3, 0), (5, 0), (7, 0), (8, 0), (10, 0)],
        karar_degree=0,
        guclu_degree=3,
        yeden_degree=6,
        preferred_regions=["lower", "middle"],
        characteristic_intervals=[(3, 2), (1, 0)],
        cadence_tendencies=[[3, 2, 1, 0]]
    )
}

def get_makam(name: str) -> MakamInfo:
    if name not in MAKAMS:
        raise ValueError(f"Unknown makam: {name}")
    return MAKAMS[name]
