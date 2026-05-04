import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GoDaddyClient:
    def __init__(self):
        self.api_key = os.getenv('GODADDY_API_KEY')
        self.api_secret = os.getenv('GODADDY_API_SECRET')
        self.base_url = 'https://api.godaddy.com/v1'
        self.headers = {
            'Authorization': f'sso-key {self.api_key}:{self.api_secret}',
            'accept': 'application/json'
        }

    def get_domain_info(self, domain):
        """Fetch basic domain information including current nameservers."""
        url = f"{self.base_url}/domains/{domain}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_dns_records(self, domain):
        """Fetch all DNS records for a domain."""
        url = f"{self.base_url}/domains/{domain}/records"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_nameservers(self, domain, nameservers):
        """Update the nameservers for a domain at GoDaddy."""
        url = f"{self.base_url}/domains/{domain}"
        # GoDaddy expects a list of nameserver strings in the 'nameServers' field
        data = {
            "nameServers": nameservers
        }
        response = requests.patch(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.status_code == 204
