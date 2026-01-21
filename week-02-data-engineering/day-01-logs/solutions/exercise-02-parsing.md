# Solution: Exercise 2 - Parsing Regex

### Regex Pattern for Legacy Logs
For the format: `[2024-01-19 20:30:15] AUTH_SUCCESS: user_id=452 ip=10.0.0.42 location="us-east-1"`

**Regex Profile:**
```regex
^\[(?<time>[^\]]+)\] (?<event_type>[^:]+): (?<details>.*)$
```

### Full Fluent Bit Parser (`parsers.conf`)
```ini
[PARSER]
    Name         app_custom_parser
    Format       regex
    Regex        ^\[(?<time>[^\]]+)\] (?<event_type>[^:]+): (?<details>.*)$
    Time_Key     time
    Time_Format  %Y-%m-%d %H:%M:%S
```

### Flattening with KV Filter
To extract `user_id` and `ip` from the `details` field:

```ini
[FILTER]
    Name         kv
    Match        legacy.app
    Key_Name     details
```
