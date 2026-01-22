import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.engine import black_scholes_greeks
from src.data_loader import fetch_spot_price

st.set_page_config(page_title="Crypto Options Risk", layout="wide")

st.title("🛡️ Desk de Risque Options")

# Sidebar - Paramètres Live
st.sidebar.header("Données de Marché")
try:
    live_btc = fetch_spot_price("BTC/USDT")
    spot_price = st.sidebar.number_input("Spot Price (BTC)", value=float(live_btc))
except:
    spot_price = st.sidebar.number_input("Spot Price (BTC)", value=60000.0)

vol = st.sidebar.slider("Volatilité Implicite (%)", 10, 150, 50) / 100

# Simulation de portefeuille
st.subheader("📋 Portefeuille Actif")
df_init = pd.DataFrame([
    {'Type': 'call', 'Strike': 65000, 'Expiry': 15, 'Qty': 1.0},
    {'Type': 'put', 'Strike': 55000, 'Expiry': 10, 'Qty': -0.5}
])
portfolio = st.data_editor(df_init, num_rows="dynamic")

# Calculs
results = []
for _, row in portfolio.iterrows():
    g = black_scholes_greeks(spot_price, row['Strike'], row['Expiry'], 0.02, vol, row['Type'])
    results.append({
        'Delta_Total': g['delta'] * row['Qty'],
        'Gamma_Total': g['gamma'] * row['Qty'],
        'Vega_Total': g['vega'] * row['Qty'],
        'PnL_Theorique': g['price'] * row['Qty']
    })

res_df = pd.DataFrame(results)

# Metrics d'affichage
c1, c2, c3 = st.columns(3)
c1.metric("Delta Global", round(res_df['Delta_Total'].sum(), 3))
c2.metric("Gamma Global", round(res_df['Gamma_Total'].sum(), 6))
c3.metric("Vega Global (1%)", round(res_df['Vega_Total'].sum(), 2))

# Graphique de Risque
st.divider()
st.subheader("📊 Profil de Risque (Stress Test)")
prices = [spot_price * (1 + x/100) for x in range(-20, 21)]
pnl_curve = []

for p in prices:
    p_pnl = 0
    for _, row in portfolio.iterrows():
        g = black_scholes_greeks(p, row['Strike'], row['Expiry'], 0.02, vol, row['Type'])
        p_pnl += g['price'] * row['Qty']
    pnl_curve.append(p_pnl - res_df['PnL_Theorique'].sum())

fig = go.Figure(data=go.Scatter(x=prices, y=pnl_curve, mode='lines', name='PnL Scenario'))
fig.update_layout(title="Variation du PnL vs Prix du Sous-jacent", xaxis_title="Prix BTC", yaxis_title="Gain/Perte")
st.plotly_chart(fig, use_container_width=True)