import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import altair as alt

# Imposta intestazioni per simulare browser
headers = {"User-Agent": "Mozilla/5.0"}

# Recupero top 10 giocatori ATP
def get_top_players():
    try:
        url = "https://www.atptour.com/en/rankings/singles?rankRange=0-100"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        players = []
        rows = soup.select("table.ranking-list tbody tr")
        for row in rows[:10]:
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
    except Exception as e:
        st.error(f"Errore nel recupero dati: {e}")
        return []

# Simulazioni
def simulate_odds(name):
    return round(random.uniform(1.5, 3.5), 2)

def simulate_recent_matches():
    return [{"Result": random.choice(["W", "L"])} for _ in range(5)]

def calculate_winrate(matches):
    wins = sum(1 for m in matches if m["Result"] == "W")
    return round(wins / len(matches) * 100, 2)

# TITOLI
st.title("Statistiche")
st.markdown("A")

# GESTIONE STATO (clic bottone)
if "players_data" not in st.session_state:
    st.session_state["players_data"] = []

if st.button("Aggiorna Dati"):
    raw_players = get_top_players()

    if not raw_players:
        st.warning("⚠️ Nessun giocatore trovato.")
        st.stop()

    dati = []
    for p in raw_players:
        matches = simulate_recent_matches()
        winrate = calculate_winrate(matches)
        odds = simulate_odds(p["Name"])
        dati.append({
            "Rank": p["Rank"],
            "Name": p["Name"],
            "Country": p["Country"],
            "Points": p["Points"],
            "Win Rate (%)": winrate,
            "Odds": odds,
            "Matches": matches
        })

    st.session_state["players_data"] = dati

# MOSTRA SOLO SE ABBIAMO DATI
if st.session_state["players_data"]:
    df = pd.DataFrame(st.session_state["players_data"])

    # FILTRO NAZIONE
    country_list = sorted(df["Country"].unique())
    selected_country = st.selectbox("🌍 Filtro Paese", ["Tutti"] + country_list)
    if selected_country != "Tutti":
        df = df[df["Country"] == selected_country]

    # TABELLA
    st.subheader("📋 Tabella Statistiche")
    st.dataframe(df[["Rank", "Name", "Country", "Points", "Win Rate (%)", "Odds"]]
                 .sort_values(by="Odds"))

    # GRAFICO
    st.subheader("📊 Grafico Percentuale Vittorie")
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Name", sort="-y"),
        y="Win Rate (%)",
        tooltip=["Name", "Win Rate (%)"]
    ).properties(width=700)
    st.altair_chart(chart)

    # ESPANSIONE DETTAGLI
    st.subheader("📂 Match Simulati")
    for row in df.itertuples():
        with st.expander(f"{row.Name} ({row.Country})"):
            st.write(f"**Win Rate**: {row._5}%")
            st.write(f"**Quota simulata**: {row.Odds}")
            st.table(pd.DataFrame(row.Matches))
