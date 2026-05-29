"""
Custom exceptions for SteadFast Courier API integration.
"""


class SteadfastException(Exception):
    """
    Base exception for all SteadFast Courier API errors.
    
    Attributes:
        message (str): The error message
        code (int): The error code (HTTP status code)
        errors (dict): Additional error details from the API
    """
    
    def __init__(self, message: str = "", code: int = 0, errors: dict = None):
        """
        Initialize the SteadfastException.
        
        Args:
            message (str): Error message
            code (int): Error code (typically HTTP status code)
            errors (dict): Additional error details
        """
        super().__init__(message)
        self.message = message
        self.code = code
        self.errors = errors or {}
    
    def __str__(self):
        """Return string representation of the exception."""
        return self.message
    
    def get_errors(self):
        """
        Get detailed errors array.
        
        Returns:
            dict: Dictionary of errors
        """
        return self.errors
