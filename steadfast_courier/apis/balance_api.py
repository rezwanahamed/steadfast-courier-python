"""
Balance API for SteadFast Courier.
"""

from typing import Any, Dict

from .base_api import BaseApi


class BalanceApi(BaseApi):
    """
    Account balance API for checking available balance.
    """
    
    def get_current_balance(self) -> Dict[str, Any]:
        """
        Get current account balance.
        
        Returns:
            dict: Balance information
            
        Example:
            >>> client = SteadfastCourier(api_key, secret_key)
            >>> balance = client.balance().get_current_balance()
            >>> print(f"Current balance: {balance['balance']}")
        """
        return self._make_request('GET', '/get_balance')
