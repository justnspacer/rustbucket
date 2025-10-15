# Operator - Architecture Overview

## System Flow Diagram

```
┌─────────────┐
│   User's    │
│   Phone     │
└──────┬──────┘
       │ SMS: "status"
       │
       ▼
┌─────────────────────────────────────────┐
│            Twilio Cloud                 │
│  - Receives SMS                         │
│  - Forwards to webhook                  │
└──────────────┬──────────────────────────┘
               │ HTTP POST
               │ /sms
               ▼
┌─────────────────────────────────────────┐
│         Flask Application               │
│              (app.py)                   │
│                                         │
│  ┌────────────────────────────────┐    │
│  │   Security Layer               │    │
│  │  - Verify Twilio Signature     │    │
│  │  - Check Authorized Numbers    │    │
│  └────────────┬───────────────────┘    │
│               │                         │
│               ▼                         │
│  ┌────────────────────────────────┐    │
│  │   Command Processor            │    │
│  │  - Parse message               │    │
│  │  - Route to handler            │    │
│  └────────────┬───────────────────┘    │
└───────────────┼─────────────────────────┘
                │
        ┌───────┴────────┐
        │                │
        ▼                ▼
┌───────────────┐  ┌──────────────┐
│   Monitors    │  │  Direct      │
│   Layer       │  │  Commands    │
└───────┬───────┘  └──────────────┘
        │
   ┌────┴────┬─────────┬──────────┬──────────┐
   │         │         │          │          │
   ▼         ▼         ▼          ▼          ▼
┌─────┐  ┌─────┐  ┌─────┐  ┌──────┐  ┌──────────┐
│Prom │  │Data │  │Logs │  │  DB  │  │ Gateway  │
│etheus│ │dog  │  │     │  │      │  │          │
└──┬──┘  └──┬──┘  └──┬──┘  └───┬──┘  └────┬─────┘
   │        │        │         │          │
   │        │        │         │          │
   ▼        ▼        ▼         ▼          ▼
┌──────────────────────────────────────────────┐
│         External Monitoring Systems          │
│  - Prometheus Server                         │
│  - Datadog API                              │
│  - Elasticsearch / Loki                     │
│  - pgBouncer / Database Stats               │
│  - Kong / API Gateway                       │
└──────────────────────────────────────────────┘
```

## Component Architecture

```
operator/
│
├── Web Layer (Flask)
│   └── app.py
│       ├── /sms endpoint      → Receives webhooks
│       ├── /health endpoint   → Health checks
│       └── / endpoint         → Service info
│
├── Processing Layer
│   ├── command_processor.py   → Command parsing & routing
│   ├── security.py            → Auth & verification
│   └── config.py              → Configuration management
│
├── Monitoring Layer
│   └── monitors/
│       ├── base_monitor.py         → Abstract base class
│       ├── prometheus_monitor.py   → Prometheus integration
│       ├── datadog_monitor.py      → Datadog integration
│       ├── logs_monitor.py         → Logs (ES/Loki)
│       ├── database_monitor.py     → DB statistics
│       └── api_gateway_monitor.py  → API Gateway stats
│
└── Utilities Layer
    ├── sms.py                 → SMS sending utilities
    └── test_*.py              → Testing utilities
```

## Data Flow for "status" Command

```
1. User sends SMS: "status"
   ↓
2. Twilio receives SMS
   ↓
3. Twilio POSTs to /sms webhook
   ↓
4. Security Layer
   ├─ Verify Twilio signature ✓
   └─ Check authorized number ✓
   ↓
5. Command Processor
   ├─ Parse: command="status", args=""
   └─ Route to: _cmd_status()
   ↓
6. Health Checks (Parallel)
   ├─ Prometheus.health_check() → ✅
   ├─ Datadog.health_check()    → ✅
   ├─ Logs.health_check()       → ❌
   ├─ Database.health_check()   → ✅
   └─ Gateway.health_check()    → ✅
   ↓
7. Format Response
   "📊 System Status:
    ✅ Prometheus
    ✅ Datadog
    ❌ Logs
    ✅ Database
    ✅ Gateway"
   ↓
8. Send via Twilio TwiML
   ↓
9. User receives SMS response
```

## Request/Response Flow

