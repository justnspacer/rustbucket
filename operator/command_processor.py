"""Command parser and processor for SMS commands."""

import re
from typing import Dict, Any, Optional
from monitors import (
    PrometheusMonitor,
    DatadogMonitor,
    LogsMonitor,
    DatabaseMonitor,
    APIGatewayMonitor
)


class CommandProcessor:
    """Parse and execute commands from SMS messages."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize command processor with monitoring integrations.
        
        Args:
            config: Configuration for all monitors
        """
        self.config = config
        
        # Initialize monitors
        self.prometheus = PrometheusMonitor(config.get('prometheus', {}))
        self.datadog = DatadogMonitor(config.get('datadog', {}))
        self.logs = LogsMonitor(config.get('logs', {}))
        self.database = DatabaseMonitor(config.get('database', {}))
        self.api_gateway = APIGatewayMonitor(config.get('api_gateway', {}))
        
        # Command patterns
        self.commands = {
            'help': self._cmd_help,
            'status': self._cmd_status,
            'metrics': self._cmd_metrics,
            'logs': self._cmd_logs,
            'db': self._cmd_database,
            'gateway': self._cmd_gateway,
            'health': self._cmd_health,
        }
    
    async def process(self, message: str) -> str:
        """
        Process an incoming SMS command.
        
        Args:
            message: The SMS message text
            
        Returns:
            Response string to send back
        """
        # Normalize message
        message = message.strip().lower()
        
        if not message:
            return "📱 Send 'help' for available commands"
        
        # Parse command and arguments
        parts = message.split(maxsplit=1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        
        # Execute command
        if command in self.commands:
            try:
                return await self.commands[command](args)
            except Exception as e:
                return f"❌ Error executing command: {str(e)}"
        else:
            return f"❌ Unknown command: {command}\nSend 'help' for available commands"
    
    async def _cmd_help(self, args: str) -> str:
        """Show available commands."""
        return """🤖 Available Commands:

• status - System overview
• metrics <query> - Query metrics
• logs <query> - Search logs
• db - Database stats
• gateway - API gateway stats
• health - Health check all systems

Examples:
metrics cpu
logs error
db connections
gateway status"""
    
    async def _cmd_status(self, args: str) -> str:
        """Get overall system status."""
        lines = ["📊 System Status:"]
        
        # Check health of all systems
        checks = {
            "Prometheus": await self.prometheus.health_check(),
            "Datadog": await self.datadog.health_check(),
            "Logs": await self.logs.health_check(),
            "Database": await self.database.health_check(),
            "Gateway": await self.api_gateway.health_check(),
        }
        
        for system, healthy in checks.items():
            status = "✅" if healthy else "❌"
            lines.append(f"{status} {system}")
        
        return "\n".join(lines)
    
    async def _cmd_metrics(self, args: str) -> str:
        """Query metrics from Prometheus or Datadog."""
        if not args:
            return "❌ Usage: metrics <query>\nExample: metrics cpu_usage"
        
        # Try Prometheus first
        result = await self.prometheus.query({'query': args})
        
        if result.get('status') == 'success':
            return self.prometheus.format_response(result)
        
        # Fallback to Datadog if Prometheus fails
        result = await self.datadog.query({'query': args})
        return self.datadog.format_response(result)
    
    async def _cmd_logs(self, args: str) -> str:
        """Search logs."""
        if not args:
            # Default: get recent errors
            args = "error"
        
        # Build query based on logs type
        if self.logs.logs_type == 'elasticsearch':
            query_params = {
                'index': 'logs-*',
                'query': {
                    'match': {
                        'message': args
                    }
                },
                'size': 5
            }
        elif self.logs.logs_type == 'loki':
            query_params = {
                'query': f'{{job="app"}} |= "{args}"',
                'limit': 5
            }
        else:
            query_params = {'query': args}
        
        result = await self.logs.query(query_params)
        return self.logs.format_response(result)
    
    async def _cmd_database(self, args: str) -> str:
        """Get database statistics."""
        metric = args if args else 'connections'
        result = await self.database.query({'metric': metric})
        return self.database.format_response(result)
    
    async def _cmd_gateway(self, args: str) -> str:
        """Get API gateway statistics."""
        endpoint = args if args else 'status'
        
        if self.api_gateway.gateway_type == 'kong':
            query_params = {'endpoint': endpoint}
        else:
            query_params = {'path': f'/{endpoint}'}
        
        result = await self.api_gateway.query(query_params)
        return self.api_gateway.format_response(result)
    
    async def _cmd_health(self, args: str) -> str:
        """Comprehensive health check."""
        lines = ["🏥 Health Check:"]
        
        # Specific system if provided
        if args:
            system = args.lower()
            if system == 'prometheus':
                healthy = await self.prometheus.health_check()
            elif system == 'datadog':
                healthy = await self.datadog.health_check()
            elif system in ['logs', 'elasticsearch', 'loki']:
                healthy = await self.logs.health_check()
            elif system in ['db', 'database']:
                healthy = await self.database.health_check()
            elif system in ['gateway', 'api']:
                healthy = await self.api_gateway.health_check()
            else:
                return f"❌ Unknown system: {system}"
            
            status = "✅ Healthy" if healthy else "❌ Unhealthy"
            return f"🏥 {system.title()}: {status}"
        
        # All systems
        systems = [
            ("Prometheus", self.prometheus),
            ("Datadog", self.datadog),
            ("Logs", self.logs),
            ("Database", self.database),
            ("API Gateway", self.api_gateway),
        ]
        
        for name, monitor in systems:
            healthy = await monitor.health_check()
            status = "✅" if healthy else "❌"
            lines.append(f"{status} {name}")
        
        return "\n".join(lines)
