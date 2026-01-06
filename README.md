# AKS Management Dashboard

A modern Flask-based web dashboard for managing and monitoring multiple Azure Kubernetes Service (AKS) clusters across subscriptions and regions.

## Features

- 🌳 **Hierarchical Cluster View**: App → Subscription → Region → AKS Cluster → Namespace → Pods
- 🔄 **Dynamic Configuration**: Auto-reload when cluster config file changes
- 📊 **Pod Management**: View pod details, status, and container information
- 📝 **Real-time Log Streaming**: WebSocket-based log tailing with xterm.js
- 🔧 **Read-Only Commands**: Execute whitelisted kubectl commands safely
- 🏥 **Health Advisor**: Detect unhealthy pods and get remediation suggestions
- 🔍 **Advanced Log Search**: Search logs by pod, namespace, or across all namespaces with search history
- 📈 **Hardware Info**: View cluster node pools and VM configurations
- ⏰ **Cronjob Management**: List and monitor cron jobs
- 🌓 **Dark/Light Theme**: Toggle between themes
- 📋 **Audit Logging**: Track all commands per IP address
- 🖥️ **Terminal Launcher**: Launch pre-configured terminals for AKS clusters
- ⌨️ **Keyboard Shortcuts**: Quick navigation and actions
- 📱 **Responsive Design**: Mobile-friendly UI with slide-out sidebar

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `/` or `Ctrl+K` | Focus search input |
| `Escape` | Close all modals and dropdowns |
| `Alt+1` | Switch to Pods tab |
| `Alt+2` | Switch to Logs tab |
| `Alt+3` | Switch to Commands tab |
| `Alt+4` | Switch to Health tab |
| `Alt+5` | Switch to Hardware tab |
| `Alt+6` | Switch to CronJobs tab |
| `Alt+7` | Switch to Search tab |

## Search Features

The dashboard includes powerful log search capabilities:

- **Pod-Specific Search**: Filter logs by specific pod
- **All Namespaces Search**: Search across all namespaces in a cluster
- **Case Sensitivity**: Toggle case-sensitive matching
- **Search History**: Recent searches saved locally (up to 20 queries)
- **Context Lines**: View surrounding log lines for matches
- **Clear & Reset**: Quick button to reset search form

## Prerequisites

- Python 3.12.3+
- Azure CLI installed and authenticated (`az login`)
- kubectl installed and configured
- Access to target AKS clusters

## Quick Start

### 1. Clone and Setup

```bash
cd AKS_Management_Dashboard
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 2. Configure

```bash
# Copy example env file
cp .env.example .env

# Edit cluster configuration
# Update config/clusters_config.json with your clusters
```

### 3. Azure Authentication

```bash
# Login to Azure CLI
az login

# Set subscription (if needed)
az account set --subscription "Your-Subscription-Name"

# Get AKS credentials for each cluster
az aks get-credentials --resource-group <rg-name> --name <cluster-name>
```

### 4. Run

```bash
python run.py
```

Visit `http://localhost:5000`

## Configuration

### clusters_config.json

Define your cluster hierarchy:

```json
{
  "applications": [
    {
      "name": "App Name",
      "subscriptions": [
        {
          "subscription_id": "xxx-xxx-xxx",
          "regions": [
            {
              "name": "East US",
              "environment": "PROD",
              "clusters": [
                {
                  "cluster_name": "my-aks-cluster",
                  "resource_group": "my-rg",
                  "monitored_namespaces": ["default", "app"]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

### allowed_commands.json

Whitelist of safe kubectl commands. Only commands listed here can be executed.

## Security

- **Read-Only**: Only `get`, `describe`, `logs`, and `top` commands allowed
- **No Destructive Operations**: `delete`, `apply`, `patch` etc. are blocked
- **Parameter Validation**: All command parameters validated against regex patterns
- **Audit Trail**: Every command logged with IP address and timestamp
- **Rate Limiting**: Configurable limits to prevent cluster overload

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Flask Web Application                     │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Jinja2 + TailwindCSS + Socket.IO)                │
├─────────────────────────────────────────────────────────────┤
│  Backend Services                                            │
│  ├── Azure Manager (azure-identity, azure-mgmt)             │
│  ├── kubectl Executor (subprocess, whitelist validation)    │
│  ├── Log Streamer (WebSocket, subprocess)                   │
│  ├── Config Watcher (watchdog)                              │
│  └── Audit Logger (CSV)                                     │
├─────────────────────────────────────────────────────────────┤
│  External                                                    │
│  ├── Azure CLI (az)                                         │
│  ├── kubectl                                                │
│  └── AKS Clusters                                           │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
AKS_Management_Dashboard/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # App configuration
│   ├── services/            # Backend services
│   ├── routes/              # API endpoints
│   ├── templates/           # Jinja2 templates
│   └── static/              # CSS, JS, images
├── config/
│   ├── clusters_config.json # Cluster definitions
│   ├── allowed_commands.json# Command whitelist
│   └── app_settings.json    # App settings
├── logs/audit/              # Command audit logs
├── tests/                   # Test suite
├── requirements.txt
├── run.py                   # Entry point
└── README.md
```

