"""
Gatekeeper Client for Operator Service.

This module provides functionality to communicate with the Gatekeeper API Gateway.
It handles service registration, health checks, and proxied requests through the gateway.
"""

import asyncio
import logging
from typing import Dict, Optional, Any
import aiohttp
from aiohttp import ClientSession, ClientTimeout, ClientError

logger = logging.getLogger(__name__)


class GatekeeperClient:
    """Client for interacting with the Gatekeeper API Gateway."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Gatekeeper client.
        
        Args:
            config: Configuration dictionary with gatekeeper settings
        """
        self.base_url = config.get('gatekeeper_url', 'http://localhost:8000')
        self.timeout = config.get('gatekeeper_timeout', 30.0)
        self.service_name = config.get('service_name', 'operator')
        self.auth_token = config.get('auth_token', '')
        self._session: Optional[ClientSession] = None
        
    async def _get_session(self) -> ClientSession:
        """Get or create an aiohttp session."""
        if self._session is None or self._session.closed:
            timeout = ClientTimeout(total=self.timeout)
            self._session = ClientSession(timeout=timeout)
        return self._session
    
    async def close(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
    
    def _get_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Prepare headers for requests to gatekeeper.
        
        Args:
            additional_headers: Optional additional headers to include
            
        Returns:
            Dictionary of headers
        """
        headers = {
            'Content-Type': 'application/json',
            'X-Service-Name': self.service_name,
        }
        
        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'
        
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check the health status of the Gatekeeper service.
        
        Returns:
            Health status response from gatekeeper
            
        Raises:
            ClientError: If the request fails
        """
        try:
            session = await self._get_session()
            url = f"{self.base_url}/"
            
            async with session.get(url, headers=self._get_headers()) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Gatekeeper health check successful: {data}")
                    return data
                else:
                    logger.error(f"Gatekeeper health check failed with status {response.status}")
                    return {
                        'status': 'error',
                        'message': f'Health check failed with status {response.status}'
                    }
        except ClientError as e:
            logger.error(f"Error checking gatekeeper health: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in health check: {str(e)}")
            raise
    
    async def get_services(self) -> Dict[str, Any]:
        """
        Get list of available services from the gateway.
        
        Returns:
            Dictionary of available services
            
        Raises:
            ClientError: If the request fails
        """
        try:
            session = await self._get_session()
            url = f"{self.base_url}/services"
            
            async with session.get(url, headers=self._get_headers()) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Retrieved services from gatekeeper: {data}")
                    return data
                else:
                    logger.error(f"Failed to get services, status {response.status}")
                    return {'services': {}}
        except ClientError as e:
            logger.error(f"Error getting services: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error getting services: {str(e)}")
            raise
    
    async def proxy_request(
        self, 
        service_name: str,
        path: str,
        method: str = 'GET',
        data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a proxied request through the gatekeeper to another service.
        
        Args:
            service_name: Name of the target service
            path: API path on the target service
            method: HTTP method (GET, POST, etc.)
            data: Optional request body data
            headers: Optional additional headers
            
        Returns:
            Response from the target service
            
        Raises:
            ClientError: If the request fails
        """
        try:
            session = await self._get_session()
            url = f"{self.base_url}/{service_name}/{path.lstrip('/')}"
            request_headers = self._get_headers(headers)
            
            logger.info(f"Proxying {method} request to {url}")
            
            async with session.request(
                method=method.upper(),
                url=url,
                json=data,
                headers=request_headers
            ) as response:
                response_data = await response.json()
                
                if response.status >= 400:
                    logger.error(f"Proxy request failed with status {response.status}: {response_data}")
                else:
                    logger.info(f"Proxy request successful: {response.status}")
                
                return {
                    'status': response.status,
                    'data': response_data
                }
        except ClientError as e:
            logger.error(f"Error in proxy request: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in proxy request: {str(e)}")
            raise
    
    async def register_service(self, service_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register this service with the gatekeeper (if the gatekeeper supports dynamic registration).
        
        Args:
            service_info: Information about this service
            
        Returns:
            Registration response
            
        Note:
            This is a placeholder for future dynamic service registration functionality.
            Current gatekeeper uses static service registry.
        """
        logger.info(f"Service registration requested for {self.service_name}")
        logger.warning("Dynamic service registration not yet implemented in gatekeeper")
        return {
            'status': 'info',
            'message': 'Dynamic registration not yet supported',
            'service': self.service_name
        }


class GatekeeperClientManager:
    """
    Singleton manager for the Gatekeeper client.
    
    This ensures a single client instance is used throughout the application.
    """
    _instance: Optional[GatekeeperClient] = None
    
    @classmethod
    def initialize(cls, config: Dict[str, Any]) -> GatekeeperClient:
        """
        Initialize the global Gatekeeper client.
        
        Args:
            config: Configuration for the client
            
        Returns:
            Initialized GatekeeperClient instance
        """
        if cls._instance is None:
            cls._instance = GatekeeperClient(config)
            logger.info(f"Initialized Gatekeeper client for {config.get('service_name', 'operator')}")
        return cls._instance
    
    @classmethod
    def get_client(cls) -> Optional[GatekeeperClient]:
        """
        Get the global Gatekeeper client instance.
        
        Returns:
            GatekeeperClient instance or None if not initialized
        """
        return cls._instance
    
    @classmethod
    async def close(cls):
        """Close the global client."""
        if cls._instance:
            await cls._instance.close()
            cls._instance = None


# Helper functions for easy access
async def check_gatekeeper_health(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Quick health check helper function.
    
    Args:
        config: Gatekeeper configuration
        
    Returns:
        Health status dictionary
    """
    client = GatekeeperClient(config)
    try:
        return await client.health_check()
    finally:
        await client.close()


async def get_available_services(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Quick helper to get available services.
    
    Args:
        config: Gatekeeper configuration
        
    Returns:
        Dictionary of available services
    """
    client = GatekeeperClient(config)
    try:
        return await client.get_services()
    finally:
        await client.close()
