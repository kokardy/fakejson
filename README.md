# fakejson

JSON-like format parser in Python

## Usage

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
