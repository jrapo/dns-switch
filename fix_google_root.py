import sys
from utils import get_config, get_cf_zone

def fix_root_dns():
    # Load default config (domain from CLI or .env)
    domain, gd, cf = get_config()
    
    # Extract custom IPs from command line if provided
    # Usage: python fix_google_root.py <domain> [ip1 ip2 ...]
    # If 2 or more arguments are passed, assume arguments after the first one are IPs
    custom_ips = sys.argv[2:] if len(sys.argv) > 2 else []
    
    # Default Google IPs if none provided
    google_ips = [
        "216.239.32.21", "216.239.34.21", "216.239.36.21", "216.239.38.21"
    ]
    
    target_ips = custom_ips if custom_ips else google_ips

    print(f"--- Fixing Root A Records for {domain} ---")
    print(f"Target IPs: {', '.join(target_ips)}")
    
    try:
        get_cf_zone(cf, domain)

        # 1. Fetch current records to find the old A record
        print("[Cloudflare] Checking for existing root A records...")
        records = cf.get_dns_records()
        
        # 2. Delete existing A records at the root (@)
        # This clears the way for the new IPs to ensure no stale routing
        for rec in records:
            if rec['type'] == 'A' and rec['name'] == domain:
                print(f"  [Deleting] Old A record: {rec['content']}")
                cf.delete_dns_record(rec['id'])

        # 3. Add the target IPs
        print(f"[Cloudflare] Adding {len(target_ips)} new A records...")
        for ip in target_ips:
            data = {
                "type": "A",
                "name": "@",
                "content": ip,
                "ttl": 1,
                "proxied": True # Recommended to be proxied for SSL
            }
            cf.create_dns_record(data)
            print(f"  [OK] Added A record -> {ip}")

        print("\nSUCCESS! Root records updated.")

    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    fix_root_dns()
