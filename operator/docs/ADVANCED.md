# Advanced Features Guide

## Alerting Integration

### Proactive Alerts

You can extend the Operator service to send proactive alerts when certain conditions are met. Here's an example implementation:

```python
# alerting.py
import asyncio
from command_processor import CommandProcessor
from sms import send_sms
from config import MONITOR_CONFIG, TWILIO_CONFIG

class AlertingService:
    """Service for proactive monitoring and alerting."""
    
    def __init__(self, config, alert_recipients):
        self.processor = CommandProcessor(config)
        self.alert_recipients = alert_recipients
        self.alert_rules = []
    
    def add_rule(self, name, check_func, threshold, message_template):
        """Add an alerting rule."""
        self.alert_rules.append({
            'name': name,
            'check': check_func,
            'threshold': threshold,
            'message': message_template
        })
    
    async def check_and_alert(self):
        """Check all rules and send alerts if needed."""
        for rule in self.alert_rules:
            value = await rule['check']()
            if value > rule['threshold']:
                message = rule['message'].format(value=value)
                await self.send_alert(rule['name'], message)
    
    async def send_alert(self, rule_name, message):
        """Send alert to all recipients."""
        for recipient in self.alert_recipients:
            send_sms(recipient, f"🚨 Alert: {message}", 
                    TWILIO_CONFIG['from_number'])

# Example usage
async def check_error_rate():
    """Example: Check error rate from Prometheus."""
    # Query error rate
    # Return percentage
    return 5.2

alerting = AlertingService(MONITOR_CONFIG, ['+1234567890'])
alerting.add_rule(
    'high_error_rate',
    check_error_rate,
    threshold=5.0,
    message_template='High error rate detected: {value}%'
)

# Run every 5 minutes
while True:
    await alerting.check_and_alert()
    await asyncio.sleep(300)
```

### Alert Examples

#### High CPU Usage
```python
async def check_cpu_usage():
    result = await prometheus.query({
        'query': 'avg(rate(process_cpu_seconds_total[5m])) * 100'
    })
    # Parse and return CPU percentage
    return cpu_percentage

alerting.add_rule('high_cpu', check_cpu_usage, 80.0,
    'CPU usage is {value}%')
```

#### High Error Rate
```python
async def check_error_rate():
    result = await prometheus.query({
        'query': '(sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100'
    })
    return error_rate

alerting.add_rule('high_errors', check_error_rate, 5.0,
    'Error rate is {value}%')
```

#### Database Connection Pool
```python
async def check_db_connections():
    result = await database.query({'metric': 'connections'})
    return result['data']['active_connections']

alerting.add_rule('db_connections', check_db_connections, 90,
    'Database has {value} active connections')
```

## Natural Language Processing (Future)

### Concept

Instead of rigid command syntax, allow natural language queries:

```python
# Future NLP integration
from transformers import pipeline

nlp = pipeline('text-classification', model='intent-classifier')

def parse_intent(message):
    """Parse user intent from message."""
    intent = nlp(message)[0]
    
    if intent['label'] == 'check_metrics':
        # Extract metric name
        return ('metrics', extract_metric(message))
    elif intent['label'] == 'search_logs':
        # Extract search term
        return ('logs', extract_search_term(message))
    # ... more intents

# Examples:
# "How's the CPU looking?" → metrics cpu_usage
# "Any errors in the last hour?" → logs error
# "What's the database status?" → db status
```

### Intent Examples

**User:** "Is everything ok?"
**Bot:** Status check across all systems

**User:** "Show me memory usage"
**Bot:** Query memory metrics

**User:** "Find errors with payment"
**Bot:** Search logs for "payment" and "error"

## API Integration Examples

### Custom Monitoring Endpoint

Create a monitor for your custom API:

```python
# monitors/custom_api_monitor.py
from .base_monitor import BaseMonitor
import aiohttp

class CustomAPIMonitor(BaseMonitor):
    """Monitor for custom application API."""
    
    async def query(self, query_params):
        endpoint = query_params.get('endpoint', 'metrics')
        url = f"{self.config['api_url']}/api/{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {'status': 'success', 'data': data}
                return {'status': 'error', 'message': f'Status {response.status}'}
    
    def format_response(self, data):
        if data['status'] == 'error':
            return f"❌ {data['message']}"
        
        metrics = data['data']
        return f"📊 API Metrics:\nRequests: {metrics['requests']}\nLatency: {metrics['latency']}ms"
```

### New Relic Integration

```python
# monitors/newrelic_monitor.py
from .base_monitor import BaseMonitor
import aiohttp

class NewRelicMonitor(BaseMonitor):
    """Monitor for New Relic APM."""
    
    def __init__(self, config):
        super().__init__(config)
        self.api_key = config.get('newrelic_api_key')
        self.account_id = config.get('newrelic_account_id')
        self.base_url = 'https://api.newrelic.com/v2'
    
    async def query(self, query_params):
        nrql = query_params.get('query', '')
        
        url = f"{self.base_url}/applications.json"
        headers = {
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {'status': 'success', 'data': data}
                return {'status': 'error', 'message': f'Status {response.status}'}
    
    def format_response(self, data):
        if data['status'] == 'error':
            return f"❌ {data['message']}"
        
        apps = data['data'].get('applications', [])
        if not apps:
            return "📊 No applications found"
        
        lines = ["📊 New Relic Apps:"]
        for app in apps[:3]:
            name = app['name']
            health = app.get('health_status', 'unknown')
            lines.append(f"{health} {name}")
        
        return "\n".join(lines)
```

