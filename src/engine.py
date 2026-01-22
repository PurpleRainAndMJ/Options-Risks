import numpy as np
from scipy.stats import norm

def black_scholes_greeks(S, K, T, r, sigma, option_type="call"):
    """Calcule le prix et les grecques (Delta, Gamma, Vega)."""
    T = max(T / 365, 0.0001) 
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    res = {}
    if option_type.lower() == "call":
        res['price'] = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        res['delta'] = norm.cdf(d1)
    else:
        res['price'] = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        res['delta'] = norm.cdf(d1) - 1
        
    res['gamma'] = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    res['vega'] = S * norm.pdf(d1) * np.sqrt(T) * 0.01
    res['theta'] = (- (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
                    - r * K * np.exp(-r * T) * norm.cdf(d2 if option_type == "call" else -d2)) / 365
    return res

def explain_pnl(delta, gamma, vega, theta, dS, dVol, dt=1/365):
    """
    Décompose la variation du PnL selon les facteurs de risque.
    dS : Variation du prix du sous-jacent
    dVol : Variation de la volatilité (ex: 0.05 pour +5%)
    """
    delta_pnl = delta * dS
    gamma_pnl = 0.5 * gamma * (dS**2)
    vega_pnl = vega * (dVol * 100) # vega est souvent pour 1%
    theta_pnl = theta * dt
    
    return {
        "Delta PnL": delta_pnl,
        "Gamma PnL": gamma_pnl,
        "Vega PnL": vega_pnl,
        "Theta PnL": theta_pnl,
        "Total Explained": delta_pnl + gamma_pnl + vega_pnl + theta_pnl
    }