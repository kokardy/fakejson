import json
import logging
from typing import Any, Callable

import fakejson

logger = logging.getLogger()


class TestFunction:
    def setup_method(self, method: Callable[[Any], Any]) -> None:
        logger.info(method.__name__)

    def test_loads_and_dumps_dict(self) -> None:
        expected = """{"key1": "value1", 'key2': 'value2'}"""
        result1 = fakejson.loads(expected)
        assert isinstance(result1, (dict,))
        assert result1["key1"] == "value1"
        assert result1["key2"] == "value2"

        json_str = fakejson.dumps(result1)
        result2 = json.loads(json_str)
        assert result1 == result2

    def test_loads_and_dumps_list(self) -> None:
        expected = """["ABCD" , 'abcd', 1234, -123, 1.2, -1.2, true , false , null]"""
        result1 = fakejson.loads(expected)
        assert isinstance(result1, (list,))
        assert result1[0] == "ABCD"
        assert result1[1] == "abcd"
        assert result1[2] == 1234
        assert result1[3] == -123
        assert result1[4] == 1.2
        assert result1[5] == -1.2
        assert result1[6] is True
        assert result1[7] is False
        assert result1[8] is None

        json_str = fakejson.dumps(result1)
        result2 = json.loads(json_str)
        assert result1 == result2

    def test_loads_str(self) -> None:
        expected = "ABCDEFG"
        result = fakejson.loads(f'"{expected}"')
        assert result == expected

    def test_dumps_str(self) -> None:
        expected = "ABCDEFG"
        result = fakejson.dumps(expected)
        assert result == f'"{expected}"'

    def test_loads_bool(self) -> None:
        params = {"true": True, "false": False}
        for input_str, expected in params.items():
            result = fakejson.loads(f"{input_str}")
            assert result == expected

    def test_dumps_bool(self) -> None:
        params = {"true": True, "false": False}
        for expected, input_obj in params.items():
            result = fakejson.dumps(input_obj)
            assert result == expected

    def test_loads_int(self) -> None:
        params = [123456, -98765]
        for expected in params:
            result = fakejson.loads(f"{expected}")
            assert result == expected

    def test_dumps_int(self) -> None:
        params = [123456, -98765]
        for expected in params:
            result = fakejson.dumps(expected)
            assert result == f"{expected}"

    def test_loads_float(self) -> None:
        params = [
            13.03e6,
            -12.56e-3,
            1.2432,
            -1.2432,
        ]
        for expected in params:
            result = fakejson.loads(f"{expected}")
            assert result == expected

    def test_dumps_float(self) -> None:
        params = [
            13.03e6,
            -12.56e-3,
            1.2432,
            -1.2432,
        ]
        for expected in params:
            result = fakejson.dumps(expected)
            assert result == f"{expected}"
