# Infrastructure Setup: Prometheus & Grafana on K8s

To build **The Self-Adjusting Sentinel**, you need a local or cloud-based Kubernetes cluster. We will use the `kube-prometheus-stack` to deploy our AIOps environment.

---

## ☸️ 1. Install Prometheus Stack via Helm

1.  **Add the repository:**
    ```bash
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update
    ```

2.  **Deploy the stack:**
    Create a namespace and install:
    ```bash
    kubectl create namespace monitoring
    helm install monitoring prometheus-community/kube-prometheus-stack --namespace monitoring
    ```

3.  **Verify Pods:**
    ```bash
    kubectl get pods -n monitoring
    ```

---

## 📊 2. Accessing the UI

### Prometheus Dashboard:
```bash
kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090 -n monitoring
```
Access at [http://localhost:9090](http://localhost:9090).

### Grafana Dashboard:
```bash
kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring
```
Access at [http://localhost:3000](http://localhost:3000).
- **Username:** `admin`
- **Password:** `prom-operator` (default)

---

## 🛠️ 3. Deploying the Test Application
We need a workload that generates interesting metrics. We will deploy `node-exporter` (already included in stack) and a simple python "Metric Spiking" app.

```yaml
# project/infrastructure/anomaly-generator.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: anomaly-generator
spec:
  replicas: 1
  selector:
    matchLabels:
      app: anomaly-generator
  template:
    metadata:
      labels:
        app: anomaly-generator
    spec:
      containers:
      - name: generator
        image: python:3.9-slim
        command: ["python", "-c"]
        args:
        - |
          import http.server, time, random
          class Handler(http.server.BaseHTTPRequestHandler):
              def do_GET(self):
                  self.send_response(200)
                  self.end_headers()
                  # Occasional latency spikes
                  if random.random() > 0.9: time.sleep(random.uniform(1, 5))
                  self.wfile.write(b"OK")
          print("Starting generator...")
          http.server.HTTPServer(('0.0.0.0', 8080), Handler).serve_forever()
```

Apply it:
```bash
kubectl apply -f project/infrastructure/anomaly-generator.yaml
```

---

## 🛡️ 4. Configuring Alertmanager
Ensure your Alertmanager is configured to route to Slack or E-mail in `values.yaml` before deploying.