```
┌─────────┐                                      ┌──────────┐
│  User   │                                      │  Twilio  │
└────┬────┘                                      └────┬─────┘
     │                                                │
     │ SMS: "metrics cpu"                            │
     ├──────────────────────────────────────────────►│
     │                                                │
     │                              POST /sms        │
     │                         ┌────────────────────►├─┐
     │                         │                     │ │
     │                         │                     │ │ Signature
┌────┴──────┐                 │                     │ │ Included
│  Operator │◄────────────────┘                     │ │
│  Service  │                                        │◄┘
└────┬──────┘                                        │
     │                                                │
     │ 1. Verify signature                           │
     │ 2. Check authorization                        │
     │ 3. Process "metrics cpu"                      │
     │    ├─ Query Prometheus                        │
     │    └─ Format response                         │
     │                                                │
     │                            TwiML Response      │
     ├───────────────────────────────────────────────►│
     │                                                │
     │                                   SMS: Result  │
     │◄───────────────────────────────────────────────┤
     │                                                │
```

## Monitor Interface Pattern

All monitors implement the same interface:

```python
class BaseMonitor:
    async def query(params) → Dict
    async def health_check() → bool
    def format_response(data) → str
```

This allows:
- Easy addition of new monitors
- Consistent command handling
- Standardized responses
- Simple testing

## Configuration Flow

```
.env file
    ↓
config.py (loads environment)
    ↓
MONITOR_CONFIG dict
    ↓
    ├─► PrometheusMonitor(config['prometheus'])
    ├─► DatadogMonitor(config['datadog'])
    ├─► LogsMonitor(config['logs'])
    ├─► DatabaseMonitor(config['database'])
    └─► APIGatewayMonitor(config['api_gateway'])
```

## Security Layers

```
Incoming Request
    │
    ▼
┌─────────────────────────────┐
│  Layer 1: Network           │
│  - HTTPS required           │
│  - Firewall rules           │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│  Layer 2: Twilio Signature  │
│  - HMAC SHA256 verification │
│  - Validates source         │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│  Layer 3: Phone Number      │
│  - Check authorized list    │
│  - Reject unknown numbers   │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│  Layer 4: Rate Limiting     │
│  - (Optional, see ADVANCED) │
└────────────┬────────────────┘
             │
             ▼
        Process Request
```

## Async Operation Pattern

```python
# Synchronous Flask handler
@app.route('/sms', methods=['POST'])
def sms_webhook():
    message = request.form.get('Body')
    
    # Create new event loop for async processing
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Run async command processor
    response = loop.run_until_complete(
        command_processor.process(message)
    )
    
    loop.close()
    return create_response(response)

# Async command processing
async def process(message):
    # All monitors use async HTTP calls
    result = await prometheus.query(params)
    return format(result)
```

## Deployment Topology

### Local Development
```
Developer Machine
  ├── Flask (localhost:5000)
  └── ngrok tunnel
      └── https://abc123.ngrok.io
          └── Twilio webhook
```

### Production
```
Load Balancer (HTTPS)
    │
    ├── App Server 1
    │   └── Gunicorn → Flask
    │
    ├── App Server 2
    │   └── Gunicorn → Flask
    │
    └── App Server 3
        └── Gunicorn → Flask
```

## Monitoring the Monitor

The service itself should be monitored:

```
Operator Service
    │
    ├─► Prometheus /metrics endpoint
    │   (requests, latency, errors)
    │
    ├─► Health check endpoint
    │   (monitored by uptime service)
    │
    ├─► Logs
    │   (sent to centralized logging)
    │
    └─► Alerts
        (if service is down)
```

## Extension Points

Easy to extend:

1. **New Monitor**: Create class in `monitors/`
2. **New Command**: Add method to `CommandProcessor`
3. **New Auth Method**: Extend `Security` class
4. **New Response Format**: Override `format_response()`
5. **Webhooks**: Add routes to `app.py`

## Technology Stack

```
┌──────────────────────────────────────┐
│         Application Layer            │
│  Python 3.11+                        │
│  Flask 3.1.0 (Web Framework)         │
└──────────────────┬───────────────────┘
                   │
┌──────────────────┴───────────────────┐
│         Libraries                    │
│  aiohttp 3.11 (Async HTTP)          │
│  Twilio 9.5 (SMS)                   │
│  python-dotenv (Config)             │
└──────────────────┬───────────────────┘
                   │
┌──────────────────┴───────────────────┐
│         External Services            │
│  Twilio (SMS Gateway)               │
│  Prometheus, Datadog, etc.          │
└──────────────────────────────────────┘
```

---

This architecture provides:
- ✅ Modular design
- ✅ Easy to extend
- ✅ Security built-in
- ✅ Async performance
- ✅ Testable components
