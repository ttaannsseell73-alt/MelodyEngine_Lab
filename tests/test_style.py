import pytest
from src.melody_engine.style import get_style, STYLES

def test_all_styles_load():
    expected_styles = ["ARABESK_POP", "POP_BALLAD", "ANATOLIAN_ROCK", "DARK_RNB_ALTPOP", "FANTEZI", "SUFI_ELECTRONIC"]
    for s in expected_styles:
        style = get_style(s)
        assert style.name == s
        assert style.note_density > 0

def test_invalid_style():
    with pytest.raises(ValueError):
        get_style("INVALID_STYLE")
