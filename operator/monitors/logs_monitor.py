"""Logs monitoring integration (ELK, CloudWatch, Loki)."""

import aiohttp
from typing import Dict, Any
from .base_monitor import BaseMonitor


class LogsMonitor(BaseMonitor):
    """Monitor for log aggregation systems."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize logs monitor.
        
        Args:
            config: Configuration with 'logs_type' ('elasticsearch', 'loki', 'cloudwatch'),
                   'logs_url', and provider-specific credentials
        """
        super().__init__(config)
        self.logs_type = self.config.get('logs_type', 'elasticsearch')
        self.base_url = self.config.get('logs_url', 'http://localhost:9200')
    
    async def query(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Query logs system.
        
        Args:
            query_params: Dict with provider-specific query parameters
            
        Returns:
            Dict with status and data
        """
        if self.logs_type == 'elasticsearch':
            return await self._query_elasticsearch(query_params)
        elif self.logs_type == 'loki':
            return await self._query_loki(query_params)
        elif self.logs_type == 'cloudwatch':
            return await self._query_cloudwatch(query_params)
        else:
            return {'status': 'error', 'message': f'Unsupported logs type: {self.logs_type}'}
    
    async def _query_elasticsearch(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Query Elasticsearch."""
        index = query_params.get('index', '_all')
        query = query_params.get('query', {'match_all': {}})
        size = query_params.get('size', 10)
        
        url = f"{self.base_url}/{index}/_search"
        body = {
            'query': query,
            'size': size,
            'sort': [{'@timestamp': 'desc'}]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=body, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'status': 'success',
                            'data': data
                        }
                    else:
                        return {
                            'status': 'error',
                            'message': f'Elasticsearch returned status {response.status}'
                        }
        except aiohttp.ClientError as e:
            return {'status': 'error', 'message': f'Connection error: {str(e)}'}
        except Exception as e:
            return {'status': 'error', 'message': f'Unexpected error: {str(e)}'}
    
    async def _query_loki(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Query Loki."""
        logql = query_params.get('query', '{job="app"}')
        limit = query_params.get('limit', 10)
        
        url = f"{self.base_url}/loki/api/v1/query_range"
        params = {
            'query': logql,
            'limit': limit
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'status': 'success',
                            'data': data
                        }
                    else:
                        return {
                            'status': 'error',
                            'message': f'Loki returned status {response.status}'
                        }
        except aiohttp.ClientError as e:
            return {'status': 'error', 'message': f'Connection error: {str(e)}'}
        except Exception as e:
            return {'status': 'error', 'message': f'Unexpected error: {str(e)}'}
    
    async def _query_cloudwatch(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Query CloudWatch (requires boto3)."""
        return {
            'status': 'error',
            'message': 'CloudWatch integration requires boto3 setup'
        }
    
    async def health_check(self) -> bool:
        """Check if logs system is accessible."""
        try:
            if self.logs_type == 'elasticsearch':
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.base_url}/_cluster/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                        return response.status == 200
            elif self.logs_type == 'loki':
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.base_url}/ready", timeout=aiohttp.ClientTimeout(total=5)) as response:
                        return response.status == 200
            return False
        except Exception:
            return False
    
    def format_response(self, data: Dict[str, Any]) -> str:
        """Format logs response for SMS."""
        if data.get('status') == 'error':
            return f"❌ Error: {data.get('message', 'Unknown error')}"
        
        if self.logs_type == 'elasticsearch':
            hits = data.get('data', {}).get('hits', {}).get('hits', [])
            total = data.get('data', {}).get('hits', {}).get('total', {})
            total_value = total.get('value', 0) if isinstance(total, dict) else total
            
            if not hits:
                return "📋 No logs found"
            
            lines = [f"📋 Found {total_value} logs"]
            for hit in hits[:3]:  # Show first 3 logs
                source = hit.get('_source', {})
                message = source.get('message', str(source)[:50])
                lines.append(f"• {message[:60]}")
            
            return "\n".join(lines)
        
        elif self.logs_type == 'loki':
            result = data.get('data', {}).get('data', {}).get('result', [])
            if not result:
                return "📋 No logs found"
            
            lines = ["📋 Recent logs:"]
            for stream in result[:3]:
                values = stream.get('values', [])
                if values:
                    log_line = values[0][1][:60]
                    lines.append(f"• {log_line}")
            
            return "\n".join(lines)
        
        return "📋 Logs query completed"
