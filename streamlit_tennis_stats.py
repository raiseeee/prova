
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_top_players():
    url = "https://www.atptour.com/en/rankings/singles"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    players = []
    for row in soup.select("table.ranking-list tbody tr")[:10]:
        rank = row.select_one(".rank-cell").get_text(strip=True)
        name = row.select_one(".player-cell").get_text(strip=True)
        country = row.select_one(".country-cell img")["alt"]
        points = row.select_one(".points-cell").get_text(strip=True)
        players.append({
            "Rank": rank,
            "Name": name,
            "Country": country,
            "Points": points
        })
    return players

def simulate(player_name):
    return round(random.uniform(1.5, 3.5), 2)

def simulate_recent_matches():
    results = ["W", "L"]
    matches = [{"Result": random.choice(results)} for _ in range(5)]
    return matches

def calculate_stats(match_data):
    total = len(match_data)
    wins = sum(1 for m in match_data if m["Result"] == "W")
    return round(wins / total * 100, 2) if total > 0 else 0.0

st.title("Statistiche") # titolo
st.markdown("prova")    # sottotitolo

if st.button("Aggiorna Dati"):
    players = get_top_players()
    final_data = []

    for player in players:
        name = player["Name"]
        simulated_matches = simulate_recent_matches()
        win_rate = calculate_stats(simulated_matches)
        odds = simulate(name)
        final_data.append({
            "Rank": player["Rank"],
            "Name": name,
            "Country": player["Country"],
            "Points": player["Points"],
            "Win Rate (%)": win_rate,
            "Simulated": odds
        })
    st.write(df)
    df = pd.DataFrame(Simulated)  # o qualunque sia il nome della tua lista    
