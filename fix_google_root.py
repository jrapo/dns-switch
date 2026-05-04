from utils import get_config, get_cf_zone

def fix_root_dns():
    domain, gd, cf = get_config()
    print(f"--- Fixing Root A Records for {domain} ---")
    
    try:
        get_cf_zone(cf, domain)

        # 1. Fetch current records to find the old A record
        print("[Cloudflare] Checking for old A records...")
        records = cf.get_dns_records()
        
        # 2. Delete the old A record at the root (@)
        for rec in records:
            # Cloudflare returns full name, so we check if name equals domain
            if rec['type'] == 'A' and rec['name'] == domain:
                print(f"  [Deleting] Old A record: {rec['content']}")
                cf.delete_dns_record(rec['id'])

        # 3. Add the 4 new Google IPs
        google_ips = [
            "216.239.32.21", "216.239.34.21", "216.239.36.21", "216.239.38.21"
        ]

        print("[Cloudflare] Adding 4 new Google A records...")
        for ip in google_ips:
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
