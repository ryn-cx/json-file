"""Class for working with JSON files."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, override

from paved_path import PavedPath

if TYPE_CHECKING:
    from typing import Any

    ParsedJson = Any


class JSONFile(PavedPath):
    """Class for working with JSON files."""

    cached_json: Any = None

    @override
    def clear_cache(self) -> None:
        self.cached_json = None
        return super().clear_cache()

    def write_json(
        self,
        data: dict[Any, Any] | list[Any] | str,
        *,
        write_through: bool = True,
        clear_cache: bool = True,
    ) -> int:
        """Manage cache, open the json file in text mode, read it, and close the file.

        Args:
            data: The data to write to the file.

            write_through: If True write the text to the file and the cache. If
                False write the text to the file and clear out the cache so it
                stays in sync.

            clear_cache: If True clear the cache. If False do not clear the
                cache.

        Returns:
            Passed from self.write_text().
        """
        # If given a string make sure it is valid JSON before writing it.
        if isinstance(data, str):
            data = json.loads(data)

        if clear_cache:
            self.clear_cache()
        if write_through:
            self.cached_json = data

        dumped_json = json.dumps(data)
        read_json = json.loads(dumped_json)
        if read_json != data:
            msg = "Serialization will create an output that is different from the input"
            raise ValueError(msg)

        # Do not clear the cache because it has already been cleared, clearing
        # it again would delete the data that was just added to the cache.
        return self.write_text(
            json.dumps(data),
            write_through=write_through,
            clear_cache=False,
        )

    def read_json(
        self,
        *,
        reload: bool = False,
        check_file: bool = False,
        skip_cache: bool = False,
    ) -> ParsedJson:
        """Read the file in text mode, parse it, and cache the result.

        Args:
            reload: * If True read the text from the file, and cache the text.
                * If False use the cached text if it exists otherwise read the
                text from the file and cache it.

            check_file: If True check if the file is newer than the cache and if
                it is reload it.

            skip_cache: If True do not use the cache at all.

        Returns:
            The cached parsed JSON of the file.
        """
        if skip_cache:
            return json.loads(self.read_text(skip_cache=skip_cache))

        if (
            self.cached_json is None
            or reload
            or (check_file and self.is_up_to_date(self.cache_timestamp))
        ):
            self.cached_json = json.loads(self.read_text(reload=reload))

        return self.cached_json
