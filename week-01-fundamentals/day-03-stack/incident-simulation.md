# Incident Response Simulation: "The Midnight Outage"

> **A realistic incident scenario to practice your observability skills.**

---

## 📖 Scenario Background

You're the on-call SRE for "ShopFast," an e-commerce platform. It's 2:47 AM on Black Friday, and PagerDuty just woke you up.

**Alert:** `High Error Rate - Payment Service`

Your phone shows 47 missed Slack messages. The CEO is awake. Customers are complaining on Twitter.

**Your mission:** Use Prometheus, Grafana, and Jaeger to diagnose and resolve the incident as fast as possible.

---

## 🎯 Learning Objectives

1. Practice incident triage using observability tools
2. Learn systematic debugging methodology
3. Experience real-world pressure (simulated)
4. Document post-incident analysis

---

## 🚨 Phase 1: Initial Alert (T+0 minutes)

### What You Know
```
Alert: HighErrorRate
Service: payment-service
Severity: CRITICAL
Error Rate: 23% (threshold: 5%)
Started: 2:42 AM
```

### Your First Actions

**⏱️ Set a timer for 5 minutes. What queries do you run?**

<details>
<summary>🔍 Suggested Investigation Steps</summary>

1. **Verify the alert is real:**
```promql
sum(rate(http_requests_total{service="payment", status=~"5.."}[5m])) 
/ 
sum(rate(http_requests_total{service="payment"}[5m]))
```

2. **Check when it started:**
```promql
rate(http_requests_total{service="payment", status=~"5.."}[1m])
```
*Look at the graph over the last hour.*

3. **Check dependencies:**
```promql
up{job=~".*payment.*|.*database.*|.*redis.*"}
```

4. **Check resource usage:**
```promql
# CPU
rate(container_cpu_usage_seconds_total{container="payment"}[5m])

# Memory
container_memory_usage_bytes{container="payment"}
```
</details>

---

## 🔎 Phase 2: Deep Dive (T+5 minutes)

### New Information from Logs

You check the logs and see:
```json
{
  "timestamp": "2024-01-08T02:43:15Z",
  "level": "ERROR",
  "service": "payment-service",
  "message": "Transaction processing failed",
  "error": "Connection timeout to payment-gateway",
  "duration_ms": 30000,
  "trace_id": "abc123def456"
}
```

### Investigation Questions

**🤔 What does this tell you?**

1. The payment service itself is UP
2. But it can't reach the payment gateway
3. Let's check if the gateway is down...

<details>
<summary>🔍 Next Steps</summary>

**Check payment gateway health:**
```promql
up{job="payment-gateway"}
```

**Check if there's a network issue:**
```promql
# Network errors
rate(node_network_transmit_errs_total[5m])

# DNS failures (if you have DNS metrics)
rate(coredns_dns_request_duration_seconds_count{rcode="SERVFAIL"}[5m])
```

**Use Jaeger to trace a failed request:**
1. Go to Jaeger UI
2. Search for trace ID: `abc123def456`
3. Look at the span duration breakdown

</details>

---

## 🎬 Phase 3: The Plot Twist (T+10 minutes)

### Jaeger Trace Analysis

```mermaid
gantt
    title Failed Payment Request Trace (TraceID: abc123def456)
    dateFormat  X
    axisFormat %L ms
    
    section Frontend
    HTTP Request       :0, 50
    
    section Payment Service
    Process Payment    :50, 30100
    Call Gateway       :60, 30050
    
    section Payment Gateway
    Timeout (no response) :30100, 30100
```

**The span shows:**
- Frontend → Payment Service: 50ms (normal)
- Payment Service waits 30 seconds
- Payment Gateway: **NO SPAN RECEIVED**

### 💡 Hypothesis

The payment gateway is not responding, causing timeouts.

**But why? It shows as `up` in Prometheus...**

<details>
<summary>🔍 Advanced Investigation</summary>

**Check gateway metrics in detail:**
```promql
# Request rate - is it receiving requests?
rate(http_requests_total{service="payment-gateway"}[5m])

# Response time - is it slow?
histogram_quantile(0.95,
  rate(http_request_duration_seconds_bucket{service="payment-gateway"}[5m])
)

# Thread pool exhaustion?
payment_gateway_thread_pool_active / payment_gateway_thread_pool_max
```

**💥 Discovery:** Thread pool is at 100%! Gateway is alive but can't process requests.

</details>

---

