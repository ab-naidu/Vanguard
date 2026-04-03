import pytest

from vanguard.json_extract import extract_json_object


def test_extract_from_fence():
    text = 'Here:\n```json\n{"a": 1}\n```\n'
    assert extract_json_object(text) == {"a": 1}


def test_extract_plain():
    assert extract_json_object('prefix {"x": "y"} suffix') == {"x": "y"}


def test_no_json_raises():
    with pytest.raises(ValueError):
        extract_json_object("no braces")
