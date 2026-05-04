import os
import requests
from dotenv import load_dotenv

load_dotenv()

class CloudflareClient:
    def __init__(self):
        self.api_token = os.getenv('CLOUDFLARE_API_TOKEN')
        self.zone_id = os.getenv('CLOUDFLARE_ZONE_ID')
        self.base_url = 'https://api.cloudflare.com/client/v4'
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

    def list_zones(self, domain_name):
        """Check if a zone exists for the given domain name."""
        url = f"{self.base_url}/zones?name={domain_name}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        result = response.json().get('result', [])
        return result[0] if result else None

    def create_zone(self, domain_name):
        """Create a new zone in Cloudflare."""
        url = f"{self.base_url}/zones"
        data = {
            "name": domain_name,
            "account": self.get_account_info(), # We need account ID
            "jump_start": True # Automatically try to fetch DNS records
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()['result']

    def get_account_info(self):
        """Fetch the account ID. Priority: CLOUDFLARE_ACCOUNT_ID env var > first available account."""
        env_account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
        if env_account_id:
            return {"id": env_account_id}

        url = f"{self.base_url}/accounts"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        accounts = response.json().get('result', [])
        if not accounts:
            raise Exception("No Cloudflare accounts found for this token.")
        return {"id": accounts[0]['id']}

    def get_zone_info(self, zone_id=None):
        """Fetch information about a Cloudflare zone."""
        zid = zone_id or self.zone_id
        url = f"{self.base_url}/zones/{zid}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_dns_records(self, zone_id=None):
        """Fetch DNS records from the Cloudflare zone."""
        zid = zone_id or self.zone_id
        url = f"{self.base_url}/zones/{zid}/dns_records?per_page=100"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get('result', [])

    def create_dns_record(self, record_data, zone_id=None):
        """Create a new DNS record in the Cloudflare zone."""
        zid = zone_id or self.zone_id
        url = f"{self.base_url}/zones/{zid}/dns_records"
        response = requests.post(url, headers=self.headers, json=record_data)
        response.raise_for_status()
        return response.json()

    def delete_dns_record(self, record_id, zone_id=None):
        """Delete a DNS record from the Cloudflare zone."""
        zid = zone_id or self.zone_id
        url = f"{self.base_url}/zones/{zid}/dns_records/{record_id}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.status_code == 200
