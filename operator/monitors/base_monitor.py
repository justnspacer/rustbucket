"""Base monitor class for all monitoring integrations."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseMonitor(ABC):
    """Abstract base class for all monitors."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize monitor with configuration."""
        self.config = config or {}
    
    @abstractmethod
    async def query(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a query against the monitoring system.
        
        Args:
            query_params: Parameters for the query
            
        Returns:
            Dict containing query results
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if the monitoring system is accessible.
        
        Returns:
            True if healthy, False otherwise
        """
        pass
    
    def format_response(self, data: Dict[str, Any]) -> str:
        """
        Format query response for SMS delivery.
        
        Args:
            data: Query result data
            
        Returns:
            Formatted string suitable for SMS
        """
        return str(data)
