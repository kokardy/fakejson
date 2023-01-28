# fakejson

JSON-like format parser in Python

## Supported formats
- JSON format

    Use either json.loads or json.load from the standard library to parse JSON data.

- JSON-like format: available single quote as string literal and object key

    If you want to parse a JSON-like string that does not contain the values null, true, or false, it is recommended to use the ast.literal_eval() function.

## Usage

```sh
pip install fekejson
```

```python

import fakejson

# bad quote json (single quote exists.)
json_like_str = """
{
    "key1": "value1",
    'key2': 'value2',
}
"""

parsed = fakejson.loads(json_like_str) # dict

assert parsed["key1"] == "value1"
assert parsed["key2"] == "value2"

json_str = fakejson.dumps(parsed)

print(json_str) # {"key1":"value1","key2":"value2"}

```
