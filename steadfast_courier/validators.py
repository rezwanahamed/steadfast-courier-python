"""
Validation utilities for SteadFast Courier API.
"""

import re

from .exceptions import SteadfastException


class Validator:
    """Validation utilities for API requests."""
    
    @staticmethod
    def validate_invoice(invoice: str) -> None:
        """
        Validate invoice format.
        
        Args:
            invoice (str): Invoice identifier
            
        Raises:
            SteadfastException: If validation fails
        """
        if not invoice:
            raise SteadfastException("Invoice cannot be empty")
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', invoice):
            raise SteadfastException(
                "Invoice must be alphanumeric and can only contain hyphens and underscores"
            )
    
    @staticmethod
    def validate_recipient_name(name: str) -> None:
        """
        Validate recipient name.
        
        Args:
            name (str): Recipient's name
            
        Raises:
            SteadfastException: If validation fails
        """
        if not name:
            raise SteadfastException("Recipient name cannot be empty")
        
        if len(name) > 100:
            raise SteadfastException("Recipient name must be within 100 characters")
    
    @staticmethod
    def validate_phone(phone: str, field_name: str = "Recipient phone") -> None:
        """
        Validate phone number format.
        
        Args:
            phone (str): Phone number
            field_name (str): Name of the field for error messages
            
        Raises:
            SteadfastException: If validation fails
        """
        if not phone:
            raise SteadfastException(f"{field_name} cannot be empty")
        
        # Extract only digits
        digits = re.sub(r'[^0-9]', '', phone)
        
        if len(digits) != 11:
            raise SteadfastException(f"{field_name} must be exactly 11 digits")
    
    @staticmethod
    def validate_address(address: str) -> None:
        """
        Validate recipient address.
        
        Args:
            address (str): Delivery address
            
        Raises:
            SteadfastException: If validation fails
        """
        if not address:
            raise SteadfastException("Recipient address cannot be empty")
        
        if len(address) > 250:
            raise SteadfastException("Recipient address must be within 250 characters")
    
    @staticmethod
    def validate_cod_amount(amount) -> None:
        """
        Validate COD amount.
        
        Args:
            amount: Cash on delivery amount
            
        Raises:
            SteadfastException: If validation fails
        """
        if not isinstance(amount, (int, float)):
            raise SteadfastException("COD amount must be numeric")
        
        if amount < 0:
            raise SteadfastException("COD amount cannot be less than 0")
    
    @staticmethod
    def validate_email(email: str) -> None:
        """
        Validate email address format.
        
        Args:
            email (str): Email address
            
        Raises:
            SteadfastException: If validation fails
        """
        if not email:
            return  # Email is optional
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise SteadfastException("Invalid email format")
    
    @staticmethod
    def validate_delivery_type(delivery_type) -> None:
        """
        Validate delivery type.
        
        Args:
            delivery_type: 0 for home delivery, 1 for hub pickup
            
        Raises:
            SteadfastException: If validation fails
        """
        if delivery_type is None:
            return  # Optional field
        
        if delivery_type not in (0, 1):
            raise SteadfastException("Delivery type must be 0 (home delivery) or 1 (hub pickup)")