## Development

### Running Tests

```bash
pytest tests/ -v --cov=app
```

### Code Formatting

```bash
black app/
flake8 app/
```

---

## Production Deployment Guide

This section provides detailed instructions for deploying the AKS Management Dashboard in a production environment.

### Step 1: Disable Mock Mode

The application runs in **Mock Mode** by default for testing. To connect to real AKS clusters:

**Open `app/config.py` and change line 15:**

```python
# Change this:
MOCK_MODE = True   # Set to False for production (real Azure/kubectl)

# To this:
MOCK_MODE = False  # Set to False for production (real Azure/kubectl)
```

That's it! Just change `True` to `False`.

### Step 2: Configuration Settings

All settings are in `app/config.py`. The main ones to review for production:

```python
# Main switch - already changed in Step 1
MOCK_MODE = False

# Change this to a random string for security
SECRET_KEY = 'your-random-secret-key-here'

# Server settings (usually fine as default)
HOST = '0.0.0.0'
PORT = 5000

# Session timeout (in seconds)
SESSION_TIMEOUT = 300       # 5 minutes
SESSION_EXTEND_TIME = 120   # 2 minutes per extend
SESSION_MAX_EXTENDS = 2     # Max 2 extensions
```

### Step 3: Environment Variables (Optional)

For advanced deployments, you can use environment variables:

```bash
# Flask Configuration
FLASK_APP=run.py
FLASK_DEBUG=0

# Azure Configuration (optional - uses az login by default)
AZURE_TENANT_ID=<your-tenant-id>
AZURE_CLIENT_ID=<your-client-id>
AZURE_CLIENT_SECRET=<your-client-secret>

# Session Timeout (seconds)
SESSION_TIMEOUT=300          # 5 minutes default
SESSION_EXTEND_TIME=120      # 2 minutes per extend
SESSION_MAX_EXTENDS=2        # Max 2 extensions allowed

# Logging
LOG_LEVEL=INFO

# Config Paths (use absolute paths in production)
CLUSTERS_CONFIG_PATH=/opt/aks-dashboard/config/clusters_config.json
ALLOWED_COMMANDS_PATH=/opt/aks-dashboard/config/allowed_commands.json
APP_SETTINGS_PATH=/opt/aks-dashboard/config/app_settings.json
AUDIT_LOG_DIR=/var/log/aks-dashboard/audit
```

### Step 3: Azure Authentication

For production, you have three authentication options:

#### Option A: Azure CLI (Interactive - for on-premises/dev servers)

```bash
az login
az account set --subscription "<subscription-id>"
az aks get-credentials --resource-group <rg> --name <cluster> --admin
```

#### Option B: Service Principal (Recommended for servers)

```bash
# Create service principal with Reader access to AKS
az ad sp create-for-rbac --name "aks-dashboard-sp" \
    --role "Azure Kubernetes Service Cluster User Role" \
    --scopes /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ContainerService/managedClusters/<cluster>

# Set environment variables
export AZURE_TENANT_ID=<tenant-id>
export AZURE_CLIENT_ID=<app-id>
export AZURE_CLIENT_SECRET=<password>
```

#### Option C: Managed Identity (for Azure VMs/AKS)

If running on Azure VM or AKS, use system-assigned managed identity:

```bash
# Enable managed identity on VM
az vm identity assign --name <vm-name> --resource-group <rg>

# Grant access to AKS
az role assignment create \
    --assignee <managed-identity-principal-id> \
    --role "Azure Kubernetes Service Cluster User Role" \
    --scope /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ContainerService/managedClusters/<cluster>
```

### Step 4: kubectl Configuration

Ensure kubectl contexts are configured for all clusters:

```bash
# Get credentials for each cluster
az aks get-credentials \
    --resource-group <resource-group> \
    --name <cluster-name> \
    --context <context-name> \
    --admin

# Verify contexts
kubectl config get-contexts

# Test connectivity
kubectl --context <context-name> get nodes
```

### Step 5: Configure Clusters

Edit `config/clusters_config.json` with your actual cluster details:

