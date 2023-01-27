from io import StringIO
from typing import TextIO

from fakejson.parser import JSONObject, JSONParser


def load(fd: TextIO) -> JSONObject:
    parser = JSONParser(fd)
    return parser.parse()


def loads(json_like: str) -> JSONObject:
    fd = StringIO(json_like)
    parser = JSONParser(fd)
    return parser.parse()
