import os
import sys
from datetime import datetime
from colorama import Fore, Style, init

# Import SentinelScope modules
import domain_whois_lookup
import gh_profile_scan
import linkedin_profile_search
import phone_osint_lookup
import subdomain_mapper

# Initialize colorama
init(autoreset=True)

# Output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
# SentinelScope - Automated OSINT Reconnaissance Framework
# Author: Frank Crespo
# Description: Automated OSINT data gathering from multiple sources.
# ==============================

def get_input(prompt):
    """Get user input and strip extra spaces."""
    return input(Fore.CYAN + prompt + Style.RESET_ALL).strip()

def save_to_file(filename, content):
    """Save content to a timestamped file inside /output."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(OUTPUT_DIR, f"{filename}_{timestamp}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(Fore.GREEN + f"[+] Results saved to {filepath}")

def run_github_recon():
    """Run GitHub reconnaissance module."""
    username = get_input("Enter GitHub username: ")
    if username:
        try:
            data = gh_profile_scan.save_github_data(username)
            if data:
                save_to_file("github_results", str(data))
        except Exception as e:
            print(Fore.RED + f"[!] GitHub Recon failed: {e}")
    else:
        print(Fore.RED + "❌ GitHub username is required.")

def run_phone_recon():
    """Run phone number OSINT module."""
    phone = get_input("Enter phone number to lookup: ")
    if phone:
        try:
            result = phone_osint_lookup.lookup_phone(phone)
            output = "\n".join([f"{k}: {v}" for k, v in result.items()])
            print(Fore.YELLOW + "\n🔍 Phone Lookup Results:\n" + output)
            save_to_file("phone_results", output)
        except Exception as e:
            print(Fore.RED + f"[!] Phone Recon failed: {e}")
    else:
        print(Fore.RED + "❌ Phone number is required.")

def run_whois_recon():
    """Run WHOIS domain lookup module."""
    domain = get_input("Enter domain (e.g., example.com): ")
    if domain:
        try:
            data = domain_whois_lookup.whois_lookup(domain)
            if data:
                save_to_file("whois_results", str(data))
        except Exception as e:
            print(Fore.RED + f"[!] WHOIS Lookup failed: {e}")
    else:
        print(Fore.RED + "❌ Domain name is required.")

def run_subdomain_recon():
    """Run subdomain reconnaissance module."""
    domain = get_input("Enter domain (e.g., example.com): ")
    if domain:
        try:
            data = subdomain_mapper.find_subdomains(domain)
            if data:
                save_to_file("subdomain_results", "\n".join(data))
        except Exception as e:
            print(Fore.RED + f"[!] Subdomain Recon failed: {e}")
    else:
        print(Fore.RED + "❌ Domain name is required.")

def run_linkedin_recon():
    """Run LinkedIn reconnaissance module."""
    try:
        linkedin_profile_search.search_linkedin()
    except Exception as e:
        print(Fore.RED + f"[!] LinkedIn Recon failed: {e}")

def run_all():
    """Run all modules in sequence."""
    username = get_input("Enter GitHub username: ")
    phone = get_input("Enter phone number to lookup: ")
    domain = get_input("Enter domain (e.g., example.com): ")

    if username:
        run_github_recon()
    if phone:
        run_phone_recon()
    if domain:
        run_whois_recon()
        run_subdomain_recon()

    linkedin_choice = get_input("Run LinkedIn Recon? (y/n): ").lower()
    if linkedin_choice == "y":
        run_linkedin_recon()

def main_menu():
    """Display the main menu and handle user selection."""
    while True:
        print(Fore.MAGENTA + "\n=== SentinelScope - Automated OSINT Reconnaissance ===")
        print(Fore.CYAN + "1. Run All")
        print("2. GitHub Recon")
        print("3. Phone Number OSINT")
        print("4. WHOIS Domain Lookup")
        print("5. Subdomain Reconnaissance")
        print("6. LinkedIn Recon")
        print("0. Exit")

        choice = get_input("\nSelect an option: ")

        if choice == "1":
            run_all()
        elif choice == "2":
            run_github_recon()
        elif choice == "3":
            run_phone_recon()
        elif choice == "4":
            run_whois_recon()
        elif choice == "5":
            run_subdomain_recon()
        elif choice == "6":
            run_linkedin_recon()
        elif choice == "0":
            print(Fore.GREEN + "[+] Exiting SentinelScope. Goodbye!")
            sys.exit()
        else:
            print(Fore.RED + "❌ Invalid choice! Try again.")

if __name__ == "__main__":
    main_menu()