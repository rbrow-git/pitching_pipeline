import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL for Baseball Reference Team Batting Stats
url = "https://www.baseball-reference.com/leagues/majors/2024-standard-batting.shtml"

# Headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Fetch the page
print("🔎 Fetching Baseball Reference Team Batting Stats...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the correct table
    table = soup.find("table", {"id": "teams_standard_batting"})

    if table:
        # Read table into Pandas
        df = pd.read_html(str(table))[0]

        # Keep only relevant columns
        columns_to_keep = ["Tm", "R/G", "SO", "BA", "OBP", "SLG", "OPS"]
        df = df[[col for col in columns_to_keep if col in df.columns]]

        # Rename columns for clarity
        df.rename(columns={"Tm": "Team", "SO": "Strikeouts"}, inplace=True)

        # Remove rows with missing team names (sometimes last row is "LgAvg" or totals)
        df = df[df["Team"].str.contains("Total") == False]

        # Save to CSV
        df.to_csv("MLB_Team_Stats.csv", index=False)

        print("✅ Team stats saved to MLB_Team_Stats.csv")
    else:
        print("❌ Table not found on the page.")
else:
    print(f"❌ Failed to fetch data. Status Code: {response.status_code}")
