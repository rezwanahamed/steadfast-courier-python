"""
Order Management API for SteadFast Courier.
"""

from typing import Any, Dict, List

from ..exceptions import SteadfastException
from ..validators import Validator
from .base_api import BaseApi


class OrderApi(BaseApi):
    """
    Order management API for creating and managing shipments.
    """
    
    def place_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Place a single order.
        
        Args:
            order_data (dict): Order information containing:
                - invoice (str): Unique order identifier
                - recipient_name (str): Customer's full name
                - recipient_phone (str): Customer's phone number (11 digits)
                - recipient_address (str): Delivery address
                - cod_amount (float): Cash on Delivery amount
                - note (str, optional): Special delivery notes
                - recipient_email (str, optional): Customer's email
                - alternative_phone (str, optional): Alternative contact number
                - item_description (str, optional): Description of items
                - total_lot (int, optional): Number of items/lots
                - delivery_type (int, optional): 0=home delivery, 1=hub pickup
        
        Returns:
            dict: API response containing consignment details
            
        Raises:
            SteadfastException: If validation fails or API error occurs
            
        Example:
            >>> client = SteadfastCourier(api_key, secret_key)
            >>> order_data = {
            ...     'invoice': 'ORD-123456',
            ...     'recipient_name': 'John Doe',
            ...     'recipient_phone': '01712345678',
            ...     'recipient_address': 'House 44, Road 2/A, Dhanmondi',
            ...     'cod_amount': 1000.00
            ... }
            >>> response = client.order().place_order(order_data)
        """
        self._validate_order_data(order_data)
        return self._make_request('POST', '/create_order', order_data)
    
    def place_bulk_orders(self, orders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Place multiple orders in a single API call.
        
        Args:
            orders (list): List of order data dictionaries (max 500 orders)
            
        Returns:
            dict: API response containing created consignments
            
        Raises:
            SteadfastException: If validation fails or API error occurs
            
        Example:
            >>> orders = [
            ...     {
            ...         'invoice': 'ORD-001',
            ...         'recipient_name': 'Customer 1',
            ...         'recipient_phone': '01712345678',
            ...         'recipient_address': 'Address 1',
            ...         'cod_amount': 500.00
            ...     },
            ...     {
            ...         'invoice': 'ORD-002',
            ...         'recipient_name': 'Customer 2',
            ...         'recipient_phone': '01812345678',
            ...         'recipient_address': 'Address 2',
            ...         'cod_amount': 1000.00
            ...     }
            ... ]
            >>> response = client.order().place_bulk_orders(orders)
        """
        if not orders:
            raise SteadfastException("Orders list cannot be empty")
        
        if len(orders) > 500:
            raise SteadfastException("Maximum 500 orders allowed per bulk request")
        
        # Validate each order
        for order in orders:
            self._validate_order_data(order)
        
        return self._make_request(
            'POST',
            '/create_order/bulk-order',
            {'data': orders}
        )
    
    def _validate_order_data(self, order_data: Dict[str, Any]) -> None:
        """
        Validate order data before sending to API.
        
        Args:
            order_data (dict): Order information to validate
            
        Raises:
            SteadfastException: If validation fails
        """
        # Required fields
        required_fields = [
            'invoice',
            'recipient_name',
            'recipient_phone',
            'recipient_address',
            'cod_amount'
        ]
        
        for field in required_fields:
            if field not in order_data:
                raise SteadfastException(f"Required field '{field}' is missing")
        
        # Validate individual fields
        Validator.validate_invoice(order_data['invoice'])
        Validator.validate_recipient_name(order_data['recipient_name'])
        Validator.validate_phone(order_data['recipient_phone'])
        Validator.validate_address(order_data['recipient_address'])
        Validator.validate_cod_amount(order_data['cod_amount'])
        
        # Validate optional fields if provided
        if 'alternative_phone' in order_data and order_data['alternative_phone']:
            Validator.validate_phone(
                order_data['alternative_phone'],
                "Alternative phone"
            )
        
        if 'recipient_email' in order_data and order_data['recipient_email']:
            Validator.validate_email(order_data['recipient_email'])
        
        if 'delivery_type' in order_data:
            Validator.validate_delivery_type(order_data['delivery_type'])
