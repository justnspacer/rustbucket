"""
Example script to test monitoring integrations locally.

Run this to verify your monitoring endpoints are configured correctly.
"""

import asyncio
from monitors import (
    PrometheusMonitor,
    DatadogMonitor,
    LogsMonitor,
    DatabaseMonitor,
    APIGatewayMonitor
)
from config import MONITOR_CONFIG


async def test_prometheus():
    """Test Prometheus integration."""
    print("\n=== Testing Prometheus ===")
    monitor = PrometheusMonitor(MONITOR_CONFIG.get('prometheus', {}))
    
    # Health check
    healthy = await monitor.health_check()
    print(f"Health: {'✅ Healthy' if healthy else '❌ Unhealthy'}")
    
    if healthy:
        # Test query
        result = await monitor.query({'query': 'up'})
        print(f"Query result: {monitor.format_response(result)}")


async def test_datadog():
    """Test Datadog integration."""
    print("\n=== Testing Datadog ===")
    monitor = DatadogMonitor(MONITOR_CONFIG.get('datadog', {}))
    
    # Health check
    healthy = await monitor.health_check()
    print(f"Health: {'✅ Healthy' if healthy else '❌ Unhealthy'}")
    
    if healthy:
        # Test query
        result = await monitor.query({
            'query': 'avg:system.cpu.user{*}',
            'from': 'now-1h',
            'to': 'now'
        })
        print(f"Query result: {monitor.format_response(result)}")


async def test_logs():
    """Test Logs integration."""
    print("\n=== Testing Logs ===")
    monitor = LogsMonitor(MONITOR_CONFIG.get('logs', {}))
    
    # Health check
    healthy = await monitor.health_check()
    print(f"Health: {'✅ Healthy' if healthy else '❌ Unhealthy'}")
    
    if healthy:
        # Test query based on type
        if monitor.logs_type == 'elasticsearch':
            result = await monitor.query({
                'index': 'logs-*',
                'query': {'match_all': {}},
                'size': 3
            })
        elif monitor.logs_type == 'loki':
            result = await monitor.query({
                'query': '{job="app"}',
                'limit': 3
            })
        else:
            result = {'status': 'error', 'message': 'Unsupported logs type'}
        
        print(f"Query result: {monitor.format_response(result)}")


async def test_database():
    """Test Database integration."""
    print("\n=== Testing Database ===")
    monitor = DatabaseMonitor(MONITOR_CONFIG.get('database', {}))
    
    # Health check
    healthy = await monitor.health_check()
    print(f"Health: {'✅ Healthy' if healthy else '❌ Unhealthy'}")
    
    if healthy:
        # Test query
        result = await monitor.query({'metric': 'connections'})
        print(f"Query result: {monitor.format_response(result)}")


async def test_api_gateway():
    """Test API Gateway integration."""
    print("\n=== Testing API Gateway ===")
    monitor = APIGatewayMonitor(MONITOR_CONFIG.get('api_gateway', {}))
    
    # Health check
    healthy = await monitor.health_check()
    print(f"Health: {'✅ Healthy' if healthy else '❌ Unhealthy'}")
    
    if healthy:
        # Test query
        result = await monitor.query({'endpoint': 'status'})
        print(f"Query result: {monitor.format_response(result)}")


async def test_all():
    """Run all tests."""
    print("=" * 50)
    print("TESTING MONITORING INTEGRATIONS")
    print("=" * 50)
    
    await test_prometheus()
    await test_datadog()
    await test_logs()
    await test_database()
    await test_api_gateway()
    
    print("\n" + "=" * 50)
    print("TESTING COMPLETE")
    print("=" * 50)


if __name__ == '__main__':
    asyncio.run(test_all())
