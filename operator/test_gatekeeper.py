"""
Test script for Gatekeeper integration.

This script tests the connection and basic functionality of the 
Gatekeeper client without running the full Flask application.
"""

import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config import GATEKEEPER_CONFIG
from gatekeeper_client import (
    GatekeeperClient, 
    check_gatekeeper_health, 
    get_available_services
)


async def test_health_check():
    """Test the gatekeeper health check."""
    print("\n" + "="*60)
    print("Testing Gatekeeper Health Check")
    print("="*60)
    
    try:
        result = await check_gatekeeper_health(GATEKEEPER_CONFIG)
        print("✅ Health check successful!")
        print(f"Status: {result.get('status')}")
        print(f"Message: {result.get('message')}")
        if 'services' in result:
            print(f"Available services: {', '.join(result['services'])}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False


async def test_get_services():
    """Test getting available services."""
    print("\n" + "="*60)
    print("Testing Get Available Services")
    print("="*60)
    
    try:
        result = await get_available_services(GATEKEEPER_CONFIG)
        print("✅ Service list retrieved successfully!")
        
        if 'services' in result:
            services = result['services']
            print(f"\nFound {len(services)} services:")
            for name, url in services.items():
                print(f"  - {name}: {url}")
        return True
    except Exception as e:
        print(f"❌ Failed to get services: {str(e)}")
        return False


async def test_client_lifecycle():
    """Test client initialization and cleanup."""
    print("\n" + "="*60)
    print("Testing Client Lifecycle")
    print("="*60)
    
    try:
        client = GatekeeperClient(GATEKEEPER_CONFIG)
        print("✅ Client initialized successfully")
        
        # Test making a request
        health = await client.health_check()
        print(f"✅ Client request successful: {health.get('status')}")
        
        # Test cleanup
        await client.close()
        print("✅ Client closed successfully")
        return True
    except Exception as e:
        print(f"❌ Client lifecycle test failed: {str(e)}")
        return False


async def test_proxy_request():
    """Test making a proxied request through the gateway."""
    print("\n" + "="*60)
    print("Testing Proxy Request")
    print("="*60)
    
    try:
        client = GatekeeperClient(GATEKEEPER_CONFIG)
        
        # Try to make a proxied request to a service
        # This assumes the service exists and the gateway can route to it
        print("Attempting proxied request to spotify service...")
        
        result = await client.proxy_request(
            service_name='spotify',
            path='/',
            method='GET'
        )
        
        print(f"✅ Proxy request completed!")
        print(f"Status: {result.get('status')}")
        print(f"Response preview: {str(result.get('data', {}))[:200]}...")
        
        await client.close()
        return True
    except Exception as e:
        print(f"⚠️  Proxy request failed (may be expected if service is not running): {str(e)}")
        return False


async def run_all_tests():
    """Run all integration tests."""
    print("\n" + "="*60)
    print("GATEKEEPER INTEGRATION TESTS")
    print("="*60)
    print(f"\nGatekeeper URL: {GATEKEEPER_CONFIG['gatekeeper_url']}")
    print(f"Service Name: {GATEKEEPER_CONFIG['service_name']}")
    print(f"Timeout: {GATEKEEPER_CONFIG['gatekeeper_timeout']}s")
    
    results = []
    
    # Run tests
    results.append(("Health Check", await test_health_check()))
    results.append(("Get Services", await test_get_services()))
    results.append(("Client Lifecycle", await test_client_lifecycle()))
    results.append(("Proxy Request", await test_proxy_request()))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


def main():
    """Main entry point."""
    try:
        exit_code = asyncio.run(run_all_tests())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
