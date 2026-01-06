# Azure AKS Management Dashboard - Comprehensive Project Plan

## Project Overview
A modern Flask-based web dashboard for managing and monitoring multiple Azure Kubernetes Service (AKS) clusters across subscriptions and regions with real-time log streaming, pod health monitoring, and command auditing.

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Technology Stack](#technology-stack)
3. [Python Libraries Reference](#python-libraries-reference)
4. [Project Structure](#project-structure)
5. [User Interaction Flow](#user-interaction-flow)
6. [Features Summary](#features-summary)
7. [Phase-wise Implementation Plan](#phase-wise-implementation-plan)
8. [Configuration Schema](#configuration-schema)
9. [API Endpoints Design](#api-endpoints-design)
10. [UI Components](#ui-components)
11. [Security Considerations](#security-considerations)
12. [Testing Strategy](#testing-strategy)
13. [Performance & Cluster Safety](#performance--cluster-safety)

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AKS Management Dashboard                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         Frontend (Flask + Jinja2)                     │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────────┐  │   │
│  │  │ Theme      │  │ Cluster    │  │ Pod        │  │ Log            │  │   │
│  │  │ Toggle     │  │ Hierarchy  │  │ Details    │  │ Viewer         │  │   │
│  │  │ (L/D)      │  │ Tree View  │  │ Panel      │  │ (WebSocket)    │  │   │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────────┘  │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────────┐  │   │
│  │  │ Command    │  │ Cronjob    │  │ Hardware   │  │ Health         │  │   │
│  │  │ Panel      │  │ List       │  │ Config     │  │ Advisor        │  │   │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         Backend Services                              │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────┐  │   │
│  │  │ Config Watcher │  │ Azure Manager  │  │ kubectl Executor       │  │   │
│  │  │ (File Monitor) │  │ (Azure SDK)    │  │ (Read-Only Commands)   │  │   │
│  │  └────────────────┘  └────────────────┘  └────────────────────────┘  │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────┐  │   │
│  │  │ WebSocket      │  │ Log Analyzer   │  │ Command Audit          │  │   │
│  │  │ Log Streamer   │  │ (Error Parser) │  │ Logger (CSV)           │  │   │
│  │  └────────────────┘  └────────────────┘  └────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         External Integrations                         │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────┐  │   │
│  │  │ Azure CLI      │  │ kubectl        │  │ clusters_config.json   │  │   │
│  │  │ (az commands)  │  │ (k8s commands) │  │ (Dynamic Reload)       │  │   │
│  │  └────────────────┘  └────────────────┘  └────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Azure Cloud                                        │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────────────┐ │
│  │ Subscription 1 │  │ Subscription 2 │  │ Subscription N                 │ │
│  │  ├─ Region A   │  │  ├─ Region A   │  │  ├─ Region A                   │ │
│  │  │  └─ AKS 1   │  │  │  └─ AKS 3   │  │  │  └─ AKS N                   │ │
│  │  ├─ Region B   │  │  ├─ Region B   │  │  └─ Region B                   │ │
│  │  │  └─ AKS 2   │  │  │  └─ AKS 4   │  │     └─ AKS N+1                 │ │
│  └────────────────┘  └────────────────┘  └────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Technology Stack

### Backend
| Component | Technology | Purpose |
|-----------|------------|---------|
| Web Framework | Flask 3.x | REST API + Server-side rendering |
| WebSocket | Flask-SocketIO | Real-time log streaming |
| Azure SDK | azure-identity, azure-mgmt-containerservice | Azure resource access |
| Kubernetes | kubernetes (official Python client) | Direct K8s API access |
| File Watching | watchdog | Config file change detection |
| Task Queue | threading/asyncio | Background operations |

### Frontend
| Component | Technology | Purpose |
|-----------|------------|---------|
| CSS Framework | TailwindCSS | Modern responsive design |
| JavaScript | Vanilla JS + Socket.IO client | Interactivity |
| Icons | Lucide Icons | UI iconography |
| Theme | CSS Variables + LocalStorage | Light/Dark mode toggle |
| Terminal | xterm.js | Log streaming terminal |

### Data & Config
| Component | Format | Purpose |
|-----------|--------|---------|
| Cluster Config | JSON | Cluster definitions (dynamic reload) |
| Audit Log | CSV | Command history per IP |
| Cache | In-memory dict | Reduce API calls |

---

## 3. Python Libraries Reference

### Core Framework Libraries
| Library | Version | Purpose |
|---------|---------|---------|
| `Flask` | >=3.0.0 | Web framework for REST API and server-side rendering |
| `Flask-SocketIO` | >=5.3.6 | WebSocket support for real-time log streaming |
| `flask-cors` | >=4.0.0 | Cross-Origin Resource Sharing support |
| `python-dotenv` | >=1.0.0 | Environment variable loading from .env files |

### Azure Integration Libraries
| Library | Version | Purpose |
|---------|---------|---------|
| `azure-identity` | >=1.15.0 | Azure authentication (DefaultAzureCredential) |
| `azure-mgmt-containerservice` | >=28.0.0 | AKS cluster management API |
| `azure-mgmt-resource` | >=23.0.0 | Azure resource group operations |

### Kubernetes Libraries
| Library | Version | Purpose |
|---------|---------|---------|
| `kubernetes` | >=28.1.0 | Official Python client for Kubernetes API |

### File System & Background Processing
| Library | Version | Purpose |
|---------|---------|---------|
| `watchdog` | >=3.0.0 | File system monitoring for config changes |
| `threading` | (built-in) | Background task execution |
| `subprocess` | (built-in) | External command execution (kubectl, az) |

### WebSocket Libraries
| Library | Version | Purpose |
|---------|---------|---------|
| `python-engineio` | >=4.8.0 | Engine.IO protocol implementation |
| `python-socketio` | >=5.10.0 | Socket.IO server implementation |
| `eventlet` | >=0.33.3 | Async networking library for WebSocket |

### Utility Libraries
| Library | Version | Purpose |
|---------|---------|---------|
| `python-dateutil` | >=2.8.2 | Date/time parsing and manipulation |
| `requests` | >=2.31.0 | HTTP client for external API calls |
| `pathlib` | (built-in) | Cross-platform file path handling |
| `json` | (built-in) | JSON parsing and serialization |
| `tempfile` | (built-in) | Temporary file creation for scripts |
| `platform` | (built-in) | OS detection for cross-platform support |
| `re` | (built-in) | Regular expressions for parsing |

### Testing Libraries
| Library | Version | Purpose |
|---------|---------|---------|
| `pytest` | >=7.4.0 | Test framework |
| `pytest-flask` | >=1.3.0 | Flask testing utilities |
| `pytest-asyncio` | >=0.21.0 | Async test support |

---

## 4. Project Structure

```
AKS_Management_Dashboard/
│
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # App configuration
│   ├── extensions.py            # SocketIO, watchdog init
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── azure_manager.py     # Azure SDK operations
│   │   ├── kubectl_executor.py  # kubectl command execution
│   │   ├── config_watcher.py    # File change detection
│   │   ├── log_streamer.py      # WebSocket log streaming
│   │   ├── log_analyzer.py      # Error/exception parsing
│   │   ├── health_advisor.py    # Pod health recommendations
│   │   └── audit_logger.py      # CSV command logging
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py              # Main UI routes
│   │   ├── api.py               # REST API endpoints
│   │   └── websocket.py         # WebSocket event handlers
│   │
│   ├── templates/
│   │   ├── base.html            # Base template with theme toggle
│   │   ├── dashboard.html       # Main dashboard
│   │   ├── components/
│   │   │   ├── cluster_tree.html
│   │   │   ├── pod_details.html
│   │   │   ├── log_viewer.html
│   │   │   ├── command_panel.html
│   │   │   ├── cronjobs.html
│   │   │   ├── hardware_config.html
│   │   │   ├── health_advisor.html
│   │   │   └── search_panel.html
│   │   └── partials/
│   │       ├── navbar.html
│   │       └── sidebar.html
│   │
│   └── static/
│       ├── css/
│       │   ├── main.css         # TailwindCSS compiled
│       │   └── themes.css       # Light/Dark theme variables
│       ├── js/
│       │   ├── app.js           # Main application JS
│       │   ├── theme.js         # Theme toggle logic
│       │   ├── websocket.js     # SocketIO client
│       │   ├── cluster_tree.js  # Tree view interactions
│       │   └── log_viewer.js    # Terminal/log display
│       └── img/
│
├── config/
│   ├── clusters_config.json     # Cluster definitions (MAIN CONFIG)
│   ├── allowed_commands.json    # Whitelisted read-only commands
│   └── app_settings.json        # Application settings
│
├── logs/
│   └── audit/
│       └── commands_YYYY-MM-DD.csv  # Daily audit logs per IP
│
├── tests/
│   ├── __init__.py
│   ├── test_azure_manager.py
│   ├── test_kubectl_executor.py
│   ├── test_config_watcher.py
│   ├── test_log_analyzer.py
│   ├── test_health_advisor.py
│   └── test_api.py
│
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── Dockerfile                   # Container deployment (optional)
├── .env.example                 # Environment variables template
├── .gitignore
└── README.md
```

---

## 5. User Interaction Flow

### Login Flow (Automated with 2FA)
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AZURE LOGIN FLOW                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. User clicks "Login" button on cluster context                           │
│                          │                                                   │
│                          ▼                                                   │
│  2. System automatically:                                                    │
│     ├─ Sets up proxy environment (PATH, HTTPS_PROXY, NO_PROXY)              │
│     └─ Executes: az login --use-device-code                                 │
│                          │                                                   │
│                          ▼                                                   │
│  3. UI displays:  ┌─────────────────────────────────────┐                   │
│                   │   Enter this code: ABC123XY         │                   │
│                   │   [Open Microsoft Login Page]       │                   │
│                   └─────────────────────────────────────┘                   │
│                          │                                                   │
│                          ▼                                                   │
│  4. USER ACTION #1: Enter device code in browser                            │
│                          │                                                   │
│                          ▼                                                   │
│  5. USER ACTION #2: Approve in Microsoft Authenticator                      │
│                          │                                                   │
│                          ▼                                                   │
│  6. System automatically:                                                    │
│     ├─ az account set --subscription <sub-id>                               │
│     ├─ az aks get-credentials -g <rg> -n <cluster>                          │
│     └─ kubectl config use-context <context>                                 │
│                          │                                                   │
│                          ▼                                                   │
│  7. Login Complete - User can now use kubectl commands                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### CLI Terminal Session Flow
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CLI TERMINAL SESSION FLOW                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. User clicks Terminal (🖥️) button on cluster context                     │
│                          │                                                   │
│                          ▼                                                   │
│  2. System opens new terminal window with:                                   │
│     ├─ Proxy environment pre-configured                                     │
│     ├─ kubectl context set to selected cluster                              │
│     └─ Helpful startup message with cluster info                            │
│                          │                                                   │
│                          ▼                                                   │
│  3. Terminal displays:                                                       │
│     ┌─────────────────────────────────────────────────────────┐             │
│     │ ═══════════════════════════════════════════════════════ │             │
│     │   AKS CLI Session                                       │             │
│     │ ═══════════════════════════════════════════════════════ │             │
│     │   Application:    F                                     │             │
│     │   Environment:    prod                                  │             │
│     │   Context:        F-prod-context-1                      │             │
│     │   Cluster:        F-prod-aks                            │             │
│     │                                                         │             │
│     │   Quick Commands:                                       │             │
│     │     kubectl get pods   - List pods                      │             │
│     │     kubectl get nodes  - List nodes                     │             │
│     │ ═══════════════════════════════════════════════════════ │             │
│     │ PS C:\>                                                 │             │
│     └─────────────────────────────────────────────────────────┘             │
│                          │                                                   │
│                          ▼                                                   │
│  4. User can run any kubectl commands directly                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Cluster Navigation Flow
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CLUSTER NAVIGATION FLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Sidebar Cluster Tree:                                                       │
│                                                                              │
│  📁 Applications                                                             │
│  ├─ 📁 F (multi-env-with-contexts)                                          │
│  │  ├─ 📁 prod                                                              │
│  │  │  └─ 🖥️ F-prod-aks                                                     │
│  │  │     ├─ Contexts:                                                      │
│  │  │     │  ├─ ● PROD Primary     [🔑 Login] [🖥️ Terminal]                │
│  │  │     │  └─ ○ PROD Secondary   [🔑 Login] [🖥️ Terminal]                │
│  │  │     └─ Namespaces: (loaded on expand)                                 │
│  │  │        ├─ F-core                                                      │
│  │  │        ├─ market-data                                                 │
│  │  │        └─ order-execution                                             │
│  │  ├─ 📁 prod1                                                             │
│  │  └─ 📁 prod2                                                             │
│  │                                                                           │
│  └─ 📁 IS (multi-region-with-contexts)                                      │
│     ├─ 📁 NA (North America)                                                │
│     ├─ 📁 EU (Europe)                                                       │
│     └─ 📁 APAC (Asia Pacific)                                               │
│                                                                              │
│  Actions per context:                                                        │
│  • Click context row → Switch kubectl context                               │
│  • Click 🔑 Login → Start automated Azure login                             │
│  • Click 🖥️ Terminal → Open CLI terminal session                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Pod Management Flow
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        POD MANAGEMENT FLOW                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. Select Cluster → Select Namespace → View Pods                           │
│                          │                                                   │
│                          ▼                                                   │
│  2. Pod List View:                                                           │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │ Pod Name          │ Status    │ Restarts │ Age    │ Actions    │     │
│     ├───────────────────┼───────────┼──────────┼────────┼────────────┤     │
│     │ api-server-abc123 │ Running   │ 0        │ 2d     │ [📋][💡]   │     │
│     │ worker-def456     │ CrashLoop │ 5        │ 1h     │ [📋][💡]   │     │
│     └─────────────────────────────────────────────────────────────────┘     │
│                          │                                                   │
│                          ▼                                                   │
│  3. Click [📋] → View pod details, logs, events                             │
│     Click [💡] → Get AI remediation suggestions for issues                  │
│                          │                                                   │
│                          ▼                                                   │
│  4. Commands Tab → Execute read-only kubectl commands                       │
│     Full command displayed: kubectl get pods -n namespace                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Features Summary

### Implemented Features

| Feature | Description | Status |
|---------|-------------|--------|
| **Multi-Cluster Support** | FDB (3 envs) + FISCD (3 regions) with variable contexts | ✅ Complete |
| **Automated Azure Login** | Device code flow with auto proxy setup, only 2 user actions needed | ✅ Complete |
| **CLI Terminal Launcher** | Open pre-configured terminal for any cluster/context | ✅ Complete |
| **Context Management** | Switch kubectl contexts per cluster | ✅ Complete |
| **Pod Listing & Details** | View pods with status, events, conditions | ✅ Complete |
| **Log Streaming** | Real-time WebSocket log streaming with xterm.js | ✅ Complete |
| **Command Execution** | Read-only kubectl commands with full audit logging | ✅ Complete |
| **Health Advisor** | Remediation suggestions for problematic pods | ✅ Complete |
| **Session Command History** | Track all executed commands per session | ✅ Complete |
| **Config Hot Reload** | Automatic config reload via file watcher | ✅ Complete |
| **Theme Support** | Light/Dark mode with persistence | ✅ Complete |
| **Proxy Support** | Corporate proxy configuration (PATH, HTTPS_PROXY, NO_PROXY) | ✅ Complete |

### Configuration Styles Supported

| Style | Example App | Structure |
|-------|-------------|----------|
| `multi-env-with-contexts` | F | App → Environments (prod/prod1/prod2) → Contexts |
| `multi-region-with-contexts` | IS | App → Regions (NA/EU/APAC) → Contexts |

---

## 7. Phase-wise Implementation Plan

### Phase 1: Foundation (Days 1-2)
**Goal**: Basic Flask app with project structure and Azure connectivity

| Task | Description | Priority |
|------|-------------|----------|
| 1.1 | Create project structure with all folders | HIGH |
| 1.2 | Setup Flask app factory pattern | HIGH |
| 1.3 | Implement config.py with environment handling | HIGH |
| 1.4 | Create requirements.txt with all dependencies | HIGH |
| 1.5 | Implement base.html with TailwindCSS CDN | HIGH |
| 1.6 | Add light/dark theme toggle with CSS variables | HIGH |
| 1.7 | Test Azure CLI authentication (`az login` status check) | HIGH |
| 1.8 | Create clusters_config.json schema and sample | HIGH |

**Deliverables**:
- Running Flask app with theme toggle
- Azure CLI connectivity verified
- Sample configuration file

---

### Phase 2: Configuration & Cluster Discovery (Days 3-4)
**Goal**: Dynamic config loading and cluster hierarchy display

| Task | Description | Priority |
|------|-------------|----------|
| 2.1 | Implement config_watcher.py using watchdog | HIGH |
| 2.2 | Create clusters_config.json parser | HIGH |
| 2.3 | Implement azure_manager.py - subscription listing | HIGH |
| 2.4 | Implement AKS cluster details fetching | HIGH |
| 2.5 | Build cluster hierarchy tree view UI | HIGH |
| 2.6 | Add namespace listing per cluster | HIGH |
| 2.7 | Implement pod listing per namespace | HIGH |
| 2.8 | Add auto-refresh on config file change | MEDIUM |

**Deliverables**:
- Tree view: App → Subscription → Region → AKS → Namespace → Pods
- Real-time config reload without restart

---

### Phase 3: Pod Details & Hardware Info (Days 5-6)
**Goal**: Detailed pod information and cluster hardware config

| Task | Description | Priority |
|------|-------------|----------|
| 3.1 | Implement pod detail panel (status, labels, annotations) | HIGH |
| 3.2 | Add container details (image, resources, ports) | HIGH |
| 3.3 | Implement hardware_config display (node pools, VM sizes) | HIGH |
| 3.4 | Add cluster capacity information | MEDIUM |
| 3.5 | Implement cronjob listing per namespace | HIGH |
| 3.6 | Add cronjob schedule and last run info | MEDIUM |
| 3.7 | Implement responsive UI for all panels | MEDIUM |

**Deliverables**:
- Complete pod details view
- Hardware configuration panel
- Cronjobs listing with schedules

---

### Phase 4: Log Streaming & Viewing (Days 7-9)
**Goal**: Real-time log streaming via WebSocket

| Task | Description | Priority |
|------|-------------|----------|
| 4.1 | Setup Flask-SocketIO integration | HIGH |
| 4.2 | Implement log_streamer.py service | HIGH |
| 4.3 | Create kubectl logs -f wrapper with subprocess | HIGH |
| 4.4 | Build log viewer component with xterm.js | HIGH |
| 4.5 | Add tail lines selector (10, 50, 100, 500, all) | HIGH |
| 4.6 | Implement container selector for multi-container pods | MEDIUM |
| 4.7 | Add log download functionality | LOW |
| 4.8 | Implement log pause/resume for streaming | MEDIUM |

**Deliverables**:
- Real-time log streaming in browser
- Tail lines configuration
- Multi-container support

---

### Phase 5: Command Execution & Audit (Days 10-11)
**Goal**: Read-only command execution with full audit trail

| Task | Description | Priority |
|------|-------------|----------|
| 5.1 | Create allowed_commands.json whitelist | HIGH |
| 5.2 | Implement kubectl_executor.py with command validation | HIGH |
| 5.3 | Build command panel UI with preset commands | HIGH |
| 5.4 | Implement audit_logger.py (CSV per IP) | HIGH |
| 5.5 | Add command output display panel | HIGH |
| 5.6 | Implement command history per session | MEDIUM |
| 5.7 | Add IP-based rate limiting | MEDIUM |

**Allowed Read-Only Commands**:
```json
{
  "allowed_commands": [
    "kubectl get pods",
    "kubectl get pods -o wide",
    "kubectl describe pod {pod_name}",
    "kubectl get events",
    "kubectl top pods",
    "kubectl top nodes",
    "kubectl get configmaps",
    "kubectl get secrets --show-labels",
    "kubectl get services",
    "kubectl get ingress",
    "kubectl get deployments",
    "kubectl get replicasets",
    "kubectl get jobs",
    "kubectl get cronjobs",
    "kubectl logs {pod_name} --tail={lines}",
    "kubectl get nodes -o wide",
    "kubectl describe node {node_name}",
    "kubectl get pv",
    "kubectl get pvc",
    "kubectl get hpa"
  ]
}
```

**Deliverables**:
- Safe command execution framework
- Complete audit CSV logging
- Command output display

---

### Phase 6: Log Analysis & Health Advisor (Days 12-14)
**Goal**: Error detection and pod health recommendations

| Task | Description | Priority |
|------|-------------|----------|
| 6.1 | Implement log_analyzer.py with regex patterns | HIGH |
| 6.2 | Add case-sensitive/insensitive search option | HIGH |
| 6.3 | Implement multi-namespace error scanning | HIGH |
| 6.4 | Build search results UI with context | HIGH |
| 6.5 | Implement health_advisor.py | HIGH |
| 6.6 | Add pod status detection (CrashLoopBackOff, OOMKilled, etc.) | HIGH |
| 6.7 | Create remediation suggestions database | HIGH |
| 6.8 | Build health advisor UI with suggested kubectl commands | HIGH |

**Pod Status → Remediation Mapping**:
```python
REMEDIATION_SUGGESTIONS = {
    "CrashLoopBackOff": {
        "description": "Container keeps crashing after startup",
        "actions": [
            "kubectl logs {pod} --previous",
            "kubectl describe pod {pod}",
            "Check application startup dependencies",
            "Verify environment variables and secrets"
        ]
    },
    "ImagePullBackOff": {
        "description": "Unable to pull container image",
        "actions": [
            "kubectl describe pod {pod}",
            "Verify image name and tag",
            "Check image registry credentials",
            "kubectl get secret regcred -o yaml"
        ]
    },
    "OOMKilled": {
        "description": "Container exceeded memory limit",
        "actions": [
            "kubectl describe pod {pod}",
            "Increase memory limits in deployment",
            "Profile application memory usage",
            "kubectl top pods"
        ]
    },
    "Pending": {
        "description": "Pod cannot be scheduled",
        "actions": [
            "kubectl describe pod {pod}",
            "kubectl get nodes",
            "kubectl describe nodes | grep -A5 Allocated",
            "Check resource requests vs available capacity"
        ]
    },
    "ContainerCreating": {
        "description": "Container is being created (may indicate issues)",
        "actions": [
            "kubectl describe pod {pod}",
            "kubectl get events --sort-by=.lastTimestamp",
            "Check volume mounts and persistent claims"
        ]
    }
}
```

**Deliverables**:
- Error/exception log search
- Pod health status indicators
- Actionable remediation suggestions

---

### Phase 7: String Search & Polish (Days 15-16)
**Goal**: Advanced search and UI polish

| Task | Description | Priority |
|------|-------------|----------|
| 7.1 | Implement pod-specific log search | HIGH |
| 7.2 | Add --all-namespaces search option | HIGH |
| 7.3 | Implement search result highlighting | MEDIUM |
| 7.4 | Add search history and saved searches | LOW |
| 7.5 | UI polish - loading states, error handling | HIGH |
| 7.6 | Add keyboard shortcuts | LOW |
| 7.7 | Implement responsive mobile view | MEDIUM |
| 7.8 | Add cluster connection status indicators | MEDIUM |

**Deliverables**:
- Complete search functionality
- Polished, responsive UI

---

### Phase 8: Testing & Documentation (Days 17-18)
**Goal**: Comprehensive testing and documentation

| Task | Description | Priority |
|------|-------------|----------|
| 8.1 | Write unit tests for all services | HIGH |
| 8.2 | Write integration tests for API endpoints | HIGH |
| 8.3 | Write WebSocket connection tests | MEDIUM |
| 8.4 | Performance testing with multiple clusters | HIGH |
| 8.5 | Security review - command injection prevention | HIGH |
| 8.6 | Write README.md with setup instructions | HIGH |
| 8.7 | Create user guide documentation | MEDIUM |
| 8.8 | Add inline code documentation | MEDIUM |

**Deliverables**:
- Test suite with >80% coverage
- Complete documentation

---

## 5. Configuration Schema

### clusters_config.json
```json
{
  "version": "1.0",
  "last_updated": "2025-12-10T09:00:00Z",
  "applications": [
    {
      "name": "Trading Platform",
      "description": "Core trading application infrastructure",
      "subscriptions": [
        {
          "subscription_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
          "subscription_name": "Trading-Production",
          "regions": [
            {
              "name": "East US",
              "environment": "PROD",
              "clusters": [
                {
                  "cluster_name": "trading-prod-aks-eastus",
                  "resource_group": "trading-prod-rg",
                  "description": "Primary production cluster",
                  "monitored_namespaces": ["trading", "market-data", "order-execution"]
                }
              ]
            },
            {
              "name": "West US",
              "environment": "BCP",
              "clusters": [
                {
                  "cluster_name": "trading-bcp-aks-westus",
                  "resource_group": "trading-bcp-rg",
                  "description": "Business continuity cluster",
                  "monitored_namespaces": ["trading", "market-data", "order-execution"]
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

---

## 6. API Endpoints Design

### REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/config` | Get current cluster configuration |
| GET | `/api/config/reload` | Force config reload |
| GET | `/api/subscriptions` | List all subscriptions |
| GET | `/api/clusters/<subscription_id>` | List clusters in subscription |
| GET | `/api/cluster/<cluster_id>/namespaces` | List namespaces |
| GET | `/api/cluster/<cluster_id>/namespace/<ns>/pods` | List pods |
| GET | `/api/pod/<cluster_id>/<ns>/<pod_name>` | Pod details |
| GET | `/api/cluster/<cluster_id>/hardware` | Hardware config |
| GET | `/api/cluster/<cluster_id>/cronjobs` | List cronjobs |
| POST | `/api/command/execute` | Execute read-only command |
| GET | `/api/pod/<cluster_id>/<ns>/<pod_name>/logs` | Get pod logs (non-streaming) |
| POST | `/api/logs/search` | Search logs for errors |
| GET | `/api/health/<cluster_id>/<ns>` | Pod health status |
| GET | `/api/audit/commands` | Get command history |

### WebSocket Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `connect` | Client→Server | Establish connection |
| `subscribe_logs` | Client→Server | Start log streaming |
| `unsubscribe_logs` | Client→Server | Stop log streaming |
| `log_data` | Server→Client | Log line data |
| `error` | Server→Client | Error notification |
| `config_updated` | Server→Client | Config file changed |

---

## 7. UI Components

### Dashboard Layout
```
┌─────────────────────────────────────────────────────────────────────────┐
│  [Logo] AKS Dashboard          [🔍 Search] [☀️/🌙 Theme] [User]        │
├─────────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────┐ ┌─────────────────────────────────────────────────┐ │
│ │                 │ │                                                 │ │
│ │  📁 Apps        │ │   [Tabs: Pods | Logs | Commands | Health]      │ │
│ │  ├─ 📁 App 1    │ │                                                 │ │
│ │  │  ├─ Sub 1    │ │   ┌─────────────────────────────────────────┐  │ │
│ │  │  │  ├─ PROD  │ │   │                                         │  │ │
│ │  │  │  │  └─AKS │ │   │     Main Content Area                   │  │ │
│ │  │  │  └─ BCP   │ │   │     (Dynamic based on selection)        │  │ │
│ │  │  │     └─AKS │ │   │                                         │  │ │
│ │  │  └─ Sub 2    │ │   │                                         │  │ │
│ │  └─ 📁 App 2    │ │   │                                         │  │ │
│ │                 │ │   │                                         │  │ │
│ │  [Refresh]      │ │   └─────────────────────────────────────────┘  │ │
│ └─────────────────┘ └─────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────┤
│  Status: Connected to 3 clusters | Last refresh: 10s ago | v1.0.0      │
└─────────────────────────────────────────────────────────────────────────┘
```

### Theme CSS Variables
```css
:root {
  /* Light Theme (default) */
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --border-color: #e2e8f0;
  --accent-color: #3b82f6;
  --success-color: #22c55e;
  --warning-color: #f59e0b;
  --error-color: #ef4444;
}

[data-theme="dark"] {
  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --border-color: #334155;
  --accent-color: #60a5fa;
  --success-color: #4ade80;
  --warning-color: #fbbf24;
  --error-color: #f87171;
}
```

---

## 8. Security Considerations

### Command Injection Prevention
```python
# CRITICAL: Whitelist approach - NEVER execute user input directly
ALLOWED_COMMANDS = load_allowed_commands()

def execute_command(command_template, params):
    """
    Execute only whitelisted commands with validated parameters
    """
    # Validate command is in whitelist
    if command_template not in ALLOWED_COMMANDS:
        raise SecurityError(f"Command not allowed: {command_template}")
    
    # Validate parameters (no shell metacharacters)
    for key, value in params.items():
        if not re.match(r'^[a-zA-Z0-9\-_.]+$', value):
            raise SecurityError(f"Invalid parameter: {value}")
    
    # Build command safely
    command = command_template.format(**params)
    
    # Execute with shell=False
    result = subprocess.run(
        command.split(),
        capture_output=True,
        text=True,
        timeout=30,
        shell=False  # CRITICAL: Never use shell=True
    )
    return result
```

### Authentication & Authorization
- Azure CLI authentication (`az login`) required
- IP-based audit logging
- Optional: Azure AD integration for user authentication
- Rate limiting per IP address

### Data Protection
- No secrets displayed in full (masked)
- Audit logs stored locally (configurable retention)
- HTTPS recommended for production

---

## 9. Testing Strategy

### Unit Tests
```python
# test_kubectl_executor.py
def test_command_whitelist_validation():
    """Ensure only whitelisted commands execute"""
    executor = KubectlExecutor()
    
    # Valid command
    assert executor.is_allowed("kubectl get pods")
    
    # Invalid command (not in whitelist)
    assert not executor.is_allowed("kubectl delete pod test")
    
    # Injection attempt
    assert not executor.is_allowed("kubectl get pods; rm -rf /")

def test_parameter_sanitization():
    """Ensure parameters are properly sanitized"""
    executor = KubectlExecutor()
    
    # Valid parameter
    assert executor.validate_param("my-pod-name-123")
    
    # Invalid parameter (shell injection)
    assert not executor.validate_param("pod; rm -rf")
    assert not executor.validate_param("pod`whoami`")
```

### Integration Tests
```python
# test_api.py
def test_pod_listing_api(client):
    """Test pod listing endpoint"""
    response = client.get('/api/cluster/test-cluster/namespace/default/pods')
    assert response.status_code == 200
    data = response.json
    assert 'pods' in data

def test_config_reload(client, tmp_path):
    """Test config file change detection"""
    # Modify config file
    config_path = tmp_path / "clusters_config.json"
    config_path.write_text('{"version": "2.0"}')
    
    # Wait for watcher
    time.sleep(1)
    
    # Verify reload
    response = client.get('/api/config')
    assert response.json['version'] == '2.0'
```

---

## 13. Performance & Cluster Safety

### Minimal Cluster Impact
```python
# Rate limiting for kubectl commands
RATE_LIMITS = {
    "get_pods": {"calls": 10, "period": 60},      # 10 calls per minute
    "describe_pod": {"calls": 5, "period": 60},   # 5 calls per minute
    "get_logs": {"calls": 3, "period": 60},       # 3 calls per minute
    "top_pods": {"calls": 2, "period": 60}        # 2 calls per minute
}

# Caching to reduce API calls
CACHE_TTL = {
    "namespaces": 60,      # 1 minute
    "pods": 30,            # 30 seconds
    "pod_details": 15,     # 15 seconds
    "hardware_config": 300, # 5 minutes
    "cronjobs": 120        # 2 minutes
}
```

### Read-Only Guarantee
- All kubectl commands use `get`, `describe`, `logs`, `top` only
- No `delete`, `apply`, `patch`, `create`, `edit` commands allowed
- Command whitelist enforced at multiple levels:
  1. Frontend - only shows allowed commands
  2. API - validates against whitelist
  3. Executor - final validation before execution

### Resource Limits
```python
# Subprocess limits
SUBPROCESS_LIMITS = {
    "timeout": 30,           # Max 30 seconds per command
    "max_output_lines": 1000, # Limit log lines
    "max_parallel_commands": 3 # Concurrent command limit
}
```

---

## 14. Production Deployment Guide

### Deployment Architecture
For production, do NOT use the built-in Flask development server. Use a production-grade WSGI server behind a reverse proxy.

```
┌─────────────┐      ┌──────────────┐      ┌───────────────┐
│   Client    │ ───► │ Reverse Proxy│ ───► │  WSGI Server  │
│  (Browser)  │      │ (Nginx/IIS)  │      │ (Gunicorn/    │
└─────────────┘      └──────────────┘      │  Waitress)    │
                                           └───────────────┘
```

### Linux Deployment (Recommended)
**Stack**: Nginx + Gunicorn + Systemd

1. **Install Dependencies**:
   ```bash
   pip install gunicorn eventlet
   ```

2. **Systemd Service** (`/etc/systemd/system/aks-dashboard.service`):
   ```ini
   [Unit]
   Description=AKS Management Dashboard
   After=network.target

   [Service]
   User=aks-user
   Group=aks-user
   WorkingDirectory=/opt/aks-dashboard
   Environment="PATH=/opt/aks-dashboard/venv/bin"
   EnvironmentFile=/opt/aks-dashboard/.env
   ExecStart=/opt/aks-dashboard/venv/bin/gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 run:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. **Nginx Configuration** (`/etc/nginx/sites-available/aks-dashboard`):
   ```nginx
   server {
       listen 80;
       server_name dashboard.internal;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

### Windows Deployment
**Stack**: IIS + Waitress + Windows Service

1. **Install Dependencies**:
   ```bash
   pip install waitress
   ```

2. **Start Script** (`run_prod.py`):
   ```python
   from waitress import serve
   from run import app
   
   if __name__ == "__main__":
       serve(app, host='0.0.0.0', port=5000, threads=6)
   ```

3. **Run as Service**: Use NSSM (Non-Sucking Service Manager) to run `python run_prod.py` as a background service.

### Security Checklist
1. **HTTPS**: Always terminate SSL at the reverse proxy (Nginx/IIS).
2. **Secrets**: Use environment variables for sensitive data (`.env` file).
3. **User Identity**: Run the service as a dedicated non-root user.
4. **Firewall**: Restrict access to port 5000 (allow only localhost).
5. **Azure Auth**: Use Managed Identity where possible instead of Service Principals.

### Monitoring & Logging
- **Application Logs**: Stream to stdout/stderr (captured by Systemd/NSSM).
- **Audit Logs**: Persist `logs/audit/*.csv` to durable storage.
- **Health Check**: Monitor `/api/login/settings` endpoint for liveness.

---

## Dependencies (requirements.txt)

```
# Flask & Extensions
Flask>=3.0.0
Flask-SocketIO>=5.3.6
flask-cors>=4.0.0
python-dotenv>=1.0.0

# Azure SDK
azure-identity>=1.15.0
azure-mgmt-containerservice>=28.0.0
azure-mgmt-resource>=23.0.0

# Kubernetes
kubernetes>=28.1.0

# File Watching
watchdog>=3.0.0

# Utilities
python-dateutil>=2.8.2
requests>=2.31.0

# WebSocket
python-engineio>=4.8.0
python-socketio>=5.10.0
eventlet>=0.33.3

# Testing
pytest>=7.4.0
pytest-flask>=1.3.0
pytest-asyncio>=0.21.0
```

---

## Next Steps

1. **Review this plan** and confirm requirements
2. **Setup Azure environment** - verify `az login` works
3. **Create sample clusters_config.json** with your actual cluster details
4. **Begin Phase 1 implementation**

---

## Notes

- All kubectl commands are READ-ONLY - no destructive operations possible
- File watcher uses OS-native APIs (inotify on Linux, ReadDirectoryChangesW on Windows)
- WebSocket log streaming uses subprocess with proper cleanup
- Audit logs are stored locally in CSV format, rotated daily
- Theme preference persisted in browser localStorage

---

*Document Version: 1.0*  
*Created: December 10, 2025*  
*Project: AKS Management Dashboard*
