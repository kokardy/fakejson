import logging
from enum import Enum
from io import StringIO
from typing import Any, Callable, Final, Generator, Literal, TextIO, TypeAlias

from .exceptions import DocumentEnd, ParseError

# JSONObjcet: TypeAlias = int | float | str | None | bool | list["JSONObjcet"] | dict[str, "JSONObjcet"]
JSONObject: TypeAlias = int | float | str | None | bool | list[Any] | dict[str, Any]


literal_true: Final = "true"
literal_false: Final = "false"
literal_null: Final = "null"

logger = logging.getLogger(__name__)


def debug(*args: Any) -> None:
    logger.debug(" ".join(str(arg) for arg in args))


def create_seq() -> Callable[[], Generator[int, None, None]]:
    def _seq() -> Generator[int, None, None]:
        i = 0
        while True:
            yield i
            i += 1

    return _seq


event_seq = create_seq()


class Event(Enum):
    DocumentStart = event_seq()
    DocumentEnd = event_seq()
    StringStart = event_seq()
    StringEnd = event_seq()
    ObjectStart = event_seq()
    ObjectEnd = event_seq()
    ArrayStart = event_seq()
    ArrayEnd = event_seq()
    LiteralStart = event_seq()
    LiteralEnd = event_seq()


spaces = set([" ", "\t", "\n", "\r"])
quotes = set(['"', "'"])


class JSONParser:
    """Bad-quote-json reader

    Attributes:
        buf: TextIO
        pos: current position
    """

    buf: TextIO
    pos: int
    nest: int

    def __init__(self, buf: TextIO):
        self.buf = buf
        self.pos = 0
        self.nest = 0

    def parse(self) -> JSONObject:
        debug(Event.DocumentStart)

        result = self.parse_something()

        try:
            _ = self.skip_spaces()
            raise ParseError("unexpected characters exists in later")
        except DocumentEnd:
            debug(Event.DocumentEnd, f"{result=}")
            return result
        except Exception as e:
            raise e

    def parse_something(self) -> JSONObject:

        first_char = self.skip_spaces()
        debug(f"{first_char=}")
        result: JSONObject
        if first_char == "{":
            debug("detect object")
            result = self.parse_object()
        elif first_char == "[":
            debug("detect array")
            result = self.parse_array()
        elif first_char in quotes:
            debug("detect string")
            result = self.parse_string()
        else:
            debug("guess literal")
            result = self.parse_literal(first_char)

        return result

    def parse_object(self) -> dict[str, JSONObject]:
        """parse json object {sothimeng}"""
        result: dict[str, Any] = dict()
        _ = self.next_char()  # {
        debug(Event.ObjectStart)
        try:
            while True:
                next_char = self.skip_spaces()

                key = self.parse_string()
                logging.debug(f"{key=}")
                collon_expected = self.skip_spaces()
                if collon_expected == ":":
                    logging.debug("find colon")
                    self.next_char()
                else:
                    raise ParseError("Collon expected")
                _ = self.skip_spaces()
                value = self.parse_something()
                logging.debug(f"{value=}")

                if key in result:
                    raise ParseError(f"same key registered: {key}")

                result[key] = value

                next_char = self.skip_spaces()
                if next_char == ",":
                    self.next_char()
                    continue
                elif next_char == "}":
                    self.next_char()
                    break

                raise ParseError("parse error")
            debug(Event.ObjectEnd, f"{result=}")
            return result
        except DocumentEnd:
            raise ParseError("Document ends unless closing array")

    def parse_array(self) -> list[JSONObject]:
        """parse json array"""
        debug(Event.ArrayStart)
        result: list[JSONObject] = list()
        _ = self.next_char()  # [
        try:
            while True:
                result.append(self.parse_something())

                first_char = self.skip_spaces()
                if first_char == ",":
                    self.next_char()
                    continue
                elif first_char == "]":
                    self.next_char()
                    break

                raise ParseError("parse error")

            debug(Event.ArrayEnd, f"{result=}")
            return result
        except DocumentEnd:
            raise ParseError("Document ends unless closing array")

    def parse_string(self) -> str:
        """parse json string"""
        debug(Event.StringStart)
        buf = StringIO()
        escaping = False
        quote = self.next_char()
        while char := self.next_char():
            # string end
            if not escaping and char == quote:
                break

            buf.write(char)

            # escape
            if not escaping and char == "\\":
                escaping = True
            else:
                escaping = False
        result = buf.getvalue()
        result = result.replace("\\t", "\t")
        result = result.replace("\\n", "\n")
        result = result.replace("\\r", "\r")
        result = result.replace("\\b", "\b")
        result = result.replace('\\"', '"')
        result = result.replace("\\'", "'")
        debug(Event.StringEnd, f"{result=}")
        return result

    def parse_literal(self, first_char: str) -> bool | None | int | float:
        """parse json literal

        Args:
            first_char: first character

        """
        # TODO number

        debug(Event.LiteralStart)

        result: bool | None
        if first_char == "t":
            result = self.parse_true()
        elif first_char == "f":
            result = self.parse_false()
        elif first_char == "n":
            self.parse_null()
            # it's successfully parsed, return None
            # otherwise raise ParseError
            return None
        else:
            result = self.parse_number()
        debug(Event.LiteralEnd, f"{result=}")
        return result

    def parse_number(self) -> int | float:
        """parse number literal"""
        buf = StringIO()
        while True:
            char = self.next_char()
            if char in "-0123456789e.":
                buf.write(char)
            else:
                self.pos -= 1
                self.buf.seek(self.pos)
                break

        result_str = buf.getvalue()
        if "." in result_str or "e" in result_str:
            result = float(result_str)
        else:
            result = int(result_str)

        return result

    def parse_null(self) -> None:
        """parse null literal"""
        buf = StringIO()
        for _ in range(4):
            char = self.next_char()
            buf.write(char)

        if buf.getvalue() == literal_null:
            return None
        else:
            raise ParseError("Literal parse error")

    def parse_true(self) -> Literal[True]:
        """parse true literal"""
        buf = StringIO()
        for _ in range(4):
            char = self.next_char()
            buf.write(char)

        if buf.getvalue() == literal_true:
            return True
        else:
            raise ParseError("Literal parse error")

    def parse_false(self) -> Literal[False]:
        """parse false literal"""
        buf = StringIO()
        for _ in range(5):
            char = self.next_char()
            buf.write(char)

        if buf.getvalue() == literal_false:
            return False
        else:
            raise ParseError("Literal parse error")

    def skip_spaces(self) -> str:
        char = ""
        while True:
            char = self.next_char()
            if char in spaces:
                continue
            else:
                break
        self.pos -= 1
        self.buf.seek(self.pos)

        return char

    def next_char(self) -> str:
        if char := self.buf.read(1):
            self.pos += 1
            return char

        raise DocumentEnd("END")
