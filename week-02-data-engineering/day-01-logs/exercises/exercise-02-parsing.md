# Exercise 02: The Parser Challenge (Unstructured to Structured)

## 🎯 Objective
Master the art of transforming "human-readable" legary logs into "machine-ready" JSON using Fluent Bit's Parser engine. This is a critical skill for AIOps, as AI models cannot process raw strings efficiently.

---

## 🛠️ Step 1: The Raw Data
Your mission is to parse the following types of legacy logs. Create a file named `legacy-apps.log` and paste these lines:

```syslog
[2024-01-19 20:30:15] AUTH_SUCCESS: user_id=452 ip=10.0.0.42 location="us-east-1"
[2024-01-19 20:30:17] API_ERROR: path="/v1/payment" code=500 latency=1542ms message="Connection timeout"
[2024-01-19 20:30:20] DB_QUERY: query="SELECT * FROM users" duration=15ms status=OK
```

---

## 📝 Step 2: Designing the Regex Parser
AIOps requires precision. We will use Named Capture Groups in Regex to define our fields.

1. **Test your regex:** Go to [Regex101.com](https://regex101.com/) (select PCRE flavor).
2. **Draft a pattern:** Try to capture `timestamp`, `log_level`, and any key-pair values.

**Hints for key-value parsing:**
`?(<key>[^=]+)=(?<value>[^\s]+)`

---

## ⚙️ Step 3: Fluent Bit Parser Config
Create a file named `parsers.conf`:

```ini
[PARSER]
    Name         app_custom_parser
    Format       regex
    Regex        ^\[(?<time>[^\]]+)\] (?<event_type>[^:]+): (?<details>.*)$
    Time_Key     time
    Time_Format  %Y-%m-%d %H:%M:%S
```

Create/Update your `fluent-bit.conf` to use this parser:

```ini
[SERVICE]
    Parsers_File parsers.conf

[INPUT]
    Name         tail
    Path         ./legacy-apps.log
    Parser       app_custom_parser
    Tag          legacy.app

[FILTER]
    Name         record_modifier
    Match        legacy.app
    Record       source_type legacy_migration

[OUTPUT]
    Name         stdout
    Match        *
    Format       json_lines
```

---

## 🚀 Step 4: Run and Verify
1. Run Fluent Bit (either locally or via Docker mapping these files).
2. Observe the output. 

**Is it structured?** 
- It should look like this: 
  `{"time":1705696215,"event_type":"AUTH_SUCCESS","details":"user_id=452 ip=10.0.0.42 location=\"us-east-1\"","source_type":"legacy_migration"}`

---

## 🧪 Advanced Challenge: Nested Key-Value Extraction
The `details` field is still a string! In AIOps, we want `user_id` and `ip` to be top-level JSON fields.

**Task:**
1. Research the [Fluent Bit Key-Value Filter](https://docs.fluentbit.io/manual/pipeline/filters/kv).
2. Add a filter to your config that parses the `details` string into real JSON keys.
3. **Verify:** You should see `{"user_id": "452", "ip": "10.0.0.42" ...}` in the final output.

## ✅ Deliverable
Show your final `parsers.conf` and `fluent-bit.conf` that produces a fully flattened JSON object for all three log samples.
