# Exercise 02: Analytical SQL with TimescaleDB

## 🎯 Objective
Learn how to use SQL for time-series analysis by converting a standard PostgreSQL table into a high-performance "Hypertable."

---

## 🛠️ Step 1: Deploying TimescaleDB

Update your `docker-compose.yml` to add TimescaleDB:

```yaml
  timescaledb:
    image: timescale/timescaledb:latest-pg14
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_PASSWORD=adminpassword
```

Start the service:
```bash
docker-compose up -d timescaledb
```

---

## 🐘 Step 2: Creating a Hypertable

Connect to the database (using `psql` or a tool like DBeaver):
```bash
docker exec -it $(docker ps -qf name=timescaledb) psql -U postgres
```

Run these SQL commands:
```sql
-- 1. Create a standard table
CREATE TABLE site_traffic (
  time        TIMESTAMPTZ       NOT NULL,
  site_id     INT               NOT NULL,
  visits      INT               DEFAULT 0,
  latency_ms  DOUBLE PRECISION  DEFAULT 0
);

-- 2. Turn it into a Hypertable (Chunks data by time)
SELECT create_hypertable('site_traffic', 'time');
```

---

## 📝 Step 3: Injecting Sample Data

Create `generate_traffic.py`:
```python
import psycopg2
import random
from datetime import datetime, timedelta

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=adminpassword")
cur = conn.cursor()

start_time = datetime.now() - timedelta(days=1)

print("Injecting 24 hours of data...")
for i in range(1440): # 1440 minutes in a day
    cur.execute(
        "INSERT INTO site_traffic (time, site_id, visits, latency_ms) VALUES (%s, %s, %s, %s)",
        (start_time + timedelta(minutes=i), random.randint(1, 4), random.randint(100, 500), random.uniform(50, 500))
    )

conn.commit()
cur.close()
conn.close()
print("Done!")
```

---

## 🔍 Step 4: Analytical Queries

Run these in your SQL console:

### Task 1: 5-Minute Rollups (Downsampling)
```sql
SELECT
  time_bucket('5 minutes', time) AS five_min,
  avg(latency_ms) AS avg_latency
FROM site_traffic
GROUP BY five_min
ORDER BY five_min DESC
LIMIT 10;
```

### Task 2: Comparative Analysis
Calculate the total visits for Site 1 vs Site 2 in the last hour.
```sql
SELECT
  site_id,
  sum(visits)
FROM site_traffic
WHERE time > now() - INTERVAL '1 hour'
GROUP BY site_id;
```

### Task 3: Performance Check (First and Last)
Identify the first and last recorded latency for each site.
```sql
SELECT 
  site_id, 
  first(latency_ms, time), 
  last(latency_ms, time) 
FROM site_traffic 
GROUP BY site_id;
```

---

## 🧪 Challenge Question
TimescaleDB uses "chunks" under the hood. Run `SELECT * FROM timescaledb_information.chunks;`. How many chunks did your 24-hour injection create? Why does this help with performance compared to one massive table?

---

## ✅ Submission
Submit your SQL query results for Task 1 showing at least 10 rows of 5-minute averaged latency.
