"""Database monitoring integration."""

import aiohttp
from typing import Dict, Any
from .base_monitor import BaseMonitor


class DatabaseMonitor(BaseMonitor):
    """Monitor for database statistics and health."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize database monitor.
        
        Args:
            config: Configuration with database connection details
        """
        super().__init__(config)
        self.db_type = self.config.get('db_type', 'postgres')
        self.stats_url = self.config.get('stats_url', '')  # e.g., pgBouncer stats endpoint
    
    async def query(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Query database statistics.
        
        Args:
            query_params: Dict with 'metric' key (connections, queries, etc.)
            
        Returns:
            Dict with status and data
        """
        metric = query_params.get('metric', 'connections')
        
        if not self.stats_url:
            return {
                'status': 'error',
                'message': 'Database stats URL not configured'
            }
        
        # For pgBouncer or similar stats endpoints
        if self.db_type == 'postgres' and 'pgbouncer' in self.stats_url:
            return await self._query_pgbouncer(metric)
        
        # Generic database health endpoint
        return await self._query_health_endpoint(metric)
    
    async def _query_pgbouncer(self, metric: str) -> Dict[str, Any]:
        """Query pgBouncer stats."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.stats_url}/stats", timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'status': 'success',
                            'data': data,
                            'metric': metric
                        }
                    else:
                        return {
                            'status': 'error',
                            'message': f'Stats endpoint returned status {response.status}'
                        }
        except aiohttp.ClientError as e:
            return {'status': 'error', 'message': f'Connection error: {str(e)}'}
        except Exception as e:
            return {'status': 'error', 'message': f'Unexpected error: {str(e)}'}
    
    async def _query_health_endpoint(self, metric: str) -> Dict[str, Any]:
        """Query generic database health endpoint."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.stats_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'status': 'success',
                            'data': data,
                            'metric': metric
                        }
                    else:
                        return {
                            'status': 'error',
                            'message': f'Health endpoint returned status {response.status}'
                        }
        except aiohttp.ClientError as e:
            return {'status': 'error', 'message': f'Connection error: {str(e)}'}
        except Exception as e:
            return {'status': 'error', 'message': f'Unexpected error: {str(e)}'}
    
    async def health_check(self) -> bool:
        """Check if database monitoring is accessible."""
        if not self.stats_url:
            return False
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.stats_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    return response.status == 200
        except Exception:
            return False
    
    def format_response(self, data: Dict[str, Any]) -> str:
        """Format database stats response for SMS."""
        if data.get('status') == 'error':
            return f"❌ Error: {data.get('message', 'Unknown error')}"
        
        metric = data.get('metric', 'stats')
        stats = data.get('data', {})
        
        if not stats:
            return "🗄️ No database stats available"
        
        lines = [f"🗄️ DB {metric.title()}:"]
        
        # Common database metrics
        if 'connections' in stats:
            lines.append(f"Connections: {stats['connections']}")
        if 'active_connections' in stats:
            lines.append(f"Active: {stats['active_connections']}")
        if 'idle_connections' in stats:
            lines.append(f"Idle: {stats['idle_connections']}")
        if 'queries_per_sec' in stats:
            lines.append(f"QPS: {stats['queries_per_sec']}")
        if 'slow_queries' in stats:
            lines.append(f"Slow queries: {stats['slow_queries']}")
        
        return "\n".join(lines) if len(lines) > 1 else "🗄️ Database healthy"
