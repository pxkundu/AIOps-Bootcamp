# Solutions: Week 2 Day 5-6 - Time-Series Databases

This directory contains reference solutions for the InfluxDB and TimescaleDB exercises.

## [Exercise 1: InfluxDB 2.x](exercise-01-influx/)
- `ingest_metrics.py`: Complete Python script using `Point` API.
- `queries.flux`: Useful Flux snippets for average windowing.

## [Exercise 2: TimescaleDB](exercise-02-timescale/)
- `generate_traffic.py`: Script to populate the site traffic table.
- `queries.sql`: Analytical SQL queries for downsampling and First/Last state.

## [Exercise 3: VictoriaMetrics](exercise-03-victoriametrics.md)
- Remote write configuration and MetricsQL examples.

## [Project: Multi-Tenant Metrics Aggregator](project-solution/)
- `proxy.py`: FastAPI implementation with routing logic and quota block (429).
- `downsampling.flux`: The influxdb task for long-term storage.
