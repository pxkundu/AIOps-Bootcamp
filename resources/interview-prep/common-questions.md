# AIOps Interview Questions

50+ common questions for AIOps engineering roles.

---

## 1. Fundamentals (10 Questions)

### Q1: What is AIOps and how does it differ from traditional monitoring?
**Key Points:**
- AIOps = AI for IT Operations
- Uses ML/AI to automate operational tasks
- Goes beyond threshold-based alerting
- Enables predictive, not just reactive, operations

### Q2: Explain the three pillars of observability.
**Key Points:**
- **Metrics**: Numeric measurements over time (CPU, memory, latency)
- **Logs**: Discrete events with context
- **Traces**: Request flow through distributed systems
- Together they provide complete system visibility

### Q3: What is MTTD and MTTR? How does AIOps improve them?
**Key Points:**
- MTTD = Mean Time To Detect
- MTTR = Mean Time To Resolve
- AIOps reduces MTTD through automated anomaly detection
- Reduces MTTR via RCA and auto-remediation

### Q4: Describe the AIOps pipeline.
**Key Points:**
- Data Collection → Aggregation → Analysis → Correlation → Action
- Ingest from multiple sources
- Normalize and enrich data
- Apply ML for pattern detection
- Automate responses

### Q5: What's the difference between monitoring and observability?
**Key Points:**
- Monitoring: Checking known issues (predefined metrics/alerts)
- Observability: Understanding unknown issues (exploratory)
- Observability enables asking new questions without new instrumentation

### Q6: How do you handle alert fatigue?
**Key Points:**
- Alert correlation and suppression
- Dynamic thresholds instead of static
- Alert severity classification with ML
- Proper runbook documentation

### Q7: What is OpenTelemetry and why is it important?
**Key Points:**
- Vendor-neutral observability framework
- Unified API for metrics, logs, traces
- Avoids lock-in
- Industry standard for instrumentation

### Q8: Explain event correlation in AIOps.
**Key Points:**
- Grouping related events to reduce noise
- Temporal correlation (same timeframe)
- Topological correlation (related services)
- Helps identify root cause faster

### Q9: What's the role of topology awareness in AIOps?
**Key Points:**
- Understanding service dependencies
- Propagating alerts through dependency graph
- Identifying blast radius
- Enabling precise root cause analysis

### Q10: How do you evaluate an AIOps tool?
**Key Points:**
- Data integration capabilities
- ML model quality and explainability
- Automation options
- Customization flexibility
- Total cost of ownership

---

## 2. Machine Learning (15 Questions)

### Q11: What ML techniques are used for anomaly detection?
**Key Points:**
- Supervised: Random Forest, XGBoost (labeled data)
- Unsupervised: Isolation Forest, DBSCAN, Autoencoders
- Statistical: Z-score, IQR, EWMA
- Deep Learning: LSTM, Transformers

### Q12: When would you use supervised vs unsupervised learning?
**Key Points:**
- Supervised: When you have labeled historical incidents
- Unsupervised: For detecting novel/unknown anomalies
- Often combine both in production

### Q13: Explain Isolation Forest algorithm.
**Key Points:**
- Ensemble of random trees
- Anomalies isolated with fewer splits
- No assumptions about data distribution
- Efficient for high-dimensional data

### Q14: How do you handle imbalanced data in incident prediction?
**Key Points:**
- Oversampling minority class (SMOTE)
- Undersampling majority class
- Class weights in model
- Precision-Recall metrics instead of accuracy

### Q15: What is concept drift and how do you handle it?
**Key Points:**
- Model performance degrades as data patterns change
- Monitor model metrics in production
- Regular retraining schedules
- Automated drift detection

