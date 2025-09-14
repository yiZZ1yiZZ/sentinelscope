import os
from datetime import datetime
import whois

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def whois_lookup(domain):
    """
    Perform WHOIS lookup for a given domain.
    Returns a dictionary with WHOIS details or an error message.
    """
    try:
        domain_info = whois.whois(domain)
        return {
            "Domain Name": domain_info.domain_name,
            "Registrar": domain_info.registrar,
            "Creation Date": domain_info.creation_date,
            "Expiration Date": domain_info.expiration_date,
            "Updated Date": domain_info.updated_date,
            "Name Servers": domain_info.name_servers,
            "Status": domain_info.status,
            "Registrant": getattr(domain_info, "org", "Private"),
            "Emails": getattr(domain_info, "emails", "Not Available"),
            "Country": getattr(domain_info, "country", "Unknown")
        }
    except Exception as e:
        return {"Error": f"WHOIS lookup failed: {e}"}

def save_whois_data(domain):
    """Save WHOIS lookup results to a timestamped file in /output."""
    details = whois_lookup(domain)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(OUTPUT_DIR, f"whois_results_{timestamp}.txt")

    with open(filepath, "w", encoding="utf-8") as file:
        file.write("🌍 WHOIS Lookup Report\n")
        file.write("=" * 40 + "\n\n")
        for key, value in details.items():
            if isinstance(value, list):
                file.write(f"{key}:\n")
                for item in value:
                    file.write(f"  - {item}\n")
            else:
                file.write(f"{key}: {value}\n")
            file.write("\n")

    print(f"\n✅ WHOIS data saved to '{filepath}'")
    return details

if __name__ == "__main__":
    domain = input("Enter a domain (e.g., example.com): ").strip()
    save_whois_data(domain)