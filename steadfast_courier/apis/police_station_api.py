"""
Police Station API for SteadFast Courier.
"""

from typing import Any, Dict

from .base_api import BaseApi


class PoliceStationApi(BaseApi):
    """
    Police Station API for retrieving police station information.
    """
    
    def get_police_stations(self) -> Dict[str, Any]:
        """
        Get list of all police stations.
        
        Returns:
            dict: List of police stations
            
        Example:
            >>> client = SteadfastCourier(api_key, secret_key)
            >>> stations = client.police_station().get_police_stations()
        """
        return self._make_request('GET', '/police_stations')
