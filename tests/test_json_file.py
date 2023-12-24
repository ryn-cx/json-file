"""Test the JSONFile class."""
import json

from json_file import JSONFile


class TestJSONFile:
    """Test the JSONFile class."""

    def test_parsed(self) -> None:
        """Test the parsed method."""
        file = JSONFile("tests/test_parsed.json")
        file.write(json.dumps({"key": "value"}))
        assert file.parsed()["key"] == "value"
        file.delete()

    def test_parsed_cached_changed_file(self) -> None:
        """Test the parsed_cached method when the file has changed."""
        file = JSONFile("tests/test_parsed_cached_changed_file.json")
        file.write(json.dumps({"key": "value"}))
        file.parsed_cached()
        file.write(json.dumps({"key2": "value2"}))
        assert file.parsed_cached()["key"] == "value"
        file.delete()

    def test_parsed_cached_updating_cache(self) -> None:
        """Test the parsed_cached method when the cache is updated."""
        file = JSONFile("tests/test_parsed_cached_updating_cache.json")
        file.write(json.dumps({"key": "value"}))
        file.parsed_cached()
        file.write(json.dumps({"key2": "value2"}))
        assert file.parsed_cached(reload=True)["key2"] == "value2"
        file.delete()
