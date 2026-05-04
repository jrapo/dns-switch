import socket
import dns.resolver
from utils import get_config

def verify_dns():
    domain, _, _ = get_config()

    print(f"\n=== DNS Health Check: {domain} ===")
    
    # 1. Verify Nameservers
    print("\n[1/3] Checking Nameservers...")
    try:
        answers = dns.resolver.resolve(domain, 'NS')
        nss = [str(ns.target).rstrip('.') for ns in answers]
        print(f"  Current NS: {', '.join(nss)}")
        if any('cloudflare.com' in ns for ns in nss):
            print("  ✅ Status: Successfully pointing to Cloudflare!")
        else:
            print("  ⏳ Status: Still pointing to old nameservers...")
    except Exception as e:
        print(f"  ❌ Error fetching NS: {e}")

    # 2. Verify A Records
    print("\n[2/3] Checking A Records (Website)...")
    try:
        ip = socket.gethostbyname(domain)
        print(f"  {domain} resolves to: {ip}")
        print("  ✅ Status: Domain is resolving.")
    except Exception as e:
        print(f"  ❌ Error resolving domain: {e}")

    # 3. Verify MX Records
    print("\n[3/3] Checking MX Records (Email)...")
    try:
        mx_answers = dns.resolver.resolve(domain, 'MX')
        mxs = sorted([f"{mx.exchange} (Priority: {mx.preference})" for mx in mx_answers])
        print(f"  Found {len(mxs)} MX records:")
        for mx in mxs:
            print(f"    - {mx}")
        
        if any('google.com' in mx or 'googlemail.com' in mx for mx in mxs):
            print("  ✅ Status: Google Workspace records are active!")
        else:
            print("  ⚠️ Warning: No Google Workspace records found.")
    except Exception as e:
        print(f"  ❌ Error fetching MX: {e}")

    print("\n=== Verification Complete ===\n")

if __name__ == "__main__":
    verify_dns()
