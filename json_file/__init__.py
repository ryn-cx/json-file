"""Library for working with JSON files."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING

from paved_path import PavedPath

if TYPE_CHECKING:
    from typing import Any

    from paved_path import PathableType


class JSONFile(PavedPath):
    """Library for working with JSON files."""

    def __init__(self, *_args: PathableType) -> None:
        """Initialize the JSONFile object."""
        self.parsed_cached_value = None
        super().__init__()

    def parsed(self) -> Any:  # type: ignore # noqa: PGH003, ANN401 - Impossible to know thereturn type of a loaded json
        # file so in this situation returning Any is the only logical choice
        """Parse the file bytes using json."""
        # I don't know of any reason why you would want to use read_text instead of read_bytes for JSON. Unless a
        # specific need arises this function will always just use read_bytes
        return json.loads(self.read_bytes())

    def parsed_cached(self, *, reload: bool = False) -> Any:  # type: ignore # noqa: PGH003, ANN401 - Impossible to know
        # the return type of a loaded json file so in this situation returning Any is the only logical choice
        """Parse the file bytes using json and cache the result."""
        # I don't know of any reason why you would want to use read_text instead of read_bytes for JSON. Unless a
        # specific need arises this function will always just use read_bytes
        if not self.parsed_cached_value or reload:
            self.parsed_cached_value = json.loads(self.read_bytes_cached(reload=reload))

        return self.parsed_cached_value
