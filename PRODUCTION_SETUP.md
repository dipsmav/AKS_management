# Production Setup Guide

A simple step-by-step guide to run AKS Management Dashboard with real Azure clusters.

---

## Quick Start (4 Steps)

### Step 1: Set Production Mode

Open `app/config.py` and change line 15:

```python
MOCK_MODE = False   # Set to False for production
```

### Step 2: Login to Azure (Before starting the app)

Open a terminal and run these commands FIRST:

```bash
# Login to Azure (this will open a browser)
az login

# Set your subscription
az account set --subscription "Your-Subscription-Name"

# Get credentials for your AKS cluster(s)
az aks get-credentials --resource-group YOUR-RG --name YOUR-CLUSTER-NAME
```

### Step 3: Verify kubectl works

```bash
# Test that kubectl can connect to your cluster
kubectl get nodes
```

You should see your cluster nodes listed. If not, fix your Azure/kubectl setup first.

### Step 4: Run the App

```bash
python run.py
```

**You should see in the console:**
```
Mode: PRODUCTION (Real kubectl)
...
STARTING IN PRODUCTION MODE - Using real kubectl
kubectl found: ...
Azure CLI found
```

Visit `http://localhost:5050` - you should see **PRODUCTION** badge (green) instead of **MOCK MODE** (yellow).

---

## Troubleshooting

### "kubectl not found" error
Install kubectl: https://kubernetes.io/docs/tasks/tools/

### "az not found" error  
Install Azure CLI: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

### "No clusters found" error
Make sure you ran `az aks get-credentials` for your clusters.

### Still showing mock data?
1. Make sure you saved `config.py` after changing `MOCK_MODE = False`
2. **Restart the app** (stop and run `python run.py` again)

---

## Configure Your Clusters

Edit `config/clusters_config.json` to match your real clusters:

```json
{
  "applications": [
    {
      "name": "My App",
      "config_style": "multi-env-with-contexts",
      "environments": [
        {
          "name": "PROD",
          "cluster_name": "my-aks-cluster",
          "resource_group": "my-resource-group",
          "subscription_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "contexts": [
            {
              "context_name": "prod-primary",
              "kubeconfig_context": "my-aks-cluster",
              "description": "Production"
            }
          ],
          "monitored_namespaces": ["default", "my-app-namespace"]
        }
      ]
    }
  ]
}
```

---

## Verify It's Working

1. Header shows green **PRODUCTION** badge (not yellow MOCK MODE)
2. Clicking "Login to Azure (2FA)" actually opens device code flow
3. Pods shown are your real pods from the cluster
4. Logs are real logs from your containers

---

## Summary

| What to do | Where |
|------------|-------|
| Switch to production | `app/config.py` line 15: `MOCK_MODE = False` |
| Configure clusters | `config/clusters_config.json` |
| Azure login | Terminal: `az login` |
| Get kubectl access | Terminal: `az aks get-credentials ...` |
| Run app | Terminal: `python run.py` |
