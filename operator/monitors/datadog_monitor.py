"""Datadog monitoring integration."""

import aiohttp
from typing import Dict, Any
from .base_monitor import BaseMonitor


class DatadogMonitor(BaseMonitor):
    """Monitor for Datadog metrics and logs."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize Datadog monitor.
        
        Args:
            config: Configuration with 'datadog_api_key', 'datadog_app_key', 'datadog_site' keys
        """
        super().__init__(config)
        self.api_key = self.config.get('datadog_api_key', '')
        self.app_key = self.config.get('datadog_app_key', '')
        self.site = self.config.get('datadog_site', 'datadoghq.com')
        self.base_url = f"https://api.{self.site}/api/v1"
    
    async def query(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Query Datadog for metrics.
        
        Args:
            query_params: Dict with 'query', 'from', 'to' keys
            
        Returns:
            Dict with status and data
        """
        query = query_params.get('query', '')
        from_ts = query_params.get('from', 'now-1h')
        to_ts = query_params.get('to', 'now')
        
        if not self.api_key or not self.app_key:
            return {'status': 'error', 'message': 'Datadog credentials not configured'}
        
        if not query:
            return {'status': 'error', 'message': 'No query provided'}
        
        url = f"{self.base_url}/query"
        params = {
            'query': query,
            'from': from_ts,
            'to': to_ts
        }
        headers = {
            'DD-API-KEY': self.api_key,
            'DD-APPLICATION-KEY': self.app_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'status': 'success',
                            'data': data
                        }
                    else:
                        return {
                            'status': 'error',
                            'message': f'Datadog returned status {response.status}'
                        }
        except aiohttp.ClientError as e:
            return {
                'status': 'error',
                'message': f'Connection error: {str(e)}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Unexpected error: {str(e)}'
            }
    
    async def health_check(self) -> bool:
        """Check if Datadog API is accessible."""
        if not self.api_key or not self.app_key:
            return False
        
        try:
            url = f"{self.base_url}/validate"
            headers = {
                'DD-API-KEY': self.api_key,
                'DD-APPLICATION-KEY': self.app_key
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    return response.status == 200
        except Exception:
            return False
    
    def format_response(self, data: Dict[str, Any]) -> str:
        """Format Datadog response for SMS."""
        if data.get('status') == 'error':
            return f"❌ Error: {data.get('message', 'Unknown error')}"
        
        series = data.get('data', {}).get('series', [])
        
        if not series:
            return "📊 No data found"
        
        lines = []
        for item in series[:3]:  # Limit to 3 series for SMS
            metric = item.get('metric', 'unknown')
            points = item.get('pointlist', [])
            if points:
                latest_value = points[-1][1]
                lines.append(f"{metric}: {latest_value:.2f}")
        
        response = "📊 Datadog:\n" + "\n".join(lines)
        if len(series) > 3:
            response += f"\n+{len(series) - 3} more"
        return response
