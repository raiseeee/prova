
import streamlit as st
import pandas as pd
import numpy as np

# Titolo
st.title("Tennis Stats - Top 10 ATP")

# Lista simulata di giocatori
players = [
    "Novak Djokovic", "Carlos Alcaraz", "Jannik Sinner", "Daniil Medvedev", "Alexander Zverev",
    "Stefanos Tsitsipas", "Andrey Rublev", "Casper Ruud", "Hubert Hurkacz", "Taylor Fritz"
]

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
