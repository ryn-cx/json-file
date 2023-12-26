"""Library for working with JSON files."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING

from paved_path import CobblestoneCache, PavedPath

if TYPE_CHECKING:
    from typing import Any

    from paved_path import PathableType


class JSONCache(CobblestoneCache):
    """Cache for JSONFile.

    This is set up as a seperate class to make it easier to clear the cache.
    """

    def __init__(self) -> None:
        """Initialize the cache with None values."""
        self.parsed = None
        super().__init__()


class JSONFile(PavedPath):
    """Library for working with JSON files."""

    def __init__(self, *_args: PathableType) -> None:
        """Initialize the JSONFile class.

        Args:
        ----
            _args: The path fragments to join together.
        """
        self.cache = JSONCache()

    def write(self, content: Any, *, write_through: bool = True) -> None:  # noqa: ANN401 - stdlib json is typed as Any
        """Write an object to the file using json.

        Args:
        ----
            content: The object to be written to the file.
            write_through: Whether to write through the cache.
        """
        # Strings and bytes are not serialized because no changescan be made on them.
        if isinstance(content, (str, bytes)):
            super().write(content, write_through=write_through)
        # All other objects are serialized using json
        else:
            super().write(json.dumps(content), write_through=write_through)
            if write_through:
                self.cache.parsed = content

    def parsed(self) -> Any:  # type: ignore # noqa: PGH003, ANN401 - Impossible to know thereturn type of a loaded json
        # file so in this situation returning Any is the only logical choice
        """Parse the file bytes using json.

        Returns
        -------
            An uncached parsed JSON object.
        """
        # I don't know of any reason why you would want to use read_text instead of read_bytes for JSON. Unless a
        # specific need arises this function will always just use read_bytes
        return json.loads(self.read_bytes())

    def parsed_cached(self, *, reload: bool = False) -> Any:  # type: ignore # noqa: PGH003, ANN401 - Impossible to know
        # the return type of a loaded json file so in this situation returning Any is the only logical choice
        """Parse the file bytes using json and cache the result.

        Args:
        ----
            reload: Whether to reload the file bytes and reparse the file.

        Returns:
        -------
            A cached parsed JSON object.
        """
        # I don't know of any reason why you would want to use read_text instead of read_bytes for JSON. Unless a
        # specific need arises this function will always just use read_bytes
        if not self.cache.parsed or reload:
            self.cache.parsed = json.loads(self.read_bytes_cached(reload=reload))

        return self.cache.parsed
