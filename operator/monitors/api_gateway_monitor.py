"""API Gateway monitoring integration."""

import aiohttp
from typing import Dict, Any
from .base_monitor import BaseMonitor


class APIGatewayMonitor(BaseMonitor):
    """Monitor for API Gateway metrics (Kong, AWS API Gateway, custom)."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize API Gateway monitor.
        
        Args:
            config: Configuration with 'gateway_type' and provider-specific settings
        """
        super().__init__(config)
        self.gateway_type = self.config.get('gateway_type', 'kong')
        self.base_url = self.config.get('gateway_url', 'http://localhost:8001')
        self.admin_key = self.config.get('admin_key', '')
    
    async def query(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Query API Gateway metrics.
        
        Args:
            query_params: Dict with query parameters specific to gateway type
            
        Returns:
            Dict with status and data
        """
        if self.gateway_type == 'kong':
            return await self._query_kong(query_params)
        elif self.gateway_type == 'aws':
            return await self._query_aws_api_gateway(query_params)
        elif self.gateway_type == 'custom':
            return await self._query_custom_gateway(query_params)
        else:
            return {'status': 'error', 'message': f'Unsupported gateway type: {self.gateway_type}'}
    
    async def _query_kong(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Query Kong Admin API."""
        endpoint = query_params.get('endpoint', 'status')
        
        url = f"{self.base_url}/{endpoint}"
        headers = {}
        if self.admin_key:
            headers['apikey'] = self.admin_key
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'status': 'success',
                            'data': data,
                            'gateway_type': 'kong'
                        }
                    else:
                        return {
                            'status': 'error',
                            'message': f'Kong API returned status {response.status}'
                        }
        except aiohttp.ClientError as e:
            return {'status': 'error', 'message': f'Connection error: {str(e)}'}
        except Exception as e:
            return {'status': 'error', 'message': f'Unexpected error: {str(e)}'}
    
    async def _query_aws_api_gateway(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Query AWS API Gateway (requires boto3)."""
        return {
            'status': 'error',
            'message': 'AWS API Gateway integration requires boto3 setup'
        }
    
    async def _query_custom_gateway(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Query custom API Gateway metrics endpoint."""
        metrics_path = query_params.get('path', '/metrics')
        url = f"{self.base_url}{metrics_path}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        # Try to parse as JSON, fall back to text
                        try:
                            data = await response.json()
                        except:
                            data = {'text': await response.text()}
                        
                        return {
                            'status': 'success',
                            'data': data,
                            'gateway_type': 'custom'
                        }
                    else:
                        return {
                            'status': 'error',
                            'message': f'Gateway returned status {response.status}'
                        }
        except aiohttp.ClientError as e:
            return {'status': 'error', 'message': f'Connection error: {str(e)}'}
        except Exception as e:
            return {'status': 'error', 'message': f'Unexpected error: {str(e)}'}
    
    async def health_check(self) -> bool:
        """Check if API Gateway is accessible."""
        try:
            if self.gateway_type == 'kong':
                url = f"{self.base_url}/status"
            else:
                url = f"{self.base_url}/health"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    return response.status == 200
        except Exception:
            return False
    
    def format_response(self, data: Dict[str, Any]) -> str:
        """Format API Gateway response for SMS."""
        if data.get('status') == 'error':
            return f"❌ Error: {data.get('message', 'Unknown error')}"
        
        gateway_type = data.get('gateway_type', 'unknown')
        gateway_data = data.get('data', {})
        
        if not gateway_data:
            return "🌐 No gateway data available"
        
        lines = [f"🌐 API Gateway ({gateway_type}):"]
        
        if gateway_type == 'kong':
            # Kong status endpoint fields
            if 'database' in gateway_data:
                db_reachable = gateway_data['database'].get('reachable', False)
                lines.append(f"DB: {'✅' if db_reachable else '❌'}")
            
            if 'server' in gateway_data:
                connections = gateway_data['server'].get('connections_active', 0)
                lines.append(f"Active connections: {connections}")
                total = gateway_data['server'].get('total_requests', 0)
                lines.append(f"Total requests: {total}")
        
        elif 'requests_per_second' in gateway_data:
            lines.append(f"RPS: {gateway_data['requests_per_second']}")
        
        if 'error_rate' in gateway_data:
            lines.append(f"Error rate: {gateway_data['error_rate']}%")
        
        if 'latency_p95' in gateway_data:
            lines.append(f"P95 latency: {gateway_data['latency_p95']}ms")
        
        return "\n".join(lines) if len(lines) > 1 else "🌐 Gateway healthy"
