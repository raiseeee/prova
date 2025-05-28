import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

# Header per simulare un browser
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Funzione per ottenere i top 10 giocatori ATP
def get_top_players():
    try:
        url = "https://www.atptour.com/en/rankings/singles"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        players = []
        for row in soup.select("table.ranking-list tbody tr")[:10]:
            rank = row.select_one(".rank-cell").get_text(strip=True)
            name = row.select_one(".player-cell").get_text(strip=True)
            country = row.select_one(".country-cell img")["alt"]
            points = row.select_one(".points-cell").get_text(strip=True)
            players.append({
                "Rank": rank,
                "Nome": name,
                "Paese": country,
                "Punti": points
            })
        return players
    except Exception as e:
        st.error(f"Errore nel recupero dei dati ATP: {e}")
        return []

# Simula una quota per scommesse
def simulate_odds(player_name):
    return round(random.uniform(1.5, 3.5), 2)

# Simula gli ultimi 5 match con risultati casuali
def simulate_recent_matches():
    risultati = ["W", "L"]  # W = vittoria, L = sconfitta
    return [{"Risultato": random.choice(risultati)} for _ in range(5)]

# Calcola la percentuale di vittorie
def calculate_stats(match_data):
    totale = len(match_data)
    vittorie = sum(1 for m in match_data if m["Risultato"] == "W")
    return round(vittorie / totale * 100, 2) if totale > 0 else 0.0

# Titolo e descrizione
st.title("🎾 Statistiche Giocatori Tennis + Quote Scommesse (Demo)")
st.markdown("Analisi dei top 10 giocatori ATP con dati simulati")

# Bottone per aggiornare i dati
if st.button("🔄 Aggiorna Dati"):
    with st.spinner("Caricamento in corso..."):
        players = get_top_players()
        dati_finali = []

        for player in players:
            nome = player["Nome"]
            match_simulati = simulate_recent_matches()
            win_rate = calculate_stats(match_simulati)
            quota = simulate_odds(nome)
            dati_finali.append({
                "Posizione": player["Rank"],
                "Nome": nome,
                "Paese": player["Paese"],
                "Punti ATP": player["Punti"],
                "Percentuale Vittorie (%)": win_rate,
                "Quota Simulata": quota
            })

        if dati_finali:
            df = pd.DataFrame(dati_finali)
            df["Quota Simulata"] = df["Quota Simulata"].astype(float)
            df["Percentuale Vittorie (%)"] = df["Percentuale Vittorie (%)"].astype(float)

            st.dataframe(df.sort_values(by="Quota Simulata").style.format({
                "Percentuale Vittorie (%)": "{:.1f}%",
                "Quota Simulata": "{:.2f}"
            }))
