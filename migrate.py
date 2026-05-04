import time
from utils import get_config, get_cf_zone

def migrate():
    domain, gd, cf = get_config()
    print(f"--- Starting Migration for {domain} ---")
    
    try:
        # 1. Setup Zone
        get_cf_zone(cf, domain)

        # 2. Fetch existing Cloudflare records to avoid duplicates
        print("[Cloudflare] Fetching existing records...")
        existing_cf_records = cf.get_dns_records()
        
        def record_exists(type, name, content):
            # Normalize names (Cloudflare often returns the full domain name)
            full_name = domain if name == '@' else f"{name}.{domain}"
            for r in existing_cf_records:
                if r['type'] == type and r['name'] == full_name and r['content'] == content:
                    return True
            return False

        # 3. Fetch records from GoDaddy
        print(f"[GoDaddy] Fetching records...")
        gd_records = gd.get_dns_records(domain)
        
        # 4. Migrate each record
        print(f"[Cloudflare] Processing {len(gd_records)} records...")
        
        migrated_count = 0
        skipped_count = 0
        duplicate_count = 0

        for rec in gd_records:
            # Skip NS records - Cloudflare manages these
            if rec['type'] == 'NS':
                skipped_count += 1
                continue

            # Skip the GoDaddy Domain Connect record
            if rec['name'] == '_domainconnect':
                skipped_count += 1
                continue

            # Check for duplicates
            if record_exists(rec['type'], rec['name'], rec['data']):
                print(f"  [Skip] Duplicate: {rec['type']} {rec['name']}")
                duplicate_count += 1
                continue

            # Prepare Cloudflare record data
            cf_data = {
                "type": rec['type'],
                "name": rec['name'],
                "content": rec['data'],
                "ttl": 1,
                "proxied": False
            }

            if rec['type'] == 'MX':
                cf_data['priority'] = rec.get('priority', 10)
            
            try:
                cf.create_dns_record(cf_data)
                print(f"  [OK] Migrated: {rec['type']} {rec['name']}")
                migrated_count += 1
                time.sleep(0.1)
            except Exception as e:
                print(f"  [Fail] {rec['type']} {rec['name']}: {e}")

        print(f"\n--- Migration Complete ---")
        print(f"Successfully migrated: {migrated_count}")
        print(f"Duplicates skipped: {duplicate_count}")
        print(f"System records skipped: {skipped_count}")

    except Exception as e:
        print(f"\nError during migration: {e}")

if __name__ == "__main__":
    migrate()
