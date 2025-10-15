"""Security utilities for authentication and authorization."""

import hmac
import hashlib
import os
from typing import Optional, List
from flask import Request


class Security:
    """Security utilities for SMS webhook."""
    
    def __init__(self, config: dict = None):
        """
        Initialize security with configuration.
        
        Args:
            config: Dict with 'authorized_numbers' and 'twilio_auth_token'
        """
        self.config = config or {}
        self.authorized_numbers = set(self.config.get('authorized_numbers', []))
        self.twilio_auth_token = self.config.get('twilio_auth_token', os.getenv('TWILIO_AUTH_TOKEN', ''))
    
    def is_authorized(self, phone_number: str) -> bool:
        """
        Check if a phone number is authorized to use the system.
        
        Args:
            phone_number: The phone number to check
            
        Returns:
            True if authorized, False otherwise
        """
        # Normalize phone number (remove spaces, dashes, etc.)
        normalized = ''.join(c for c in phone_number if c.isdigit() or c == '+')
        
        # If no authorized numbers configured, allow all (development mode)
        if not self.authorized_numbers:
            return True
        
        return normalized in self.authorized_numbers
    
    def verify_twilio_signature(self, request: Request) -> bool:
        """
        Verify that the request came from Twilio.
        
        Args:
            request: Flask request object
            
        Returns:
            True if signature is valid, False otherwise
        """
        if not self.twilio_auth_token:
            # If no auth token configured, skip verification (development mode)
            return True
        
        # Get the signature from headers
        signature = request.headers.get('X-Twilio-Signature', '')
        
        if not signature:
            return False
        
        # Get the full URL
        url = request.url
        
        # Get the POST parameters
        params = request.form.to_dict()
        
        # Create the data string
        data_string = url
        for key in sorted(params.keys()):
            data_string += key + params[key]
        
        # Compute the signature
        computed_signature = self._compute_signature(data_string)
        
        # Compare signatures
        return hmac.compare_digest(signature, computed_signature)
    
    def _compute_signature(self, data: str) -> str:
        """
        Compute HMAC SHA256 signature for Twilio verification.
        
        Args:
            data: The data string to sign
            
        Returns:
            Base64 encoded signature
        """
        import base64
        
        # Compute HMAC SHA256
        mac = hmac.new(
            self.twilio_auth_token.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        )
        
        # Return base64 encoded signature
        return base64.b64encode(mac.digest()).decode('utf-8')
    
    def add_authorized_number(self, phone_number: str) -> None:
        """
        Add a phone number to the authorized list.
        
        Args:
            phone_number: The phone number to add
        """
        normalized = ''.join(c for c in phone_number if c.isdigit() or c == '+')
        self.authorized_numbers.add(normalized)
    
    def remove_authorized_number(self, phone_number: str) -> None:
        """
        Remove a phone number from the authorized list.
        
        Args:
            phone_number: The phone number to remove
        """
        normalized = ''.join(c for c in phone_number if c.isdigit() or c == '+')
        self.authorized_numbers.discard(normalized)
    
    def get_authorized_numbers(self) -> List[str]:
        """
        Get list of all authorized phone numbers.
        
        Returns:
            List of authorized phone numbers
        """
        return list(self.authorized_numbers)
