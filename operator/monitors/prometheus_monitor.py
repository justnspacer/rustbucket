"""Prometheus monitoring integration."""

import aiohttp
from typing import Dict, Any
from .base_monitor import BaseMonitor


class PrometheusMonitor(BaseMonitor):
    """Monitor for Prometheus metrics."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize Prometheus monitor.
        
        Args:
            config: Configuration with 'prometheus_url' key
        """
        super().__init__(config)
        self.base_url = self.config.get('prometheus_url', 'http://localhost:9090')
    
    async def query(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Query Prometheus for metrics.
        
        Args:
            query_params: Dict with 'query' key containing PromQL query
            
        Returns:
            Dict with status and data
        """
        promql = query_params.get('query', '')
        
        if not promql:
            return {'status': 'error', 'message': 'No query provided'}
        
        url = f"{self.base_url}/api/v1/query"
        params = {'query': promql}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'status': 'success',
                            'data': data.get('data', {})
                        }
                    else:
                        return {
                            'status': 'error',
                            'message': f'Prometheus returned status {response.status}'
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
        """Check if Prometheus is accessible."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/-/healthy", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    return response.status == 200
        except Exception:
            return False
    
    def format_response(self, data: Dict[str, Any]) -> str:
        """Format Prometheus response for SMS."""
        if data.get('status') == 'error':
            return f"❌ Error: {data.get('message', 'Unknown error')}"
        
        result_type = data.get('data', {}).get('resultType', '')
        results = data.get('data', {}).get('result', [])
        
        if not results:
            return "📊 No data found"
        
        if result_type == 'vector':
            # Format instant vector results
            lines = []
            for item in results[:5]:  # Limit to 5 results for SMS
                metric = item.get('metric', {})
                value = item.get('value', [None, 'N/A'])
                metric_name = metric.get('__name__', 'metric')
                lines.append(f"{metric_name}: {value[1]}")
            
            response = "📊 Metrics:\n" + "\n".join(lines)
            if len(results) > 5:
                response += f"\n+{len(results) - 5} more"
            return response
        
        return f"📊 Found {len(results)} result(s)"
