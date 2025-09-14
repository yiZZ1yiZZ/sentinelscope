import os
from datetime import datetime
import phonenumbers
from phonenumbers import geocoder, carrier

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def lookup_phone(phone_number):
    """
    Look up phone number details: country and carrier.
    Returns a dictionary with the results or an error message.
    """
    try:
        parsed_number = phonenumbers.parse(phone_number)
        country = geocoder.description_for_number(parsed_number, "en")
        provider = carrier.name_for_number(parsed_number, "en")

        return {
            "Phone Number": phone_number,
            "Country": country if country else "Unknown",
            "Carrier": provider if provider else "Unknown"
        }
    except phonenumbers.NumberParseException:
        return {"Error": "Invalid phone number format."}

def save_phone_data(phone_number):
    """Save phone lookup results to a timestamped file in /output."""
    result = lookup_phone(phone_number)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(OUTPUT_DIR, f"phone_results_{timestamp}.txt")

    with open(filepath, "w", encoding="utf-8") as file:
        file.write("📱 Phone Lookup Report\n")
        file.write("=" * 40 + "\n\n")
        for key, value in result.items():
            file.write(f"{key}: {value}\n")

    print(f"\n✅ Phone data saved to '{filepath}'")
    return result

if __name__ == "__main__":
    phone_number = input("Enter phone number (with country code): ").strip()
    save_phone_data(phone_number)