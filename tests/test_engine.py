# Pour lancer les tests : tape 'pytest' dans ton terminal
import pytest
from src.engine import black_scholes_greeks

def test_call_price():
    res = black_scholes_greeks(S=100, K=100, T=365, r=0.05, sigma=0.2, option_type="call")
    assert round(res['price'], 2) == 10.45

def test_delta_limit():
    res = black_scholes_greeks(S=200, K=100, T=30, r=0.01, sigma=0.2, option_type="call")
    assert 0.99 <= res['delta'] <= 1.0

def test_put_delta_negative():
    res = black_scholes_greeks(S=100, K=100, T=30, r=0.01, sigma=0.2, option_type="put")
    assert res['delta'] < 0