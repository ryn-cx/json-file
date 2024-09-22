"""Test the JSONFile class."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest
from paved_path import PavedPath

from src.json_file import JSONFile

if TYPE_CHECKING:
    from collections.abc import Generator

    from _pytest.fixtures import SubRequest

def cache_is_empty(temp_path: JSONFile) -> bool:
    """Check if the cache is empty."""
    return (
        temp_path.cached_json is None
        and temp_path.cached_text is None
        and temp_path.cached_bytes is None
        and temp_path.cache_timestamp is None
    )


@pytest.fixture(name="temp_path")
def temp_path_fixture(request: SubRequest) -> Generator[JSONFile, Any, Any]:
    """Create a clean state for tests and cleans it up upon test completion."""
    temp_dir = PavedPath(__file__).parent / "data"
    temp_path = JSONFile(f"{temp_dir}/{request.node.name}")
    if temp_path.parent == Path(temp_dir):
        temp_path.parent.delete_dir()
    yield temp_path
    if temp_path.parent == Path(temp_dir):
        temp_path.parent.delete_dir()


def make_list(number: int) -> list[str | int]:
    """Make a list for testing."""
    return [number, f"Text {number}", f"{number}"]


def make_dict(number: int) -> dict[str, str | int]:
    """Make a dictionary for testing."""
    return {f"key {number}": f"value {number}"}


class TestReadJSON:
    def test_read_list(self, temp_path: JSONFile) -> None:
        temp_path.write_json(make_list(1))
        new_path = JSONFile(temp_path)
        assert new_path.read_json() == make_list(1)

    def test_read_dict(self, temp_path: JSONFile) -> None:
        temp_path.write_json(make_dict(1))
        new_path = JSONFile(temp_path)
        assert new_path.read_json() == make_dict(1)

    def test_read_str(self, temp_path: JSONFile) -> None:
        temp_path.write_json(json.dumps(make_list(1)))
        new_path = JSONFile(temp_path)
        assert new_path.read_json() == make_list(1)


class TestClearCache:
    def test_clear_cache(self, temp_path: JSONFile) -> None:
        temp_path.write_json(make_list(1))
        temp_path.clear_cache()
        assert cache_is_empty(temp_path)


class TestWrite:
    def test_write_json(self, temp_path: JSONFile) -> None:
        temp_path.write_json(make_dict(1))
        assert temp_path.cached_json == make_dict(1)

    def test_write_json_filled_cache(self, temp_path: JSONFile) -> None:
        temp_path.write_json(make_dict(1))
        temp_path.write_json(make_dict(2), write_through=False)
        assert cache_is_empty(temp_path)

    def test_write_json_empty_cache_no_write_through(
        self,
        temp_path: JSONFile,
    ) -> None:
        temp_path.write_json(make_dict(1), write_through=False)
        assert cache_is_empty(temp_path)

    def test_write_json_filled_cache_no_write_through(
        self,
        temp_path: JSONFile,
    ) -> None:
        temp_path.write_json(make_dict(1))
        temp_path.write_json(make_dict(2))
        assert temp_path.cached_json == make_dict(2)


    def test_write_invalid_dict(self, temp_path: JSONFile) -> None:
        msg = "Serialization will create an output that is different from the input"
        with pytest.raises(ValueError, match=msg):
            temp_path.write_json({"key": 1, 1: "value"})

    def test_write_invalid_str(self, temp_path: JSONFile) -> None:
        with pytest.raises(json.JSONDecodeError):
            temp_path.write_json("String")