### Q16: Explain precision, recall, and F1-score in AIOps context.
**Key Points:**
- Precision: Of predicted anomalies, how many are real? (avoid false positives)
- Recall: Of real anomalies, how many did we catch? (avoid false negatives)
- F1: Harmonic mean, balance both
- In AIOps, high recall often more important (don't miss incidents)

### Q17: How would you build a log classification system?
**Key Points:**
- Parse logs into structured format
- Feature extraction (TF-IDF, embeddings)
- Train classifier (severity, category)
- Evaluate with stratified cross-validation

### Q18: What is time-series forecasting used for in AIOps?
**Key Points:**
- Capacity planning
- SLA breach prediction
- Anomaly detection (compare actual vs forecast)
- Resource scaling decisions

### Q19: Explain ARIMA vs Prophet for forecasting.
**Key Points:**
- ARIMA: Statistical, requires stationarity, manual parameter tuning
- Prophet: Additive model, handles seasonality automatically, more robust
- Prophet better for ops data with multiple seasonalities

### Q20: How do you detect anomalies in real-time?
**Key Points:**
- Stream processing (Kafka, Flink)
- Online learning models
- Sliding window statistics
- Trade-off between latency and accuracy

### Q21: What is root cause analysis in AIOps?
**Key Points:**
- Identifying the underlying cause of incidents
- Uses causality models, not just correlation
- Topology-aware analysis
- Often combines multiple signals

### Q22: How do you validate an anomaly detection model?
**Key Points:**
- Historical labeled data (if available)
- Inject synthetic anomalies
- Time-based cross-validation
- A/B testing in production

### Q23: What are autoencoders and how are they used for anomaly detection?
**Key Points:**
- Neural network that learns compressed representation
- Trained on normal data
- High reconstruction error = anomaly
- Good for complex, high-dimensional data

### Q24: How do you handle seasonality in metrics?
**Key Points:**
- Decomposition (trend, seasonal, residual)
- Seasonal ARIMA (SARIMA)
- Prophet's built-in seasonality handling
- Compare against same hour/day/week

### Q25: What's the difference between statistical and ML anomaly detection?
**Key Points:**
- Statistical: Simpler, interpretable, requires assumptions
- ML: Handles complex patterns, less interpretable
- Statistical good for simple cases, ML for complex

---

## 3. System Design (10 Questions)

### Q26: Design an alerting system that minimizes noise.
**Key Points:**
- Multi-stage pipeline: Collection → Correlation → Classification → Routing
- Dynamic thresholds with ML
- Alert correlation engine
- Severity prediction
- On-call routing with escalation

### Q27: How would you design a log analytics platform?
**Key Points:**
- Collection: Fluentd/Filebeat agents
- Transport: Kafka for buffering
- Storage: Elasticsearch/ClickHouse
- Processing: Drain3 for parsing, ML for classification
- Query: Kibana/Grafana for visualization

### Q28: Design an auto-remediation system.
**Key Points:**
- Incident detection triggers
- Runbook selection (rule-based or ML)
- Safe execution with rollback
- Human-in-loop for critical actions
- Audit logging

### Q29: How would you scale a metrics collection system?
**Key Points:**
- Remote write to central store
- Horizontal sharding by tenant/service
- Push vs pull trade-offs
- Aggregation at edge
- Long-term storage tiering

### Q30: Design a system to predict SLA breaches.
**Key Points:**
- Define SLA metrics (latency P99, error rate)
- Collect relevant features
- Train regression/classification model
- Real-time scoring pipeline
- Alert before breach threshold

### Q31: How do you implement distributed tracing at scale?
**Key Points:**
- OpenTelemetry instrumentation
- Sampling strategies (head-based, tail-based)
- Trace storage (Jaeger, Tempo)
- Service dependency mapping
- Trace-to-log correlation

### Q32: Design a ChatOps bot for incident management.
**Key Points:**
- Slack/Teams integration
- Natural language understanding
- Action execution framework
- Access control and audit
- Integration with runbooks

### Q33: How would you build a capacity forecasting system?
**Key Points:**
- Historical usage data collection
- Multi-variate time-series analysis
- Forecast multiple resources
- Scenario planning (what-if)
- Integration with provisioning

### Q34: Design a multi-cloud observability platform.
**Key Points:**
- Unified data model across clouds
- Cloud-native integrations (CloudWatch, Stackdriver)
- Central correlation engine
- Cost-aware data retention
- Consistent dashboards

### Q35: How do you implement feature stores for AIOps?
**Key Points:**
- Real-time feature computation
- Historical feature retrieval (training)
- Feature versioning
- Low-latency serving
- Integration with ML pipeline

---

## 4. Tools & Technologies (10 Questions)

### Q36: Compare Prometheus vs InfluxDB.
**Key Points:**
- Prometheus: Pull-based, PromQL, better for Kubernetes
- InfluxDB: Push-based, Flux/SQL, more flexible data model
- Prometheus for cloud-native, InfluxDB for broader use cases

### Q37: When would you use Elasticsearch vs Loki?
**Key Points:**
- Elasticsearch: Full-text search, complex queries, more features
- Loki: Simpler, cheaper, Grafana-native, label-based
- Elasticsearch for compliance, Loki for cloud-native scale

### Q38: Explain Grafana's role in observability.
**Key Points:**
- Unified visualization layer
- Multi-source dashboards
- Alerting capabilities
- Exploration tools
- Ecosystem integrations

### Q39: How does Kubernetes HPA relate to AIOps?
**Key Points:**
- Horizontal Pod Autoscaler for resource management
- Custom metrics scaling
- AIOps can enhance with predictive scaling
- Proactive instead of reactive

### Q40: What is MLflow used for?
**Key Points:**
- Experiment tracking
- Model versioning
- Model registry
- Deployment management
- Essential for ML lifecycle in AIOps

### Q41: Explain service mesh observability.
**Key Points:**
- Built-in metrics, logs, traces
- Automatic mTLS
- Traffic management
- Examples: Istio, Linkerd
- Reduces instrumentation burden

### Q42: When would you use streaming vs batch processing for AIOps?
**Key Points:**
- Streaming: Real-time detection, immediate actions
- Batch: Training models, trend analysis
- Often need both in production

### Q43: What are custom Prometheus exporters?
**Key Points:**
- Expose application-specific metrics
- Written in any language
- HTTP endpoint with metrics format
- Bridges gap with custom systems

### Q44: How do PagerDuty/Opsgenie fit in AIOps?
**Key Points:**
- Incident management platforms
- On-call scheduling and escalation
- Integration with monitoring tools
- AIOps enriches alerts before routing

### Q45: Explain chaos engineering in context of AIOps.
**Key Points:**
- Intentionally inject failures
- Tests system resilience
- Validates detection and remediation
- Tools: Chaos Monkey, Litmus

---

## 5. Scenario-Based (5 Questions)

### Q46: You're seeing 10,000 alerts per day. How do you address this?
**Approach:**
1. Analyze alert distribution and false positive rate
2. Implement alert correlation to group related alerts
3. Add dynamic thresholds for noisy metrics
4. Build severity classifier
5. Create runbooks for top alert types
6. Measure improvement in alert-to-incident ratio

### Q47: CPU usage is spiking unpredictably. How do you investigate?
**Approach:**
1. Check metrics for patterns (time of day, specific processes)
2. Correlate with deployments, traffic spikes
3. Analyze logs during spike periods
4. Check for resource leaks
5. Review traces for slow operations
6. Consider load testing to reproduce

### Q48: Build an AIOps solution for a greenfield project.
**Approach:**
1. Start with OpenTelemetry instrumentation
2. Set up Prometheus + Grafana for metrics
3. Implement structured logging with correlation IDs
4. Add distributed tracing
5. Build data pipeline for ML
6. Start with statistical anomaly detection
7. Gradually add ML models as data accumulates

### Q49: Your ML model is raising too many false positives. How do you fix it?
**Approach:**
1. Analyze false positive patterns
2. Review training data quality
3. Adjust decision threshold
4. Add more discriminative features
5. Consider ensemble methods
6. Implement feedback loop for model improvement

### Q50: Design an AIOps strategy for a microservices migration.
**Approach:**
1. Establish observability baseline
2. Instrument new services with OpenTelemetry
3. Build service dependency map
4. Create canary deployment monitoring
5. Implement anomaly detection per service
6. Build automated rollback triggers
7. Gradually increase automation as confidence grows

---

## Behavioral Questions

### Q51: Tell me about a time you improved system reliability.
*Use STAR method: Situation, Task, Action, Result*

### Q52: How do you prioritize when multiple incidents occur?
**Key points:** Impact, customer affect, SLA considerations

### Q53: Describe a situation where automation failed.
**Key points:** What happened, how you recovered, what you learned

### Q54: How do you communicate technical issues to non-technical stakeholders?
**Key points:** Simplify, focus on business impact, use analogies

### Q55: How do you stay updated with AIOps developments?
**Key points:** Conferences, papers, open source, communities

---

*Good luck with your interviews! 🚀*
