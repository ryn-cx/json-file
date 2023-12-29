"""Library for working with JSON files."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING

from paved_path import CobblestoneCache, PavedPath

if TYPE_CHECKING:
    from typing import Any, Self

    from paved_path import PathableType


# This is set up as a seperate class to make it easier to clear the cache.
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

    def __new__(cls, *args: PathableType) -> Self:
        """Convert all arguments to Path objects and passes them to the Path constructor."""
        cls.cache = JSONCache()
        return super().__new__(cls, *args)

    def write(self, content: Any, *, write_through: bool = True) -> None:  # noqa: ANN401 - stdlib json is typed as Any
        """Open the file, write to it, close the file, and clear the cache.

        Args:
        ----
            content: The object to be written to the file.
            write_through: If True the cache will be updated to match what is written to the file. If False the cache
            will be cleared. Either way the cache is not allowed to be out of sync with the file, either it matches the
            file or it is None.
        """
        # Strings and bytes are not serialized because no changescan be made on them.
        if isinstance(content, (str, bytes)):
            super().write(content, write_through=write_through)
        # All other objects are serialized using json
        else:
            super().write(json.dumps(content), write_through=write_through)
            if write_through:
                self.cache.parsed = content

    def parsed(self) -> Any:  # type: ignore # noqa: PGH003, ANN401 - Impossible to know the return type of a loaded
        # json file so in this situation returning Any is the only logical choice
        """Read the file bytes and parse the file using json.

        Returns
        -------
            An uncached parsed json object.
        """
        # I don't know of any reason why you would want to use read_text instead of read_bytes for json. Unless a
        # specific need arises this function will always use read_bytes.
        return json.loads(self.read_bytes())

    def parsed_cached(self, *, reload: bool = False) -> Any:  # type: ignore # noqa: PGH003, ANN401 - Impossible to know
        # the return type of a loaded json file so in this situation returning Any is the only logical choice
        """Read the file bytes, parse the file using json, and cache the result.

        Args:
        ----
            reload: If true read the bytes from the file, parse it using json and cache the result even if a
            json object is already cached. If False use the cached json object if it exists otherwise read
            the bytes from the file, parse it using json and cache the result.

        Returns:
        -------
            A cached parsed json object.
        """
        if not self.cache.parsed or reload:
            self.cache.parsed = json.loads(self.read_bytes_cached(reload=reload))

        return self.cache.parsed
