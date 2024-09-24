import requests
import pandas as pd
from tqdm import tqdm

# ----------------------------
# Configuration
# ----------------------------

API_KEY = 'd2165956bcf797c43b327487874f82bf'  # Replace with your API key
BASE_URL = 'https://v3.football.api-sports.io/'
COMPETITION_ID = 14  # UEFA Youth League
SEASONS = [2020, 2021, 2022]  # Available seasons for fetching data

# Output CSV file paths
OUTPUT_FIXTURES_CSV = 'youth_league_fixtures_2020_2021.csv'
OUTPUT_SCORERS_CSV = 'youth_league_top_scorers_2020_2021.csv'
OUTPUT_ASSISTS_CSV = 'youth_league_top_assists_2020_2021.csv'
OUTPUT_CARDS_CSV = 'youth_league_top_cards_2020_2021.csv'

# ----------------------------
# Headers
# ----------------------------

headers = {
    'x-apisports-key': API_KEY,
    'Accept': 'application/json'
}

# ----------------------------
# Helper Function to Fetch Data
# ----------------------------

def fetch_data(endpoint, season):
    params = {
        'league': COMPETITION_ID,
        'season': season
    }
    
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, params=params)
    
    if response.status_code == 200:
        # Decode the response content as UTF-8
        response.encoding = 'utf-8'  # Ensure response is read as UTF-8
        return response.json().get('response', [])
    else:
        print(f"Failed to fetch {endpoint} data for Season {season}. Status Code: {response.status_code}")
        try:
            print("Response:", response.json())
        except:
            print("Response:", response.text)
        return []

# ----------------------------
# Data Fetching for Fixtures
# ----------------------------

all_fixtures = []

print("Fetching Fixtures Data...")
for season in tqdm(SEASONS, desc="Fetching Fixtures for Seasons"):
    params = {
        'league': COMPETITION_ID,
        'season': season
    }
    
    response = requests.get(f"{BASE_URL}fixtures", headers=headers, params=params)
    
    if response.status_code == 200:
        response.encoding = 'utf-8'  # Ensure response is read as UTF-8
        data = response.json()
        fixtures = data.get('response', [])
        
        print(f"Season {season}: {len(fixtures)} fixtures fetched.")
        
        if fixtures:
            all_fixtures.extend(fixtures)
    else:
        print(f"Failed to fetch fixtures data for Season {season}. Status Code: {response.status_code}")
        try:
            print("Response:", response.json())
        except:
            print("Response:", response.text)

# Save Fixtures Data
if all_fixtures:
    fixtures_df = pd.json_normalize(all_fixtures)
    # Save with UTF-8 encoding
    fixtures_df.to_csv(OUTPUT_FIXTURES_CSV, index=False, encoding='utf-8')
    print(f"Fixtures data saved to '{OUTPUT_FIXTURES_CSV}'")
else:
    print("No fixtures data fetched.")

# ----------------------------
# Data Fetching for Top Scorers, Assists, and Cards
# ----------------------------

all_scorers = []
all_assists = []
all_cards = []

# Fetch top scorers, assists, and cards for each season
for season in SEASONS:
    # Check if top scorers data is available for this season
    print(f"Fetching Top Scorers for Season {season}...")
    scorers = fetch_data('players/topscorers', season)
    if scorers:
        all_scorers.extend(scorers)
    else:
        print(f"No top scorers data available for Season {season}.")
    
    print(f"Fetching Top Assists for Season {season}...")
    assists = fetch_data('players/topassists', season)
    if assists:
        all_assists.extend(assists)
    else:
        print(f"No top assists data available for Season {season}.")
    
    print(f"Fetching Top Cards for Season {season}...")
    cards = fetch_data('players/topcards', season)
    if cards:
        all_cards.extend(cards)
    else:
        print(f"No top cards data available for Season {season}.")

# ----------------------------
# Data Processing and Saving
# ----------------------------

# Save Top Scorers Data
if all_scorers:
    scorers_df = pd.json_normalize(all_scorers)
    # Save with UTF-8 encoding
    scorers_df.to_csv(OUTPUT_SCORERS_CSV, index=False, encoding='utf-8')
    print(f"Top Scorers data saved to '{OUTPUT_SCORERS_CSV}'")
else:
    print("No Top Scorers data fetched.")

# Save Top Assists Data
if all_assists:
    assists_df = pd.json_normalize(all_assists)
    # Save with UTF-8 encoding
    assists_df.to_csv(OUTPUT_ASSISTS_CSV, index=False, encoding='utf-8')
    print(f"Top Assists data saved to '{OUTPUT_ASSISTS_CSV}'")
else:
    print("No Top Assists data fetched.")

# Save Top Cards Data
if all_cards:
    cards_df = pd.json_normalize(all_cards)
    # Save with UTF-8 encoding
    cards_df.to_csv(OUTPUT_CARDS_CSV, index=False, encoding='utf-8')
    print(f"Top Cards data saved to '{OUTPUT_CARDS_CSV}'")
else:
    print("No Top Cards data fetched.")

# As a result. It seems like there is no data on assists and cards for youth league. We will just analyze and post data on strikers. 