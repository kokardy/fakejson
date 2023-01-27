import json
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


def dumps(json_obj: JSONObject) -> str:
    buf = StringIO()
    dump(json_obj, buf)
    return buf.getvalue()


def dump(json_obj: JSONObject, fd: TextIO) -> None:
    if json_obj is None:
        fd.write("null")
    elif json_obj is True:
        fd.write("true")
    elif json_obj is False:
        fd.write("false")
    elif isinstance(json_obj, (dict, list)):
        json.dump(json_obj, fd)
    elif isinstance(json_obj, (str,)):
        fd.write(f'"{json_obj}"')
    elif isinstance(json_obj, (int, float)):
        fd.write(f'{json_obj}')

    else:
        raise Exception(f"Unexpected Type {json_obj} is {type(json_obj)}")
