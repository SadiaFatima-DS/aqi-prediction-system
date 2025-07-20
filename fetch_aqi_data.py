import requests
from datetime import datetime
import csv
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------
# Configuration
# -----------------------
API_KEY = os.getenv("AQI_PROJECT")
CITY = os.getenv("CITY")
STATE = os.getenv("STATE")
COUNTRY = os.getenv("COUNTRY")

URL = f"https://api.airvisual.com/v2/city?city={CITY}&state={STATE}&country={COUNTRY}&key={API_KEY}"
CSV_FILE = "lahore_aqi_iqair.csv"

# -----------------------
# Fetch AQI from IQAir API
# -----------------------
def fetch_aqi():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        aqi_us = data["data"]["current"]["pollution"]["aqius"]
        timestamp = data["data"]["current"]["pollution"]["ts"]
        return timestamp, aqi_us
    else:
        print("API Error:", response.status_code)
        return None, None

# -----------------------
# Save to CSV
# -----------------------
def save_to_csv(timestamp, aqi):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Timestamp", "AQI (US)"])
        writer.writerow([timestamp, aqi])
    print(f"Saved AQI: {aqi} at {timestamp}")

# -----------------------
# Main Function
# -----------------------
def main():
    timestamp, aqi = fetch_aqi()
    if aqi is not None:
        save_to_csv(timestamp, aqi)

if __name__ == "__main__":
    main()
