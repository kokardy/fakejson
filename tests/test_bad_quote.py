import ast
import json
import logging
import os
from typing import Any, Callable

from fakejson.parser.parser import JSONParser

logger = logging.getLogger()


class TestBadQuoteJSON:
    def setup_method(self, method: Callable[[Any], Any]) -> None:
        logger.info(method.__name__)

    def get_path(self, filename: str) -> str:
        return os.path.join(os.path.dirname(__file__), "data", "bad_quote", filename)

    def _test_file_without_single_quote(self, filename: str) -> None:
        file_path = self.get_path(filename)
        with open(file_path) as fd:
            json_str = fd.read().replace("'", '"')
            expected = json.loads(json_str)

        with open(file_path) as fd:
            json_reader = JSONParser(fd)
            result = json_reader.parse()

        assert result == expected

    def _test_file_without_null_and_bool(self, filename: str) -> None:
        file_path = self.get_path(filename)
        with open(file_path) as fd:
            expected = ast.literal_eval(fd.read())

        with open(file_path) as fd:
            json_reader = JSONParser(fd)
            result = json_reader.parse()

        assert result == expected

    def test_simple(self) -> None:
        self._test_file_without_single_quote("simple.json")

    def test_complex(self) -> None:
        self._test_file_without_single_quote("complex.json")

    def test_single_quote(self) -> None:
        self._test_file_without_null_and_bool("single_quote.json")

    def test_string(self) -> None:
        self._test_file_without_null_and_bool("string.json")

    def test_list(self) -> None:
        self._test_file_without_null_and_bool("list.json")
