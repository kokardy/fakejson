import json
import logging
import os
from typing import Any, Callable

from fakejson.parser.parser import JSONParser

logger = logging.getLogger()


class TestStrictJSON:
    def setup_method(self, method: Callable[[Any], Any]) -> None:
        logger.info(method.__name__)

    def get_path(self, filename: str) -> str:
        return os.path.join(os.path.dirname(__file__), "data", "strict", filename)

    def _test_file(self, filename: str) -> None:
        file_path = self.get_path(filename)
        with open(file_path) as fd:
            expected = json.load(fd)

        with open(file_path) as fd:
            json_reader = JSONParser(fd)
            result = json_reader.parse()

        assert result == expected

    def test_simple(self) -> None:
        self._test_file("simple.json")

    def test_complex(self) -> None:
        self._test_file("complex.json")

    def test_list(self) -> None:
        self._test_file("list.json")
