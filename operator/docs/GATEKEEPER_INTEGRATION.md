# Operator-Gatekeeper Integration

This document describes the integration between the Operator service and the Gatekeeper API Gateway.

## Overview

The Operator service now includes a client to communicate with the Gatekeeper API Gateway. This allows the Operator to:

- Check gateway health status
- List available services in the ecosystem
- Make proxied requests to other services through the gateway
- Prepare for future dynamic service registration

## Configuration

### Environment Variables

Add the following to your `.env` file in the `operator/` directory:

```bash
# Gatekeeper Configuration
GATEKEEPER_URL=http://localhost:8000
GATEKEEPER_TIMEOUT=30.0
SERVICE_NAME=operator
GATEKEEPER_AUTH_TOKEN=
```

### Docker Compose Setup

When running in Docker, update the `GATEKEEPER_URL` to use the service name:

```bash
GATEKEEPER_URL=http://gatekeeper:8000
```

## Usage

### Python API

#### Initialize the Client

The client is automatically initialized when the Flask app starts:

```python
from gatekeeper_client import GatekeeperClientManager
from config import GATEKEEPER_CONFIG

# Already done in app.py
client = GatekeeperClientManager.get_client()
```

#### Check Gateway Health

```python
from gatekeeper_client import check_gatekeeper_health
from config import GATEKEEPER_CONFIG

health = await check_gatekeeper_health(GATEKEEPER_CONFIG)
print(health)
```

#### Get Available Services

```python
from gatekeeper_client import get_available_services
from config import GATEKEEPER_CONFIG

services = await get_available_services(GATEKEEPER_CONFIG)
print(services)
```

#### Make Proxied Requests

```python
# Get the singleton client
client = GatekeeperClientManager.get_client()

# Make a request through the gateway
response = await client.proxy_request(
    service_name='spotify',
    path='/api/spotify/search',
    method='GET',
    data={'query': 'Beatles'},
    headers={'X-Custom-Header': 'value'}
)
```

### REST API Endpoints

The Operator service exposes the following endpoints for gateway interaction:

#### 1. Gateway Information
```bash
GET http://localhost:5000/gateway
```

Returns configuration information about the gateway connection.

**Response:**
```json
{
  "gateway_url": "http://localhost:8000",
  "service_name": "operator",
  "timeout": 30.0,
  "status": "configured"
}
```

#### 2. Gateway Health Check
```bash
GET http://localhost:5000/gateway/health
```

Checks if the Gatekeeper gateway is healthy and accessible.

**Response:**
```json
{
  "status": "healthy",
  "message": "API Gateway is running",
  "services": ["spotify", "squirrel", "operator", ...]
}
```

#### 3. List Gateway Services
```bash
GET http://localhost:5000/gateway/services
```

Retrieves the list of services registered with the gateway.

**Response:**
```json
{
  "services": {
    "spotify": "http://spotify:5000/api/spotify",
    "squirrel": "http://localhost:8000/api/v1/",
    "operator": "http://127.0.0.1:5000/api/operator"
  }
}
```

## Architecture

### Components

1. **GatekeeperClient**: Core client class for making requests to the gateway
2. **GatekeeperClientManager**: Singleton manager to ensure one client instance
3. **Helper Functions**: Convenience functions for common operations

### Flow Diagram

```
┌─────────────┐
│   Operator  │
│   Service   │
└──────┬──────┘
       │
       │ HTTP Requests
       │
       ▼
┌─────────────────┐
│   Gatekeeper    │
│   API Gateway   │
└────────┬────────┘
         │
         │ Routes & Proxies
         │
    ┌────┴─────┬────────┬──────────┐
    ▼          ▼        ▼          ▼
┌────────┐ ┌───────┐ ┌──────┐ ┌──────┐
│Spotify │ │Squirrel│ │Next  │ │ ... │
└────────┘ └────────┘ └──────┘ └──────┘
```

## Features

### Current Features

- ✅ Health check integration
- ✅ Service discovery
- ✅ Proxied requests through gateway
- ✅ Configurable timeouts
- ✅ Error handling and logging
- ✅ Async support with aiohttp

### Future Enhancements

- 🔄 Dynamic service registration
- 🔄 JWT token integration for authenticated requests
- 🔄 Circuit breaker pattern for fault tolerance
- 🔄 Request retry logic
- 🔄 Metrics and monitoring integration

## Error Handling

The client includes comprehensive error handling:

- **Connection Errors**: Logged and re-raised for caller to handle
- **Timeouts**: Configurable timeout with sensible defaults
- **HTTP Errors**: Status codes and error responses properly handled
- **Logging**: All operations logged for debugging

## Testing

### Manual Testing

1. Start the Gatekeeper service:
```bash
cd gatekeeper
python main.py
```

2. Start the Operator service:
```bash
cd operator
python app.py
```

3. Test the gateway endpoints:
```bash
# Check gateway info
curl http://localhost:5000/gateway

# Check gateway health
curl http://localhost:5000/gateway/health

# List services
curl http://localhost:5000/gateway/services
```

### Integration with Docker

To run both services with Docker Compose:

```bash
docker-compose up gatekeeper operator
```

## Troubleshooting

### Connection Refused
- Ensure Gatekeeper service is running
- Check `GATEKEEPER_URL` is correct
- Verify network connectivity (especially in Docker)

### Timeout Errors
- Increase `GATEKEEPER_TIMEOUT` in .env
- Check if Gatekeeper is responding slowly

### Authentication Errors
- Verify `GATEKEEPER_AUTH_TOKEN` if using authentication
- Check token format and validity

## Dependencies

The following Python packages are required:

- `aiohttp`: Async HTTP client
- `python-dotenv`: Environment variable management
- `flask`: Web framework (already installed)

All dependencies are included in `requirements.txt`.

## Security Considerations

1. **Authentication**: Use `GATEKEEPER_AUTH_TOKEN` for service-to-service authentication
2. **HTTPS**: Use HTTPS URLs in production
3. **Token Storage**: Never commit tokens to version control
4. **Rate Limiting**: Be aware of gateway rate limits
5. **Network Isolation**: Use Docker networks to isolate services

## Contributing

When adding new gateway integration features:

1. Update `gatekeeper_client.py` with new methods
2. Add corresponding Flask endpoints in `app.py` if needed
3. Update this README with usage examples
4. Add appropriate error handling and logging
5. Test thoroughly with the actual Gatekeeper service

## References

- [Gatekeeper Service Documentation](../gatekeeper/README.md)
- [Operator Service Documentation](./README.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [aiohttp Documentation](https://docs.aiohttp.org/)
