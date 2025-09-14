import os
import requests
from datetime import datetime

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_crtsh_subdomains(domain):
    """Retrieve subdomains from crt.sh."""
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    subdomains = set()
    try:
        response = requests.get(url, timeout=10, verify=False)
        if response.status_code == 200:
            json_data = response.json()
            subdomains.update(entry['name_value'].strip() for entry in json_data)
    except requests.RequestException as e:
        subdomains.add(f"Error fetching data from crt.sh: {e}")
    return subdomains

def get_threatcrowd_subdomains(domain):
    """Retrieve subdomains from ThreatCrowd."""
    url = f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}"
    subdomains = set()
    try:
        response = requests.get(url, timeout=10, verify=False)
        if response.status_code == 200:
            json_data = response.json()
            if json_data.get("subdomains"):
                subdomains.update(json_data["subdomains"])
    except requests.RequestException as e:
        subdomains.add(f"Error fetching data from ThreatCrowd: {e}")
    return subdomains

def find_subdomains(domain):
    """
    Find subdomains using multiple sources and save results.
    Returns a set of subdomains.
    """
    subdomains = set()
    subdomains.update(get_crtsh_subdomains(domain))
    subdomains.update(get_threatcrowd_subdomains(domain))
    save_subdomains(domain, subdomains)
    return subdomains

def save_subdomains(domain, subdomains):
    """Save subdomain results to a timestamped file in /output."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(OUTPUT_DIR, f"subdomain_results_{timestamp}.txt")

    with open(filepath, "w", encoding="utf-8") as file:
        file.write("🔍 Subdomain Enumeration Report\n")
        file.write("=" * 40 + "\n\n")
        file.write(f"📌 Target Domain: {domain}\n")
        file.write(f"📅 Total Subdomains Found: {len(subdomains)}\n\n")
        file.write("📜 Subdomains List:\n")
        file.write("-" * 25 + "\n")
        for sub in sorted(subdomains):
            file.write(f"🔹 {sub}\n")

    print(f"✅ Subdomains saved to '{filepath}'")

if __name__ == "__main__":
    target_domain = input("Enter target domain: ").strip()
    find_subdomains(target_domain)