```json
{
  "version": "2.0",
  "proxy_settings": {
    "https_proxy": "",
    "no_proxy": "localhost,127.0.0.1,.internal",
    "kubectl_path": "/usr/local/bin"
  },
  "applications": [
    {
      "name": "Production App",
      "config_style": "multi-env-with-contexts",
      "environments": [
        {
          "name": "PROD",
          "display_name": "Production",
          "subscription_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "resource_group": "rg-prod",
          "cluster_name": "aks-prod-cluster",
          "contexts": [
            {
              "context_name": "prod-primary",
              "kubeconfig_context": "aks-prod-cluster",
              "description": "Primary Production"
            }
          ],
          "monitored_namespaces": ["default", "app", "monitoring"]
        }
      ]
    }
  ]
}
```

### Step 6: Production Server Setup

#### Using Gunicorn (Linux - Recommended)

```bash
# Install gunicorn
pip install gunicorn eventlet

# Run with gunicorn
gunicorn --worker-class eventlet \
         --workers 1 \
         --bind 0.0.0.0:5000 \
         --timeout 120 \
         --log-level info \
         "app:create_app('production')"
```

#### Using Waitress (Windows)

```bash
# Install waitress
pip install waitress

# Run with waitress
waitress-serve --host=0.0.0.0 --port=5000 --call "app:create_app"
```

#### Systemd Service (Linux)

Create `/etc/systemd/system/aks-dashboard.service`:

```ini
[Unit]
Description=AKS Management Dashboard
After=network.target

[Service]
Type=simple
User=aks-dashboard
Group=aks-dashboard
WorkingDirectory=/opt/aks-dashboard
Environment="FLASK_ENV=production"
Environment="MOCK_MODE=false"
Environment="SECRET_KEY=<your-secret-key>"
ExecStart=/opt/aks-dashboard/.venv/bin/gunicorn \
    --worker-class eventlet \
    --workers 1 \
    --bind 127.0.0.1:5000 \
    --timeout 120 \
    "app:create_app('production')"
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable aks-dashboard
sudo systemctl start aks-dashboard
```

### Step 7: Reverse Proxy (nginx)

Create `/etc/nginx/sites-available/aks-dashboard`:

```nginx
upstream aks_dashboard {
    server 127.0.0.1:5000;
}

server {
    listen 443 ssl http2;
    server_name aks-dashboard.example.com;

    ssl_certificate /etc/ssl/certs/aks-dashboard.crt;
    ssl_certificate_key /etc/ssl/private/aks-dashboard.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        proxy_pass http://aks_dashboard;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}

server {
    listen 80;
    server_name aks-dashboard.example.com;
    return 301 https://$server_name$request_uri;
}
```

Enable and restart nginx:

```bash
sudo ln -s /etc/nginx/sites-available/aks-dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 8: Session Timeout Configuration

The dashboard includes automatic session timeout for security:

| Setting | Default | Description |
|---------|---------|-------------|
| `SESSION_TIMEOUT` | 300s (5 min) | Initial session duration |
| `SESSION_EXTEND_TIME` | 120s (2 min) | Time added per extension |
| `SESSION_MAX_EXTENDS` | 2 | Maximum number of extensions |

**Behavior:**
- Countdown timer displayed in navbar
- User can extend session up to 2 times (+2 min each)
- After max extensions, session is force-logged out
- User activity (clicks, keystrokes) resets the timer

### Step 9: Security Checklist

Before going live, verify:

- [ ] `MOCK_MODE=false` is set
- [ ] `SECRET_KEY` is a strong random value (32+ characters)
- [ ] `FLASK_DEBUG=0` is set
- [ ] SSL/TLS is configured
- [ ] Firewall allows only required ports (443)
- [ ] Azure RBAC permissions are minimal (Reader/User roles)
- [ ] `allowed_commands.json` contains only safe read-only commands
- [ ] Audit logging is enabled and logs are rotated
- [ ] Session timeout is configured appropriately
- [ ] kubectl contexts are properly configured

### Step 10: Monitoring & Maintenance

#### Log Locations

```
/var/log/aks-dashboard/audit/    # Command audit logs
/var/log/aks-dashboard/app.log   # Application logs
```

#### Health Check Endpoint

```bash
curl http://localhost:5000/api/config
```

#### Rotate Audit Logs

```bash
# Add to /etc/logrotate.d/aks-dashboard
/var/log/aks-dashboard/audit/*.csv {
    daily
    rotate 30
    compress
    missingok
    notifempty
}
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "Pod not found" errors | Verify kubectl context and namespace configuration |
| Azure login fails | Check service principal permissions and credentials |
| WebSocket disconnects | Ensure nginx proxy settings include WebSocket upgrade |
| Session expires too fast | Increase `SESSION_TIMEOUT` environment variable |
| Commands fail | Check `allowed_commands.json` whitelist |

---

## License

MIT License

## Support

For issues and feature requests, please open a GitHub issue.
