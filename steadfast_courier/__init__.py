"""
SteadFast Courier Python Package
A professional Python package for integrating with SteadFast Courier API.
Compatible with Django, FastAPI, Flask, and all Python frameworks.

Version: 1.0.0
Author: Rezwan Ahamed (https://github.com/rezwanahamed)
Original PHP Package: Nayem Uddin
"""

from .client import SteadfastCourier
from .exceptions import SteadfastException

__version__ = "1.0.0"
__author__ = "Rezwan Ahamed"
__github__ = "https://github.com/rezwanahamed"
__all__ = ["SteadfastCourier", "SteadfastException"]
