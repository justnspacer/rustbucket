"""Configuration for the Operator service."""

import os
from dotenv import load_dotenv

load_dotenv()


# Twilio Configuration
TWILIO_CONFIG = {
    'account_sid': os.getenv('TWILIO_ACCOUNT_SID'),
    'auth_token': os.getenv('TWILIO_AUTH_TOKEN'),
    'messaging_service_sid': os.getenv('TWILIO_MESSAGING_SERVICE_SID'),
    'from_number': os.getenv('TWILIO_FROM_NUMBER'),
    'to_number': os.getenv('TWILIO_TO_NUMBER'),
}

# Security Configuration
SECURITY_CONFIG = {
    'authorized_numbers': os.getenv('AUTHORIZED_NUMBERS', '').split(','),
    'twilio_auth_token': os.getenv('TWILIO_AUTH_TOKEN'),
}

# Prometheus Configuration
PROMETHEUS_CONFIG = {
    'prometheus_url': os.getenv('PROMETHEUS_URL', 'http://localhost:9090'),
}

# Datadog Configuration
DATADOG_CONFIG = {
    'datadog_api_key': os.getenv('DATADOG_API_KEY', ''),
    'datadog_app_key': os.getenv('DATADOG_APP_KEY', ''),
    'datadog_site': os.getenv('DATADOG_SITE', 'datadoghq.com'),
}

# Logs Configuration
LOGS_CONFIG = {
    'logs_type': os.getenv('LOGS_TYPE', 'elasticsearch'),  # elasticsearch, loki, cloudwatch
    'logs_url': os.getenv('LOGS_URL', 'http://localhost:9200'),
}

# Database Configuration
DATABASE_CONFIG = {
    'db_type': os.getenv('DB_TYPE', 'postgres'),
    'stats_url': os.getenv('DB_STATS_URL', ''),  # e.g., pgBouncer stats endpoint
}

# API Gateway Configuration
API_GATEWAY_CONFIG = {
    'gateway_type': os.getenv('GATEWAY_TYPE', 'kong'),  # kong, aws, custom
    'gateway_url': os.getenv('GATEWAY_URL', 'http://localhost:8001'),
    'admin_key': os.getenv('GATEWAY_ADMIN_KEY', ''),
}

# Gatekeeper Configuration
GATEKEEPER_CONFIG = {
    'gatekeeper_url': os.getenv('GATEKEEPER_URL', 'http://localhost:8000'),
    'gatekeeper_timeout': float(os.getenv('GATEKEEPER_TIMEOUT', '30.0')),
    'service_name': os.getenv('SERVICE_NAME', 'operator'),
    'auth_token': os.getenv('GATEKEEPER_AUTH_TOKEN', ''),  # Optional: for service-to-service auth
}

# Combined Monitor Configuration
MONITOR_CONFIG = {
    'prometheus': PROMETHEUS_CONFIG,
    'datadog': DATADOG_CONFIG,
    'logs': LOGS_CONFIG,
    'database': DATABASE_CONFIG,
    'api_gateway': API_GATEWAY_CONFIG,
}

# Flask Configuration
FLASK_CONFIG = {
    'host': os.getenv('FLASK_HOST', '0.0.0.0'),
    'port': int(os.getenv('FLASK_PORT', 5000)),
    'debug': os.getenv('FLASK_DEBUG', 'False').lower() == 'true',
}
