import ccxt
import os
from dotenv import load_dotenv

load_dotenv()

def get_binance_client():
    return ccxt.binance({
        'apiKey': os.getenv("BINANCE_API_KEY"),
        'secret': os.getenv("BINANCE_SECRET_KEY"),
        'options': {'defaultType': 'delivery'} # Pour accéder aux options
    })

def fetch_spot_price(symbol="BTC/USDT"):
    exchange = ccxt.binance()
    ticker = exchange.fetch_ticker(symbol)
    return ticker['last']