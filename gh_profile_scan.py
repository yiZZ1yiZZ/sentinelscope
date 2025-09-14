import os
import requests
from datetime import datetime
from sentinelscope_config import GITHUB_TOKEN

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_github_info(username):
    """
    Retrieve public GitHub profile information for a given username.
    Returns a dictionary with profile details or an error message.
    """
    url = f"https://api.github.com/users/{username}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "Username": data.get("login", "N/A"),
                "Name": data.get("name", "N/A"),
                "Bio": data.get("bio", "N/A"),
                "Location": data.get("location", "Unknown"),
                "Company": data.get("company", "N/A"),
                "Email": data.get("email", "N/A"),
                "Twitter": data.get("twitter_username", "N/A"),
                "Account Created": data.get("created_at", "N/A"),
                "Last Updated": data.get("updated_at", "N/A"),
                "Public Repos": data.get("public_repos", 0),
                "Starred Repos": get_starred_count(username, headers),
                "Followers": data.get("followers", 0),
                "Profile URL": data.get("html_url"),
                "Organizations": get_user_orgs(username, headers)
            }
        else:
            return {"Error": f"User not found or API limit exceeded. Status: {response.status_code}"}
    except requests.RequestException as e:
        return {"Error": f"Request failed: {e}"}

def get_starred_count(username, headers):
    """Return the number of repositories starred by the user."""
    url = f"https://api.github.com/users/{username}/starred"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return len(response.json()) if response.status_code == 200 else "N/A"
    except requests.RequestException:
        return "N/A"

def get_user_orgs(username, headers):
    """Return a comma-separated list of organizations the user belongs to."""
    url = f"https://api.github.com/users/{username}/orgs"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            orgs = [org["login"] for org in response.json()]
            return ", ".join(orgs) if orgs else "None"
    except requests.RequestException:
        pass
    return "N/A"

def save_github_data(username):
    """Save GitHub profile information to a timestamped file in /output."""
    profile_info = get_github_info(username)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(OUTPUT_DIR, f"github_results_{timestamp}.txt")

    with open(filepath, "w", encoding="utf-8") as file:
        file.write("🐙 GitHub OSINT Report\n")
        file.write("=" * 40 + "\n\n")
        for key, value in profile_info.items():
            file.write(f"{key}: {value}\n")

    print(f"\n✅ GitHub data saved to '{filepath}'")
    return profile_info

if __name__ == "__main__":
    username = input("Enter GitHub username: ").strip()
    save_github_data(username)