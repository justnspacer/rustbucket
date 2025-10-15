# Operator - Setup Guide

## Quick Start

### 1. Environment Setup

Copy the example environment file and configure it with your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual configuration values.

### 2. Install Dependencies

```bash
# Activate virtual environment (if not already activated)
source venv_operator/bin/activate  # On Windows: venv_operator\Scripts\activate

# Install/upgrade requirements
pip install -r requirements.txt
```

### 3. Run the Application

```bash
# Start the Flask webhook server
python app.py
```

The server will start on `http://0.0.0.0:5000` by default.

### 4. Configure Twilio Webhook

1. Log in to your [Twilio Console](https://console.twilio.com/)
2. Go to Phone Numbers → Manage → Active Numbers
3. Select your number
4. Under "Messaging Configuration":
   - Set "A MESSAGE COMES IN" webhook to: `https://your-domain.com/sms`
   - Method: `POST`
5. Save the configuration

**Note**: For local development, use [ngrok](https://ngrok.com/) to expose your local server:

```bash
ngrok http 5000
```

Then use the ngrok URL (e.g., `https://abc123.ngrok.io/sms`) as your Twilio webhook.

## Configuration Guide

### Required Environment Variables

```bash
# Twilio credentials (required)
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=your_token
TWILIO_MESSAGING_SERVICE_SID=MGxxxxx
TWILIO_FROM_NUMBER=+1234567890

# Security
AUTHORIZED_NUMBERS=+1234567890,+0987654321
```

### Monitoring System Configuration

#### Prometheus
```bash
PROMETHEUS_URL=http://prometheus.example.com:9090
```

#### Datadog
```bash
DATADOG_API_KEY=your_api_key
DATADOG_APP_KEY=your_app_key
DATADOG_SITE=datadoghq.com  # or datadoghq.eu for EU
```

#### Logs (Elasticsearch/Loki/CloudWatch)
```bash
LOGS_TYPE=elasticsearch  # or loki, cloudwatch
LOGS_URL=http://elasticsearch.example.com:9200
```

#### Database Monitoring
```bash
DB_TYPE=postgres
DB_STATS_URL=http://pgbouncer.example.com:9200/stats
```

#### API Gateway
```bash
GATEWAY_TYPE=kong  # or aws, custom
GATEWAY_URL=http://kong.example.com:8001
GATEWAY_ADMIN_KEY=your_admin_key
```

## Available SMS Commands

Send these commands via SMS to your Twilio number:

### General Commands

- `help` - Show available commands
- `status` - Get system overview
- `health` - Health check all systems
- `health <system>` - Check specific system (prometheus, datadog, logs, db, gateway)

### Monitoring Commands

- `metrics <query>` - Query metrics from Prometheus/Datadog
  - Example: `metrics cpu_usage`
  - Example: `metrics http_requests_total`

- `logs <query>` - Search logs
  - Example: `logs error`
  - Example: `logs 500`

- `db` - Get database statistics
  - Example: `db connections`

- `gateway` - Get API gateway statistics
  - Example: `gateway status`

## Development

### Project Structure

```
operator/
├── app.py                    # Flask webhook application
├── main.py                   # Original SMS sender (testing)
├── sms.py                    # SMS utilities
├── command_processor.py      # Command parser and executor
├── security.py              # Authentication and authorization
├── config.py                # Configuration loader
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment file
├── monitors/               # Monitoring integrations
│   ├── __init__.py
│   ├── base_monitor.py
│   ├── prometheus_monitor.py
│   ├── datadog_monitor.py
│   ├── logs_monitor.py
│   ├── database_monitor.py
│   └── api_gateway_monitor.py
└── venv_operator/          # Virtual environment
```

### Testing Locally

1. **Test SMS sending** (using original main.py):
```bash
python main.py
```

2. **Test webhook endpoint**:
```bash
# Send a test POST request
curl -X POST http://localhost:5000/sms \
  -d "From=+1234567890" \
  -d "Body=help"
```

3. **Test monitoring integrations**:
```python
# Create a test script
import asyncio
from monitors import PrometheusMonitor

async def test():
    monitor = PrometheusMonitor({'prometheus_url': 'http://localhost:9090'})
    result = await monitor.query({'query': 'up'})
    print(monitor.format_response(result))

asyncio.run(test())
```

### Security Notes

1. **Twilio Signature Verification**: The app verifies all incoming webhooks are from Twilio
2. **Phone Number Authorization**: Only authorized numbers can execute commands
3. **HTTPS Required**: Use HTTPS in production (Twilio requirement)
4. **Environment Variables**: Never commit `.env` file to version control

### Adding New Commands

To add a new command:

1. Add method to `CommandProcessor` class in `command_processor.py`:
```python
async def _cmd_mycommand(self, args: str) -> str:
    """My new command."""
    # Implementation here
    return "Result"
```

2. Register it in the `__init__` method:
```python
self.commands = {
    # ... existing commands
    'mycommand': self._cmd_mycommand,
}
```

3. Update help text to include the new command.

### Adding New Monitors

To add a new monitoring integration:

1. Create new file in `monitors/` directory (e.g., `new_monitor.py`)
2. Extend `BaseMonitor` class
3. Implement required methods: `query()`, `health_check()`, `format_response()`
4. Add to `monitors/__init__.py`
5. Initialize in `CommandProcessor`
6. Add configuration to `config.py`

## Deployment

### Using systemd (Linux)

Create `/etc/systemd/system/operator.service`:

```ini
[Unit]
Description=Operator SMS Command Service
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/operator
Environment="PATH=/path/to/operator/venv_operator/bin"
ExecStart=/path/to/operator/venv_operator/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable operator
sudo systemctl start operator
sudo systemctl status operator
```

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t operator .
docker run -p 5000:5000 --env-file .env operator
```

### Using Gunicorn (Production)

Install gunicorn:
```bash
pip install gunicorn
```

Run:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

### Common Issues

1. **"Import could not be resolved" errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **Twilio signature verification fails**
   - Check that `TWILIO_AUTH_TOKEN` is correct
   - Ensure webhook URL matches exactly (including https://)
   - For local testing, you can temporarily disable verification

3. **Monitoring endpoints timeout**
   - Verify monitoring URLs are accessible
   - Check firewall/network settings
   - Increase timeout in monitor classes if needed

4. **Unauthorized number error**
   - Add your number to `AUTHORIZED_NUMBERS` in `.env`
   - Use E.164 format: `+1234567890`

## Next Steps

- [ ] Set up alerting integration for proactive notifications
- [ ] Add NLP for natural language queries
- [ ] Implement rate limiting
- [ ] Add logging to file/external service
- [ ] Create dashboard for command history
- [ ] Add more monitoring integrations (New Relic, etc.)
