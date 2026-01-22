import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
import os

# --- 1. CONFIGURATION DU CHEMIN (HACK MAC/MODULES) ---
# Ceci permet à Python de trouver le dossier 'src' sans erreur
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.engine import black_scholes_greeks, explain_pnl
from src.data_loader import fetch_spot_price

# --- 2. CONFIGURATION DE L'INTERFACE ---
st.set_page_config(page_title="Options Risk Desk", layout="wide")
st.title("🛡️ Options Risk & Stress Test Dashboard")

# --- 3. BARRE LATÉRALE : PARAMÈTRES DE MARCHÉ ---
st.sidebar.header("📈 Paramètres de Marché")

# Tentative de récupération du prix live, sinon valeur par défaut
try:
    live_btc = fetch_spot_price("BTC/USDT")
    spot_price = st.sidebar.number_input("Prix du BTC (Spot)", value=float(live_btc), step=100.0)
except Exception:
    spot_price = st.sidebar.number_input("Prix du BTC (Spot)", value=65000.0, step=100.0)

vol = st.sidebar.slider("Volatilité Implicite (%)", 10, 150, 50) / 100
risk_free_rate = st.sidebar.number_input("Taux sans risque (%)", value=2.0) / 100

st.sidebar.divider()
st.sidebar.header("🧪 Simulation PnL Explain")
move_price = st.sidebar.slider("Mouvement du Prix (USDT)", -10000, 10000, 0)
move_vol = st.sidebar.slider("Choc de Volatilité (%)", -20, 20, 0) / 100

# --- 4. GESTION DU PORTEFEUILLE ---
st.subheader("📋 Portefeuille d'Options")
# Données par défaut pour l'exemple
df_init = pd.DataFrame([
    {'Type': 'call', 'Strike': 65000, 'Expiry': 15, 'Qty': 1.0},
    {'Type': 'put', 'Strike': 60000, 'Expiry': 10, 'Qty': -0.5},
    {'Type': 'call', 'Strike': 70000, 'Expiry': 30, 'Qty': 2.0}
])
edited_df = st.data_editor(df_init, num_rows="dynamic")

# --- 5. CALCULS DES RISQUES AGGRÉGÉS ---
# Initialisation indispensable pour éviter les NameError
total_delta = 0.0
total_gamma = 0.0
total_vega = 0.0
total_theta = 0.0
total_pnl_theorique = 0.0

portfolio_results = []

for _, row in edited_df.iterrows():
    # Calcul unitaire pour chaque ligne
    g = black_scholes_greeks(
        S=spot_price, 
        K=row['Strike'], 
        T=row['Expiry'], 
        r=risk_free_rate, 
        sigma=vol, 
        option_type=row['Type']
    )
    
    qty = row['Qty']
    
    # Agrégation (Grecque * Quantité)
    total_delta += g['delta'] * qty
    total_gamma += g['gamma'] * qty
    total_vega += g['vega'] * qty
    total_theta += g['theta'] * qty
    total_pnl_theorique += g['price'] * qty
    
    # On garde les détails pour affichage si besoin
    portfolio_results.append(g)

# --- 6. AFFICHAGE DES METRICS ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Delta Total (BTC)", round(total_delta, 3))
c2.metric("Gamma Total", f"{total_gamma:.6f}")
c3.metric("Vega Total (USDT/1%)", round(total_vega, 2))
c4.metric("Theta Total (Quotidien)", round(total_theta, 2))

# --- 7. GRAPHIQUE DE STRESS TEST (MULTI-VOL) ---
st.divider()
st.subheader("📉 Stress Test : PnL vs Prix & Volatilité")

# On définit les scénarios de vol
vol_scenarios = {
    "Volatilité Basse (-10%)": max(0.01, vol - 0.10),
    "Volatilité Actuelle": vol,
    "Volatilité Haute (+10%)": vol + 0.10
}

# Génération des prix pour l'axe X (Plage de +/- 20%)
price_range = np.linspace(spot_price * 0.8, spot_price * 1.2, 50)
fig = go.Figure()

for name, v_sim in vol_scenarios.items():
    pnl_curve = []
    for p in price_range:
        scenario_pnl = 0
        for _, row in edited_df.iterrows():
            g_sim = black_scholes_greeks(p, row['Strike'], row['Expiry'], risk_free_rate, v_sim, row['Type'])
            scenario_pnl += g_sim['price'] * row['Qty']
        
        # PnL relatif par rapport au prix actuel
        pnl_curve.append(scenario_pnl - total_pnl_theorique)

    fig.add_trace(go.Scatter(x=price_range, y=pnl_curve, mode='lines', name=name))

fig.add_vline(x=spot_price, line_dash="dash", line_color="gray", annotation_text="Prix Actuel")
fig.update_layout(xaxis_title="Prix du Sous-jacent", yaxis_title="Profit / Perte (USDT)", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# --- 8. SECTION PNL EXPLAIN ---
if move_price != 0 or move_vol != 0:
    st.divider()
    st.subheader("🧩 Décomposition du PnL (Approximation)")
    
    explanation = explain_pnl(
        delta=total_delta,
        gamma=total_gamma,
        vega=total_vega,
        theta=total_theta,
        dS=move_price,
        dVol=move_vol
    )
    
    # Affichage sous forme de jolies colonnes
    cols = st.columns(len(explanation))
    for i, (key, value) in enumerate(explanation.items()):
        cols[i].metric(key, f"{value:.2f} $")

st.info("💡 Le Delta mesure l'exposition directionnelle, tandis que le Gamma et le Vega capturent la convexité et la sensibilité à la peur du marché.")