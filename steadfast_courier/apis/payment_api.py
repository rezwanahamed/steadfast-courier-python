"""
Payment API for SteadFast Courier.
"""

from typing import Any, Dict

from .base_api import BaseApi


class PaymentApi(BaseApi):
    """
    Payment API for managing payments and invoices.
    """
    
    def get_payments(self) -> Dict[str, Any]:
        """
        Get list of all payments.
        
        Returns:
            dict: List of payments
            
        Example:
            >>> client = SteadfastCourier(api_key, secret_key)
            >>> payments = client.payment().get_payments()
        """
        return self._make_request('GET', '/payments')
    
    def get_payment(self, payment_id: int) -> Dict[str, Any]:
        """
        Get single payment with associated consignments.
        
        Args:
            payment_id (int): Payment ID
            
        Returns:
            dict: Payment details with consignments
            
        Example:
            >>> client = SteadfastCourier(api_key, secret_key)
            >>> payment = client.payment().get_payment(123)
        """
        return self._make_request('GET', f'/payments/{payment_id}')
