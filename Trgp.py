import urllib.request
import json
import time
import socket

class LocationTracker:
    def __init__(self, log_file='location_log.txt'):
        """
        Initialize the Location Tracker with basic configuration
        
        Args:
            log_file (str): Path to the log file for storing location data
        """
        self.log_file = log_file
        self.location_data = []

    def get_ip_location(self):
        """
        Retrieve approximate location based on IP address using external service
        
        Returns:
            dict: Location information or None if retrieval fails
        """
        try:
            # Use a public IP geolocation service
            with urllib.request.urlopen('https://ipinfo.io/json') as response:
                data = json.loads(response.read().decode('utf-8'))
                
                # Extract location information
                location_info = {
                    'timestamp': time.time(),
                    'ip': data.get('ip', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('region', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                }
                
                # Try to parse coordinates if available
                try:
                    loc = data.get('loc', '0,0').split(',')
                    location_info['latitude'] = float(loc[0])
                    location_info['longitude'] = float(loc[1])
                except (ValueError, IndexError):
                    location_info['latitude'] = 0
                    location_info['longitude'] = 0
                
                return location_info
        
        except Exception as e:
            print(f"Location retrieval error: {e}")
            return None

    def log_location(self, location_info):
        """
        Log location information to a text file
        """