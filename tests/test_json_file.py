"""Test the JSONFile class."""

from typing import Generator

import pytest

from json_file import JSONFile


class TestJSONFile:
    """Test the JSONFile class."""

    @pytest.fixture()
    def temporary_file(self) -> Generator[JSONFile, None, None]:
        """Get a file path for testing and delete the test_data folder if it exists after the test."""
        temporary_file = JSONFile("test_data/file.json")
        yield temporary_file
        if temporary_file.parent == JSONFile("test_data"):
            temporary_file.parent.delete()

    def test_write(self, temporary_file: JSONFile) -> None:
        """Test the write method."""
        # Test empty cache without write_through
        output = {"abc": 123}
        temporary_file.write(output, write_through=False)
        assert temporary_file.cache.parsed is None

        # Test empty cache with write_through
        temporary_file.write(output)
        assert temporary_file.cache.parsed == output

        output = {"def": 456}

        # Test non-empty cache with write_through
        temporary_file.write(output)
        assert temporary_file.cache.parsed == output

        # Test non-empty cache without write_through
        temporary_file.write(output, write_through=False)
        assert temporary_file.cache.parsed is None

    def test_parse(self, temporary_file: JSONFile) -> None:
        """Test the parse method."""
        temporary_file.write({"abc": 123})
        assert temporary_file.parsed() == {"abc": 123}
        assert temporary_file.cache.parsed == {"abc": 123}
