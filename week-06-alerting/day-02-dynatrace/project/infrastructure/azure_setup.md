# Azure Setup Guide: Dynatrace OneAgent & Service Principal

To implement **The Root Cause Detective**, you need to connect your Azure subscription to Dynatrace so that Davis AI can see both high-level metrics and low-level code issues.

---

## 🔐 1. Azure Service Principal (Cloud Integration)

To pull Azure-specific metrics (like Azure SQL DTUs or App Service Plans), Dynatrace needs a Service Principal.

1.  **Azure Portal** -> **App Registrations** -> **New Registration**.
    - Name: `DynatraceCloudIntegration`.
2.  **Certificates & Secrets** -> **New Client Secret**.
    - Copy the **Value** immediately (it will be hidden later).
3.  **Access Control (IAM)** -> **Subscription Level**.
    - Add **Role Assignment**: `Reader`.
    - Select your `DynatraceCloudIntegration` app.
4.  **Copy standard IDs:**
    - Directory (Tenant) ID.
    - Application (Client) ID.

## 🏗️ 2. Connecting to Dynatrace

1.  In **Dynatrace**, go to **Infrastructure** -> **Azure**.
2.  Click **Configure Integration**.
3.  Enter the 4 IDs from Step 1 (Tenant, Client, Secret, Subscription).
4.  Wait 5 minutes. You should see your Azure Resources appearing in the **Infrastructure** dashboard.

---

## 📡 3. OneAgent Deployment (Code Integration)

For deep RCA, we need the OneAgent inside your App Service.

### For Azure App Service (Windows/Linux):
1.  Go to your **App Service** in Azure.
2.  Under **Settings**, click on **Extensions**.
3.  Click **+ Add** and search for **Dynatrace OneAgent**.
4.  Provide your **Tenant URL** and **API Token** (Installer Token).
5.  **Restart** the App Service.

### For Azure Kubernetes Service (AKS):
Follow the Dynatrace Operator pattern:
```bash
# Get the dynatrace-operator.yaml from your DT tenant
kubectl create namespace dynatrace
kubectl apply -f https://github.com/Dynatrace/dynatrace-operator/releases/latest/download/kubernetes.yaml
```

---

## 🧪 4. Verifying Smartscape
1.  In Dynatrace, click on **Smartscape Topology**.
2.  You should see your **Web App** connected to your **Database** with an arrow.
3.  If Davis detects an error in the DB, it will automatically trace it up the chain to the Web App.

## 💡 Troubleshooting
- **No metrics in DT?** Ensure the Service Principal has `Reader` permissions at the **Subscription** level, not just the Resource Group.
- **No code-level traces?** Ensure the App Service was restarted after Installing the extension.
