import os
import sys
from dotenv import load_dotenv
from godaddy import GoDaddyClient
from cloudflare import CloudflareClient

def get_config():
    """
    Load configuration and initialize clients.
    Priority for domain: CLI argument > .env DOMAIN variable.
    """
    load_dotenv()
    
    domain = sys.argv[1] if len(sys.argv) > 1 else os.getenv('DOMAIN')
    
    if not domain:
        print("Error: Domain not provided.")
        print("Usage: python <script>.py <domain>")
        print("Alternatively, set DOMAIN in your .env file.")
        sys.exit(1)
        
    return domain, GoDaddyClient(), CloudflareClient()

def get_cf_zone(cf, domain):
    """Utility to find or verify a Cloudflare zone."""
    zone = cf.list_zones(domain)
    if not zone:
        print(f"Error: Zone '{domain}' not found in Cloudflare.")
        sys.exit(1)
    cf.zone_id = zone['id']
    return zone
