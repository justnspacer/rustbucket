# Quick Start: Testing Operator-Gatekeeper Integration

This guide will help you quickly test the integration between the Operator service and the Gatekeeper API Gateway.

## Prerequisites

1. Python 3.8+ installed
2. Both operator and gatekeeper services available
3. Dependencies installed (see below)

## Step 1: Install Dependencies

### For Operator
```bash
cd operator
python -m venv venv_operator  # If not already created
source venv_operator/Scripts/activate  # On Windows: venv_operator\Scripts\activate
pip install -r requirements.txt
```

### For Gatekeeper
```bash
cd gatekeeper
pip install -r requirements.txt
```

## Step 2: Configure Environment

Make sure your `operator/.env` file has the gatekeeper settings:

```bash
# Gatekeeper Configuration
GATEKEEPER_URL=http://localhost:8000
GATEKEEPER_TIMEOUT=30.0
SERVICE_NAME=operator
GATEKEEPER_AUTH_TOKEN=
```

## Step 3: Start Services

### Terminal 1 - Start Gatekeeper
```bash
cd gatekeeper
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Terminal 2 - Start Operator
```bash
cd operator
python app.py
```

You should see:
```
INFO:root:Initialized Gatekeeper client: http://localhost:8000
 * Running on http://0.0.0.0:5000
```

## Step 4: Test the Integration

### Option A: Using the Test Script (Recommended)

In a third terminal:

```bash
cd operator
python test_gatekeeper.py
```

Expected output:
```
============================================================
GATEKEEPER INTEGRATION TESTS
============================================================

Gatekeeper URL: http://localhost:8000
Service Name: operator
Timeout: 30.0s

============================================================
Testing Gatekeeper Health Check
============================================================
✅ Health check successful!
Status: healthy
Message: API Gateway is running
Available services: hue-dashboard, next-rusty-tech, nothing, operator, spotify, squirrel

============================================================
Testing Get Available Services
============================================================
✅ Service list retrieved successfully!

Found 6 services:
  - hue-dashboard: http://127.0.0.1:5000/api/hue-dashboard
  - next-rusty-tech: http://localhost:3000
  - nothing: http://127.0.0.1:5000/api/nothing
  - operator: http://127.0.0.1:5000/api/operator
  - spotify: http://spotify:5000/api/spotify
  - squirrel: http://localhost:8000/api/v1/

...

============================================================
TEST SUMMARY
============================================================
Health Check: ✅ PASSED
Get Services: ✅ PASSED
Client Lifecycle: ✅ PASSED
Proxy Request: ⚠️  FAILED (expected if services not running)

Total: 3/4 tests passed

🎉 All critical tests passed!
```

### Option B: Manual Testing with curl

#### Test 1: Get Gateway Info
```bash
curl http://localhost:5000/gateway
```

Expected response:
```json
{
  "gateway_url": "http://localhost:8000",
  "service_name": "operator",
  "timeout": 30.0,
  "status": "configured"
}
```

#### Test 2: Check Gateway Health
```bash
curl http://localhost:5000/gateway/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "API Gateway is running",
  "services": ["hue-dashboard", "next-rusty-tech", "nothing", "operator", "spotify", "squirrel"]
}
```

#### Test 3: List Gateway Services
```bash
curl http://localhost:5000/gateway/services
```

Expected response:
```json
{
  "services": {
    "hue-dashboard": "http://127.0.0.1:5000/api/hue-dashboard",
    "next-rusty-tech": "http://localhost:3000",
    "nothing": "http://127.0.0.1:5000/api/nothing",
    "operator": "http://127.0.0.1:5000/api/operator",
    "spotify": "http://spotify:5000/api/spotify",
    "squirrel": "http://localhost:8000/api/v1/"
  }
}
```

#### Test 4: Check Operator Health
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "operator"
}
```

### Option C: Testing with Python

```python
import asyncio
from config import GATEKEEPER_CONFIG
from gatekeeper_client import check_gatekeeper_health

async def test():
    result = await check_gatekeeper_health(GATEKEEPER_CONFIG)
    print(result)

asyncio.run(test())
```

## Step 5: Verify Integration

✅ **Success Indicators:**
- Gatekeeper responds to health checks
- Services list is returned
- No connection errors in logs
- Operator logs show: "Initialized Gatekeeper client"

❌ **Common Issues:**

### Issue: Connection Refused
```
Error: Connection refused
```
**Solution:** Make sure gatekeeper is running on port 8000

### Issue: Timeout
```
Error: Timeout waiting for connection
```
**Solution:** 
1. Check if gatekeeper is responding: `curl http://localhost:8000`
2. Increase `GATEKEEPER_TIMEOUT` in `.env`

### Issue: 404 Not Found
```
Error: 404 Not Found
```
**Solution:** Verify the endpoint URL in the request

### Issue: Import Errors
```
ModuleNotFoundError: No module named 'aiohttp'
```
**Solution:** 
```bash
pip install -r requirements.txt
```

## Step 6: Integration in Your Code

Once verified, you can use the client in your code:

```python
from gatekeeper_client import GatekeeperClientManager

# Get the initialized client
client = GatekeeperClientManager.get_client()

# Use it in async functions
async def my_function():
    # Check health
    health = await client.health_check()
    
    # Get services
    services = await client.get_services()
    
    # Make a proxied request
    response = await client.proxy_request(
        service_name='spotify',
        path='/api/spotify/search',
        method='GET'
    )
```

## Docker Testing

If using Docker Compose:

```bash
# Start services
docker-compose up gatekeeper operator

# In another terminal, test
docker-compose exec operator python test_gatekeeper.py
```

Update `.env` for Docker:
```bash
GATEKEEPER_URL=http://gatekeeper:8000
```

## Next Steps

- ✅ Integration working? Continue to [GATEKEEPER_INTEGRATION.md](GATEKEEPER_INTEGRATION.md)
- 📚 Want more details? See [INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md)
- 🔧 Need to customize? Check `gatekeeper_client.py` for available methods

## Getting Help

1. Check the logs in both services
2. Verify network connectivity
3. Ensure correct ports are open
4. Review the error messages in detail
5. Consult [GATEKEEPER_INTEGRATION.md](GATEKEEPER_INTEGRATION.md)

## Success Checklist

- [ ] Gatekeeper service running on port 8000
- [ ] Operator service running on port 5000
- [ ] Health check returns "healthy" status
- [ ] Services list contains expected services
- [ ] No connection errors in logs
- [ ] Test script passes core tests

If all items are checked, your integration is working! 🎉
