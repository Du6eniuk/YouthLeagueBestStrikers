# Using this script we will understand what kind of leagues we have access to
import requests

API_KEY = '___' # You can get one for free at the website API Football
headers = {
    'x-apisports-key': API_KEY,
    'Accept': 'application/json'
}

response = requests.get('https://v3.football.api-sports.io/leagues', headers=headers)
if response.status_code == 200:
    competitions = response.json()['response']
    for comp in competitions:
        print(comp['league']['id'], comp['league']['name'])
else:
    print("Failed to fetch competitions:", response.status_code)