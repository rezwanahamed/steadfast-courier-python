"""
Main SteadFast Courier client class.
"""

import os
from typing import Optional

from .apis import (BalanceApi, OrderApi, PaymentApi, PoliceStationApi,
                   ReturnApi, StatusApi)


class SteadfastCourier:
    """
    Main SteadFast Courier client for all API operations.
    
    This client provides access to all SteadFast Courier API endpoints
    with built-in validation, rate limiting, and error handling.
    
    Attributes:
        api_key (str): SteadFast API Key
        secret_key (str): SteadFast Secret Key
        base_url (str): Base URL for API calls
    
    Example:
        >>> from steadfast_courier import SteadfastCourier
        >>> 
        >>> # Initialize from environment variables
        >>> client = SteadfastCourier.from_env()
        >>> 
        >>> # Or manually provide credentials
        >>> client = SteadfastCourier(
        ...     api_key='your-api-key',
        ...     secret_key='your-secret-key'
        ... )
        >>> 
        >>> # Place an order
        >>> order_response = client.order().place_order({
        ...     'invoice': 'ORD-123456',
        ...     'recipient_name': 'John Doe',
        ...     'recipient_phone': '01712345678',
        ...     'recipient_address': 'House 44, Road 2/A, Dhanmondi',
        ...     'cod_amount': 1000.00
        ... })
    """
    
    def __init__(
        self,
        api_key: str,
        secret_key: str,
        base_url: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize the SteadFast Courier client.
        
        Args:
            api_key (str): Your SteadFast API Key
            secret_key (str): Your SteadFast Secret Key
            base_url (str, optional): Custom base URL. Defaults to official API.
            timeout (int): Request timeout in seconds. Defaults to 30.
            
        Raises:
            ValueError: If api_key or secret_key is not provided
        """
        if not api_key or not secret_key:
            raise ValueError("API Key and Secret Key are required")
        
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.timeout = timeout
        
        # Initialize API instances
        self._order_api = None
        self._status_api = None
        self._balance_api = None
        self._return_api = None
        self._payment_api = None
        self._police_station_api = None
    
    @classmethod
    def from_env(
        cls,
        api_key_env: str = "STEADFAST_API_KEY",
        secret_key_env: str = "STEADFAST_SECRET_KEY",
        base_url_env: str = "STEADFAST_BASE_URL",
        timeout_env: str = "STEADFAST_TIMEOUT"
    ) -> 'SteadfastCourier':
        """
        Initialize the SteadFast Courier client from environment variables.
        
        This method reads configuration from environment variables, making it
        easy to manage credentials without hardcoding them in your application.
        
        Args:
            api_key_env (str): Environment variable name for API key. 
                              Defaults to "STEADFAST_API_KEY"
            secret_key_env (str): Environment variable name for secret key. 
                                 Defaults to "STEADFAST_SECRET_KEY"
            base_url_env (str): Environment variable name for base URL. 
                               Defaults to "STEADFAST_BASE_URL"
            timeout_env (str): Environment variable name for timeout. 
                              Defaults to "STEADFAST_TIMEOUT"
        
        Returns:
            SteadfastCourier: Initialized client instance
            
        Raises:
            ValueError: If required environment variables are not set
            
        Example:
            # Create a .env file with:
            # STEADFAST_API_KEY=your-api-key
            # STEADFAST_SECRET_KEY=your-secret-key
            # STEADFAST_BASE_URL=https://portal.packzy.com/api/v1
            # STEADFAST_TIMEOUT=30
            
            >>> from steadfast_courier import SteadfastCourier
            >>> client = SteadfastCourier.from_env()
        """
        api_key = os.getenv(api_key_env)
        secret_key = os.getenv(secret_key_env)
        base_url = os.getenv(base_url_env)
        timeout_str = os.getenv(timeout_env, "30")
        
        if not api_key:
            raise ValueError(f"Environment variable '{api_key_env}' is not set")
        if not secret_key:
            raise ValueError(f"Environment variable '{secret_key_env}' is not set")
        
        try:
            timeout = int(timeout_str)
        except ValueError:
            timeout = 30
        
        return cls(
            api_key=api_key,
            secret_key=secret_key,
            base_url=base_url,
            timeout=timeout
        )
    
    def order(self) -> OrderApi:
        """
        Get Order API instance for managing shipments.
        
        Returns:
            OrderApi: Order API instance
        """
        if self._order_api is None:
            self._order_api = OrderApi(
                self.api_key,
                self.secret_key,
                self.base_url,
                self.timeout
            )
        return self._order_api
    
    def status(self) -> StatusApi:
        """
        Get Status API instance for tracking shipments.
        
        Returns:
            StatusApi: Status API instance
        """
        if self._status_api is None:
            self._status_api = StatusApi(
                self.api_key,
                self.secret_key,
                self.base_url,
                self.timeout
            )
        return self._status_api
    
    def balance(self) -> BalanceApi:
        """
        Get Balance API instance for checking account balance.
        
        Returns:
            BalanceApi: Balance API instance
        """
        if self._balance_api is None:
            self._balance_api = BalanceApi(
                self.api_key,
                self.secret_key,
                self.base_url,
                self.timeout
            )
        return self._balance_api
    
    def return_api(self) -> ReturnApi:
        """
        Get Return API instance for managing returns.
        
        Returns:
            ReturnApi: Return API instance
        """
        if self._return_api is None:
            self._return_api = ReturnApi(
                self.api_key,
                self.secret_key,
                self.base_url,
                self.timeout
            )
        return self._return_api
    
    def payment(self) -> PaymentApi:
        """
        Get Payment API instance for managing payments.
        
        Returns:
            PaymentApi: Payment API instance
        """
        if self._payment_api is None:
            self._payment_api = PaymentApi(
                self.api_key,
                self.secret_key,
                self.base_url,
                self.timeout
            )
        return self._payment_api
    
    def police_station(self) -> PoliceStationApi:
        """
        Get Police Station API instance.
        
        Returns:
            PoliceStationApi: Police Station API instance
        """
        if self._police_station_api is None:
            self._police_station_api = PoliceStationApi(
                self.api_key,
                self.secret_key,
                self.base_url,
                self.timeout
            )
        return self._police_station_api
