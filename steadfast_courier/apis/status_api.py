"""
Status Tracking API for SteadFast Courier.
"""

from typing import Any, Dict

from ..exceptions import SteadfastException
from .base_api import BaseApi


class StatusApi(BaseApi):
    """
    Status tracking API for checking shipment delivery status.
    """
    
    def get_status_by_consignment_id(self, consignment_id: int) -> Dict[str, Any]:
        """
        Check delivery status by consignment ID.
        
        Args:
            consignment_id (int): SteadFast consignment ID
            
        Returns:
            dict: Status information
            
        Raises:
            SteadfastException: If API error occurs
            
        Example:
            >>> client = SteadfastCourier(api_key, secret_key)
            >>> status = client.status().get_status_by_consignment_id(12345)
        """
        if not consignment_id:
            raise SteadfastException("Consignment ID is required")
        
        return self._make_request('GET', f'/status_by_cid/{consignment_id}')
    
    def get_status_by_invoice(self, invoice: str) -> Dict[str, Any]:
        """
        Check delivery status by invoice number.
        
        Args:
            invoice (str): Invoice/order number
            
        Returns:
            dict: Status information
            
        Raises:
            SteadfastException: If API error occurs
            
        Example:
            >>> client = SteadfastCourier(api_key, secret_key)
            >>> status = client.status().get_status_by_invoice('ORD-123456')
        """
        if not invoice:
            raise SteadfastException("Invoice is required")
        
        return self._make_request('GET', f'/status_by_invoice/{invoice}')
    
    def get_status_by_tracking_code(self, tracking_code: str) -> Dict[str, Any]:
        """
        Check delivery status by tracking code.
        
        Args:
            tracking_code (str): SteadFast tracking code
            
        Returns:
            dict: Status information
            
        Raises:
            SteadfastException: If API error occurs
            
        Example:
            >>> client = SteadfastCourier(api_key, secret_key)
            >>> status = client.status().get_status_by_tracking_code('TRAC123456789')
        """
        if not tracking_code:
            raise SteadfastException("Tracking code is required")
        
        return self._make_request('GET', f'/status_by_trackingcode/{tracking_code}')
