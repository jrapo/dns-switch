from utils import get_config, get_cf_zone

def finish_switch():
    domain, gd, cf = get_config()
    print(f"--- Final Step: Switching Nameservers for {domain} ---")
    
    try:
        # 1. Get the required nameservers from Cloudflare
        zone = get_cf_zone(cf, domain)
        target_ns = zone.get('name_servers', [])
        
        if not target_ns:
            print("Error: No nameservers found in Cloudflare zone.")
            return

        print(f"Target Nameservers: {', '.join(target_ns)}")

        # 2. Update GoDaddy
        print(f"[GoDaddy] Updating nameservers for {domain}...")
        success = gd.update_nameservers(domain, target_ns)
        
        if success:
            print("\nSUCCESS! GoDaddy has been instructed to use Cloudflare nameservers.")
        else:
            print("\nUpdate failed. GoDaddy returned an unexpected response.")

    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    finish_switch()
