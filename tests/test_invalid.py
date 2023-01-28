import logging
import os
from typing import Any, Callable

import pytest

from fakejson.parser.parser import JSONParser, ParseError

logger = logging.getLogger()


class TestInvalidJSON:
    def setup_method(self, method: Callable[[Any], Any]) -> None:
        logger.info(method.__name__)

    def get_path(self, filename: str) -> str:
        return os.path.join(os.path.dirname(__file__), "data", "invalid", filename)

    def test_simple(self):
        files = [
                "unclosed_object.json",
                "unclosed_array.json",
                "unclosed_string.json",
                ]
        for file_name in files:
            file_path = self.get_path(file_name)

            with (pytest.raises(ParseError) as e, open(file_path) as fp):
                parser = JSONParser(fp)
                _ = parser.parse()
            logger.debug(f"{file_name=} expected error occurred: {e}")
