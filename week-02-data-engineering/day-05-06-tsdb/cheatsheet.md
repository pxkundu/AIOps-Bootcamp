# TSDB Cheat Sheet: InfluxDB (Flux) & TimescaleDB (SQL)

> Master the languages of time-series data storage and analysis.

---

## 🌊 InfluxDB: The Flux Language
Flux is a functional, data-pipe language.

### Basic Query
```js
from(bucket: "aiops_bucket")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu")
  |> filter(fn: (r) => r.host == "server-01")
```

### Aggregation (Windowing)
```js
from(bucket: "aiops_bucket")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "mem")
  |> aggregateWindow(every: 5m, fn: mean, createEmpty: false)
  |> yield(name: "mean_usage")
```

### Anomaly Detection (Fill Missing Data)
```js
  |> interpolate.linear(every: 1m) // Fill gaps for ML models
```

---

## 🐘 TimescaleDB: SQL for Time-Series
Standard SQL with specialized 'Hyperfunctions'.

### Create a Hypertable
```sql
CREATE TABLE sensor_data (
  time        TIMESTAMPTZ       NOT NULL,
  sensor_id   INTEGER           NOT NULL,
  temperature DOUBLE PRECISION  NULL
);

SELECT create_hypertable('sensor_data', 'time');
```

### Time-Bucket Aggregation (SQL equivalent of aggregateWindow)
```sql
SELECT
  time_bucket('5 minutes', time) AS five_min,
  avg(temperature) AS avg_temp
FROM sensor_data
WHERE time > now() - INTERVAL '24 hours'
GROUP BY five_min
ORDER BY five_min DESC;
```

### Advanced: First & Last (State Tracking)
```sql
SELECT 
  sensor_id,
  last(temperature, time), -- Get most recent reading
  first(temperature, time) -- Get first reading in window
FROM sensor_data
GROUP BY sensor_id;
```

---

## 🏎️ Performance Tuning Reference

### InfluxDB 2.x Optimization
- **Bucket Retention:** `influx bucket update -n my_bucket -r 7d`
- **Sharding:** Use a `shard-group-duration` that matches your query lookback window.
- **Batch Size:** Aim for **5000-10,000** points per write for optimal throughput.

### TimescaleDB Optimization
- **Compression:**
```sql
ALTER TABLE sensor_data SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'sensor_id'
);
SELECT add_compression_policy('sensor_data', INTERVAL '7 days');
```
- **Chunk Size:** Target chunk sizes that fit in roughly 25% of your available RAM.

---

## 🔍 TSDB Comparison at a Glance

| Feature | InfluxDB | TimescaleDB |
|---------|----------|-------------|
| **Join Support** | Limited (Flux only) | **Full SQL Joins** |
| **Ingestion** | **Ultra-High** | High (Relational overhead) |
| **Ecosystem** | Telegraf / Kapacitor | **Entire PostgreSQL ecosystem** |
| **Query Learning** | New language (Flux) | Familiar SQL |
| **Storage** | Highly optimized TSM | PostgreSQL storage + Compression |

---

## 💡 AIOps Insight: Schema-on-Write
Always use **Tags** for things you use in WHERE clauses (region, host, env) and **Fields** for the numbers you want to average or sum. Combining them into tags will cause **Series Explosion** (Cardinality issues).
