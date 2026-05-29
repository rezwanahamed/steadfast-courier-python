"""
Base API class for all SteadFast Courier API endpoints.
"""

import logging
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from ..exceptions import SteadfastException

logger = logging.getLogger(__name__)


class BaseApi:
    """
    Base class for all API endpoints.
    Handles HTTP requests, rate limiting, and error handling.
    """
    
    # Rate limiting: max requests per minute
    RATE_LIMIT_PER_MINUTE = 60
    
    # Cache prefix for rate limiting
    CACHE_PREFIX = "steadfast_courier_"
    
    # Default base URL for SteadFast API
    DEFAULT_BASE_URL = "https://portal.packzy.com/api/v1"
    
    def __init__(
        self,
        api_key: str,
        secret_key: str,
        base_url: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize the Base API.
        
        Args:
            api_key (str): SteadFast API Key
            secret_key (str): SteadFast Secret Key
            base_url (str, optional): Custom base URL. Defaults to official API.
            timeout (int): Request timeout in seconds. Defaults to 30.
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip('/')
        self.timeout = timeout
        
        # Track requests for rate limiting
        self._request_timestamps = {}
    
    def _check_rate_limit(self, endpoint: str) -> None:
        """
        Check and enforce rate limiting.
        
        Args:
            endpoint (str): API endpoint
            
        Raises:
            SteadfastException: If rate limit exceeded
        """
        current_minute = int(time.time() // 60)
        cache_key = f"{self.CACHE_PREFIX}rate_limit_{endpoint}_{current_minute}"
        
        if cache_key not in self._request_timestamps:
            self._request_timestamps[cache_key] = 0
        
        self._request_timestamps[cache_key] += 1
        
        if self._request_timestamps[cache_key] > self.RATE_LIMIT_PER_MINUTE:
            raise SteadfastException(
                f"Rate limit exceeded. Maximum {self.RATE_LIMIT_PER_MINUTE} requests per minute.",
                429
            )
        
        # Cleanup old entries
        current_minute_int = int(current_minute)
        keys_to_delete = [
            k for k in self._request_timestamps.keys()
            if int(k.split('_')[-1]) < current_minute_int - 1
        ]
        for k in keys_to_delete:
            del self._request_timestamps[k]
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the SteadFast API.
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint path
            data (dict, optional): Request payload
            
        Returns:
            dict: API response
            
        Raises:
            SteadfastException: On API errors
        """
        # Check rate limit
        self._check_rate_limit(endpoint)
        
        # Prepare URL
        url = urljoin(self.base_url, endpoint.lstrip('/'))
        
        # Prepare headers
        headers = {
            'Api-Key': self.api_key,
            'Secret-Key': self.secret_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        
        try:
            logger.debug(f"Making {method} request to {url}")
            
            if method.upper() == 'GET':
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=self.timeout
                )
            elif method.upper() == 'POST':
                response = requests.post(
                    url,
                    json=data,
                    headers=headers,
                    timeout=self.timeout
                )
            elif method.upper() == 'PUT':
                response = requests.put(
                    url,
                    json=data,
                    headers=headers,
                    timeout=self.timeout
                )
            elif method.upper() == 'DELETE':
                response = requests.delete(
                    url,
                    headers=headers,
                    timeout=self.timeout
                )
            else:
                raise SteadfastException(f"Unsupported HTTP method: {method}")
            
            # Handle response
            status_code = response.status_code
            
            try:
                response_data = response.json()
            except ValueError:
                response_data = {}
            
            # Check for errors
            if status_code >= 400:
                message = response_data.get('message', '')
                
                if not message:
                    if status_code == 404:
                        message = f"Endpoint not found: {url}. Please verify the API endpoint path."
                    elif status_code == 401:
                        message = "Unauthorized. Please check your API Key and Secret Key."
                    elif status_code == 403:
                        message = "Forbidden. Your API credentials may not have permission for this operation."
                    elif status_code == 422:
                        message = "Validation error. Please check your request data."
                    elif status_code == 500:
                        message = "Server error on SteadFast's side. Please try again later."
                    else:
                        message = f"API request failed with status code {status_code}."
                
                logger.error(
                    f"SteadFast API Error: {message}",
                    extra={
                        'endpoint': endpoint,
                        'method': method,
                        'status': status_code,
                        'url': url,
                        'response': response_data
                    }
                )
                
                raise SteadfastException(
                    message,
                    status_code,
                    response_data.get('errors', {})
                )
            
            logger.debug(f"Request successful. Status code: {status_code}")
            return response_data or {}
        
        except SteadfastException:
            raise
        
        except requests.exceptions.Timeout:
            error_msg = f"Request timeout after {self.timeout} seconds"
            logger.error(error_msg)
            raise SteadfastException(error_msg, 408)
        
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection error: {str(e)}"
            logger.error(error_msg)
            raise SteadfastException(error_msg, 0)
        
        except Exception as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            raise SteadfastException(error_msg, 0)