## 🛠️ Phase 4: Resolution (T+15 minutes)

### Root Cause Identified

The payment gateway's thread pool is exhausted. Why?

<details>
<summary>🔍 Final Investigation</summary>

**Check external API calls from gateway:**
```promql
rate(payment_gateway_external_api_calls_total[5m])
```

**Discovery:** The gateway is calling a third-party fraud detection API, which is responding slowly (20 seconds vs normal 100ms).

**Correlation:**
```promql
# Fraud API latency
fraud_api_response_time_seconds > 10
```

**Timeline:**
1. 2:42 AM: Fraud API became slow
2. Payment gateway threads waiting on fraud API
3. Thread pool exhausted
4. New payment requests timeout
5. Customers see errors

</details>

### Resolution Options

**Which would you choose?**

A. Restart payment gateway (clears thread pool)
B. Disable fraud check temporarily
C. Increase thread pool size
D. Implement circuit breaker

<details>
<summary>💡 Best Practice Solution</summary>

**Option D: Circuit Breaker (if available)** or **Option B (immediate fix) + Option D (permanent fix)**

**Immediate action:**
```bash
# Feature flag to bypass fraud check
kubectl set env deployment/payment-gateway FRAUD_CHECK_ENABLED=false
```

**Post-incident:**
- Implement circuit breaker pattern
- Add timeout to fraud API calls (max 2s)
- Add fallback logic

</details>

---

## 📊 Phase 5: Post-Incident Review (PIR)

### Incident Timeline

| Time | Event | Evidence |
|------|-------|----------|
| 2:42 AM | Incident starts | Error rate spike in Prometheus |
| 2:43 AM | Logs show timeouts | Logs analysis |
| 2:47 AM | Alert fires | PagerDuty |
| 2:52 AM | Root cause found | Jaeger + Prometheus correlation |
| 3:05 AM | Mitigation applied | Feature flag deployed |
| 3:10 AM | Incident resolved | Error rate returns to normal |

**Total downtime:** 28 minutes  
**Estimated revenue impact:** $450,000

---

## 🎓 What You Learned

### The Observability Triangle in Action

1. **Metrics (Prometheus):** Detected high error rate, resource usage
2. **Logs:** Provided error details and trace IDs
3. **Traces (Jaeger):** Pinpointed exact bottleneck

### Key Insights

✅ **Golden Signals worked:**
- Latency: P95 went from 100ms → 30s
- Errors: 5xx rate spiked to 23%
- Traffic: Request rate dropped (circuit breaking)
- Saturation: Thread pool at 100%

✅ **Correlation is crucial:**
- Don't just look at one service
- Check ALL dependencies
- External APIs can be the culprit

❌ **What could have prevented this:**
- Circuit breaker on external API calls
- Synthetic monitoring of payment flow
- Dependency health checks in readiness probe

---

## 🏆 Challenge: Your Turn

### Simulate This Yourself

**Setup:**
1. Deploy the multi-service project from Day 3
2. Add a "fraud-api" service with configurable latency
3. Configure thread pools in payment service

**Inject the failure:**
```bash
# Slow down fraud API
kubectl set env deployment/fraud-api RESPONSE_DELAY_MS=20000
```

**Time yourself:**
- How long to detect?
- How long to diagnose?
- How long to resolve?

**Bonus:** Create alert rules that would have caught this earlier.

---

## 📝 Exercise: Write Your PIR

Create a `pir-midnight-outage.md` with:

1. **What happened?** (1 paragraph summary)
2. **Timeline** (detailed with evidence)
3. **Root cause** (5 Whys analysis)
4. **Resolution** (what you did)
5. **Prevention** (action items)

**5 Whys Example:**
1. Why did payments fail? → Timeouts from payment gateway
2. Why timeouts? → Gateway thread pool exhausted
3. Why exhausted? → Threads blocked on fraud API
4. Why blocked? → Fraud API responding slowly (20s)
5. Why no circuit breaker? → Not implemented

**Root cause:** No timeout or circuit breaker on external dependency.

---

## 🎯 Real-World Application

This scenario is based on actual incidents from:
- **Shopify Black Friday 2021** - Third-party payment gateway issues
- **Stripe 2019** - Database connection pool exhaustion
- **PayPal 2020** - Network latency cascade

**Lesson:** Your monitoring is only as good as your ability to correlate signals across systems.

---

**Share your incident timeline in GitHub Discussions!** 🚨
