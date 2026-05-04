from utils import get_config

def main():
    domain, gd, cf = get_config()
    
    print(f"--- Auditing DNS for {domain} ---")
    
    try:
        # 1. GoDaddy Audit
        gd_info = gd.get_domain_info(domain)
        print("\n[GoDaddy] Current Nameservers:")
        for ns in gd_info.get('nameServers', []):
            print(f"  - {ns}")

        # 2. Cloudflare Audit
        print(f"\n[Cloudflare] Checking for zone: {domain}...")
        zone = cf.list_zones(domain)
        
        if not zone:
            print(f"Zone '{domain}' not found. Creating it now...")
            zone = cf.create_zone(domain)
            print(f"Successfully created zone: {zone['id']}")
        else:
            print(f"Found existing zone: {zone['id']}")

        print(f"\n[Cloudflare] Status: {zone['status']}")
        print("Required Nameservers for Cloudflare:")
        for ns in zone.get('name_servers', []):
            print(f"  - {ns}")

        # 3. List GoDaddy Records
        print(f"\n[GoDaddy] Fetching DNS records for {domain}...")
        records = gd.get_dns_records(domain)
        print(f"Found {len(records)} records on GoDaddy:")
        for rec in records:
            print(f"  [{rec['type']}] {rec['name']} -> {rec['data']}")

    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
