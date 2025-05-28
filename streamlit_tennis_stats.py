
import streamlit as st
import pandas as pd
import numpy as np

# Titolo
st.title("Tennis Stats - Top 10 ATP")
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

# Generazione statistiche simulate
simulated_stats = []
for player in players:
    simulated_stats.append({
        "Player": player,
        "Win Rate (%)": round(np.random.uniform(60, 95), 1),
    })

df = pd.DataFrame(simulated_stats)

# Aggiunta quote simulate
df["Simulated Odds"] = np.round(np.random.uniform(1.5, 3.5, size=len(df)), 2)

# Ordinamento per quote
st.subheader("Classifica simulata con quote scommesse")
st.dataframe(df.sort_values(by="Simulated Odds"))
