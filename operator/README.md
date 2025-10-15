# Operator
A Command Processing Service for SMS-based Monitoring

## Overview

Operator is an SMS-based command interface for monitoring and querying your infrastructure. Send SMS commands to check system health, query metrics, search logs, and monitor your API gateways—all from your phone.

**New**: Now integrated with the Gatekeeper API Gateway for seamless service-to-service communication. See [GATEKEEPER_INTEGRATION.md](GATEKEEPER_INTEGRATION.md) for details.

## Features

✅ **Implemented:**
- ✅ Receives SMS webhooks from Twilio
- ✅ Parses and executes commands from messages
- ✅ Queries monitoring systems (Prometheus, Datadog, Logs, Database, API Gateway)
- ✅ Sends formatted responses back via SMS
- ✅ Security: Phone number authorization and Twilio signature verification
- ✅ Flask webhook server with health checks
- ✅ Async monitoring integrations
- ✅ **Gatekeeper integration for service discovery and proxied requests**

## Monitoring & Data Sources

### Currently Supported:
- **Application metrics**: Prometheus, Datadog
- **Logs**: Elasticsearch, Loki (CloudWatch ready)
- **Database stats**: pgBouncer stats, custom DB endpoints
- **API Gateway metrics**: Kong, AWS API Gateway, custom metrics
- **Health endpoints**: Individual health checks for each service
- **Gateway Integration**: Gatekeeper API Gateway for service mesh communication

## Quick Start

See [SETUP.md](SETUP.md) for detailed setup instructions.

```bash
# 1. Copy and configure environment
cp .env.example .env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python app.py

# 4. Configure Twilio webhook to point to your /sms endpoint
```

## Usage Examples

Send these commands via SMS:

- `help` - Show available commands
- `status` - Get system overview
- `metrics cpu_usage` - Query CPU metrics
- `logs error` - Search for errors in logs
- `db connections` - Get database connection stats
- `gateway status` - Check API gateway status
- `health` - Health check all systems

## Architecture

```
SMS → Twilio → Flask Webhook → Command Processor → Monitors → Response → SMS
                    ↓
              Security Layer
           (Auth + Signature)
```

## Project Structure

```
operator/
├── app.py                    # Flask webhook application
├── command_processor.py      # Command parser and executor
├── security.py              # Authentication and authorization
├── config.py                # Configuration management
├── sms.py                   # SMS utilities
├── monitors/                # Monitoring integrations
│   ├── prometheus_monitor.py
│   ├── datadog_monitor.py
│   ├── logs_monitor.py
│   ├── database_monitor.py
│   └── api_gateway_monitor.py
├── requirements.txt
├── .env.example
└── SETUP.md                 # Detailed setup guide
```

## Enhanced Features (Roadmap)

- [ ] **Alerting Integration**: Send proactive alerts (e.g., "High error rate detected")
- [ ] **Natural Language Processing**: Parse natural language queries
- [ ] **Rate Limiting**: Prevent abuse and excessive queries
- [ ] **Command History**: Track and review past commands
- [ ] **Multi-user Support**: Team-based access controls
- [ ] **New Relic Integration**: Additional APM monitoring
- [ ] **Grafana Integration**: Query Grafana dashboards

## Security

- **Phone Number Authorization**: Only configured numbers can execute commands
- **Twilio Signature Verification**: Validates requests come from Twilio
- **HTTPS Required**: Production deployment requires HTTPS
- **Environment-based Secrets**: All credentials in environment variables

## Contributing

To add new commands or monitoring integrations, see the development section in [SETUP.md](SETUP.md).

## License

[Your License Here]
