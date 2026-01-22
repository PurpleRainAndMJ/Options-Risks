from datetime import datetime
import pandas as pd

def days_to_expiry(expiry_str):
    """
    Convertit une date de type '260327' (27 mars 2026) en nombre de jours restants.
    """
    try:
        expiry_date = datetime.strptime(expiry_str, '%y%m%d')
        delta = expiry_date - datetime.now()
        return max(delta.days, 0.001)  # On évite 0 pour les divisions
    except ValueError:
        return 30.0 # Valeur par défaut en cas d'erreur

def format_number(num):
    """Formate les gros chiffres pour la lisibilité."""
    if abs(num) >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif abs(num) >= 1_000:
        return f"{num / 1_000:.2f}k"
    return f"{num:.2f}"