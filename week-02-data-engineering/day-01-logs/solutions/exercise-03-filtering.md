# Solution: Exercise 3 - Masking & Sampling

### `mask.lua`
```lua
function mask_acc(tag, timestamp, record)
    -- Mask account number if present
    if record["acc"] ~= nil then
        -- Keep first 2 chars, mask rest
        record["acc"] = string.sub(record["acc"], 1, 2) .. "********"
    end
    
    -- Example: Add processing metadata
    record["processed_by"] = "fluent-bit-lua"
    
    return 1, timestamp, record
end
```

### `fluent-bit.conf` (Sampling Logic)
```ini
[SERVICE]
    Flush        1
    Parsers_File parsers.conf

[INPUT]
    Name         tail
    Path         ./finance.log
    Tag          finance.raw

# 1. Masking via Lua
[FILTER]
    Name    lua
    Match   finance.*
    script  mask.lua
    call    mask_acc

# 2. Adaptive Sampling: Keep 100% of ERROR, 10% of DEBUG
# We use rewrite_tag to send DEBUG to a separate tag then sample it.

[FILTER]
    Name          rewrite_tag
    Match         finance.raw
    Rule          $level ^(DEBUG)$  finance.debug  false
    Rule          $level ^(ERROR|INFO)$  finance.keep   true

[FILTER]
    Name          random
    Match         finance.debug
    Samples       10  # Keep 10%

[OUTPUT]
    Name          stdout
    Match         finance.*
```
