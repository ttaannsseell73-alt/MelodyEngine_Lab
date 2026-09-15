import pytest
from src.melody_engine.makam import get_makam, MAKAMS

def test_all_makams_load():
    expected_makams = ["NIHAVENT", "HICAZ", "USAK", "RAST", "HUZZAM", "KURDILIHICAZKAR"]
    for m in expected_makams:
        makam = get_makam(m)
        assert makam.name == m
        assert len(makam.degrees) > 0

def test_invalid_makam():
    with pytest.raises(ValueError):
        get_makam("INVALID_MAKAM")
