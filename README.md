# 📈 Options Risk Desk (Binance Crypto)

> **Tableau de bord professionnel pour le suivi et le pilotage des risques d'un portefeuille d'options crypto.**

Ce projet permet de surveiller les expositions d'un desk de dérivés en temps réel. Il calcule les **Grecques (Delta, Gamma, Vega, Theta)**, simule des **Stress Tests** sur la volatilité et propose une décomposition mathématique de la performance via le **PnL Explain**.

---

## 🚀 Fonctionnalités Clés

* **Calcul des Grecques (Modèle Black-Scholes)** : Monitoring précis de la sensibilité au prix ($S$), au temps ($t$), à la volatilité ($\sigma$) et aux taux ($r$).
* **Stress Testing Multi-Scénarios** : Visualisation interactive de l'impact combiné d'une variation du prix du BTC (+/- 20%) et de la volatilité implicite.
* **PnL Explain** : Décomposition du profit/perte théorique par facteur de risque (Effet Delta, Effet Gamma, Effet Vega, Effet Theta).
* **Gestion de Portefeuille Dynamique** : Édition en direct des positions (Long/Short, Call/Put) avec mise à jour instantanée du risque global.
* **Données Live Binance** : Récupération automatique du prix du sous-jacent via l'API Binance (CCXT).



---

## 🛠 Stack Technique

* **Langage** : Python 3.14+
* **Interface** : [Streamlit](https://streamlit.io/) (Dashboard interactif)
* **Calculs** : NumPy, SciPy (Stats)
* **Visualisation** : Plotly (Graphiques financiers dynamiques)
* **API** : CCXT (Connexion Binance)
* **Qualité** : Pytest (Tests unitaires mathématiques)

---

## 📦 Installation et Lancement

### 1. Cloner le projet
```bash
git clone [https://github.com/votre-nom/Options-Risks.git](https://github.com/votre-nom/Options-Risks.git)
cd Options-Risks