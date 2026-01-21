# Solution: Exercise 2 - LogQL Mastery

### Task 1: Basic Search
Find all logs containing "error" but excluding "timeout".
```logql
{job="varlogs"} |= "error" != "timeout"
```

### Task 2: Regex Extraction
Extract `user_id` from: `User 123 logged out`.
```logql
{job="varlogs"} | regexp "User (?P<user_id>\\d+) logged out"
```

### Task 3: Converting Logs to Metrics
1. **Error Count per minute:**
```logql
sum by (job) (count_over_time({job="varlogs"} |= "error" [1m]))
```

2. **Average Latency (from JSON logs):**
Assuming the log is `{"latency": 150, ...}`.
```logql
avg_over_time({job="v1"} | json | unwrap latency [5m])
```

3. **95th Percentile Latency (AIOps common metric):**
```logql
quantile_over_time(0.95, {job="v1"} | json | unwrap latency [5m])
```