## Webhook Integration

### Receive Alerts from Other Systems

Set up endpoints to receive webhooks from monitoring systems:

```python
# In app.py, add:

@app.route('/webhook/prometheus', methods=['POST'])
def prometheus_webhook():
    """Receive alerts from Prometheus Alertmanager."""
    alert_data = request.json
    
    for alert in alert_data.get('alerts', []):
        if alert['status'] == 'firing':
            message = f"🚨 {alert['labels']['alertname']}: {alert['annotations']['summary']}"
            
            # Send to authorized users
            for number in security.get_authorized_numbers():
                send_sms(number, message, TWILIO_CONFIG['from_number'])
    
    return {'status': 'ok'}, 200

@app.route('/webhook/datadog', methods=['POST'])
def datadog_webhook():
    """Receive alerts from Datadog."""
    alert_data = request.json
    
    message = f"🚨 Datadog Alert: {alert_data.get('title', 'Unknown')}"
    
    for number in security.get_authorized_numbers():
        send_sms(number, message, TWILIO_CONFIG['from_number'])
    
    return {'status': 'ok'}, 200
```

## Rate Limiting

Prevent abuse with rate limiting:

```python
# rate_limiter.py
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    """Simple rate limiter for SMS commands."""
    
    def __init__(self, max_requests=10, window_minutes=5):
        self.max_requests = max_requests
        self.window = timedelta(minutes=window_minutes)
        self.requests = defaultdict(list)
    
    def is_allowed(self, phone_number):
        """Check if request is allowed."""
        now = datetime.now()
        cutoff = now - self.window
        
        # Remove old requests
        self.requests[phone_number] = [
            ts for ts in self.requests[phone_number]
            if ts > cutoff
        ]
        
        # Check limit
        if len(self.requests[phone_number]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[phone_number].append(now)
        return True

# Use in app.py
rate_limiter = RateLimiter(max_requests=10, window_minutes=5)

@app.route('/sms', methods=['POST'])
def sms_webhook():
    from_number = request.form.get('From', '')
    
    if not rate_limiter.is_allowed(from_number):
        response = MessagingResponse()
        response.message("⚠️ Rate limit exceeded. Please wait a few minutes.")
        return str(response)
    
    # ... rest of handler
```

## Logging and Monitoring

Add comprehensive logging:

```python
# logging_config.py
import logging
import logging.handlers
import os

def setup_logging():
    """Configure logging for the application."""
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/operator.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# In app.py:
from logging_config import setup_logging
logger = setup_logging()

# Log all commands
logger.info(f"Command from {from_number}: {message_body}")
logger.info(f"Response to {from_number}: {response_text}")
```

## Dashboard (Future)

Create a web dashboard to view command history:

```python
# dashboard.py (separate Flask app or add routes to app.py)

@app.route('/dashboard')
def dashboard():
    """Show command history and statistics."""
    return render_template('dashboard.html', 
                         commands=get_recent_commands(),
                         stats=get_statistics())

def get_recent_commands():
    """Get recent command history from database."""
    # Query from database
    return [
        {'timestamp': '2025-10-14 10:30', 'user': '+1234567890', 
         'command': 'status', 'response': 'All systems healthy'},
        # ...
    ]

def get_statistics():
    """Get usage statistics."""
    return {
        'total_commands': 1234,
        'unique_users': 5,
        'most_used_command': 'status',
        'avg_response_time': '1.2s'
    }
```

## Best Practices

1. **Security First**: Always verify Twilio signatures in production
2. **Rate Limiting**: Prevent abuse and excessive queries
3. **Error Handling**: Gracefully handle all errors with user-friendly messages
4. **Monitoring**: Monitor the monitoring service itself!
5. **Logging**: Log all commands and responses for audit
6. **Testing**: Test all integrations before deploying
7. **Documentation**: Keep commands and responses clear and concise
8. **SMS Limits**: Keep responses under 160 characters when possible

## Performance Tips

1. **Caching**: Cache monitoring data for short periods
2. **Async**: Use async/await for all I/O operations
3. **Timeouts**: Set reasonable timeouts on all HTTP requests
4. **Connection Pooling**: Reuse HTTP connections
5. **Background Workers**: Use Celery for long-running tasks

## Example Production Setup

```python
# production.py
import gunicorn

bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
timeout = 30
keepalive = 5

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"

# Process naming
proc_name = "operator"

# Server mechanics
daemon = False
pidfile = "operator.pid"
```

Run with:
```bash
gunicorn -c production.py app:app
```
