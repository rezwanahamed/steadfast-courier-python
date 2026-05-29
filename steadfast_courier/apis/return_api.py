"""
Return Management API for SteadFast Courier.
"""

from typing import Any, Dict

from ..exceptions import SteadfastException
from .base_api import BaseApi


class ReturnApi(BaseApi):
    """
    Return management API for handling return requests.
    """
    
    def create_return_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a return request for a consignment.
        
        Args:
            data (dict): Return request data containing one of:
                - consignment_id (int): SteadFast consignment ID
                - invoice (str): Invoice/order number
                - tracking_code (str): Tracking code
                And optionally:
                - reason (str): Reason for return
        
        Returns:
            dict: Return request details
            
        Raises:
            SteadfastException: If required identifier is missing
            
        Example:
            >>> client = SteadfastCourier(api_key, secret_key)
            >>> return_req = client.return_api().create_return_request({
            ...     'invoice': 'ORD-123456',
            ...     'reason': 'Customer requested return'
            ... })
        """
        # At least one identifier is required
        if not any(k in data for k in ['consignment_id', 'invoice', 'tracking_code']):
            raise SteadfastException(
                'Either consignment_id, invoice, or tracking_code is required'
            )
        
        return self._make_request('POST', '/create_return_request', data)
    
    def get_return_request(self, return_id: int) -> Dict[str, Any]:
        """
        Get a single return request by ID.
        
        Args:
            return_id (int): Return request ID
            
        Returns:
            dict: Return request details
            
        Example:
            >>> client = SteadfastCourier(api_key, secret_key)
            >>> return_req = client.return_api().get_return_request(123)
        """
        return self._make_request('GET', f'/get_return_request/{return_id}')
    
    def get_return_requests(self) -> Dict[str, Any]:
        """
        Get all return requests.
        
        Returns:
            dict: List of return requests
            
        Example:
            >>> client = SteadfastCourier(api_key, secret_key)
            >>> returns = client.return_api().get_return_requests()
        """
        return self._make_request('GET', '/get_return_requests')
