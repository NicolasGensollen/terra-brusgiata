import matplotlib.pyplot as plt
import numpy as np

from terra_brusgiata.banc import charger_scenarios, evaluer, statistiques
from terra_brusgiata.strategies import parefeux_devant


# 1. Jouer 150 parties de parefeux_devant sur le scénario pozzo.json
scenarios = charger_scenarios(["scenarios/pozzo.json"])
lignes = evaluer(parefeux_devant, scenarios, range(150), {})
gains = np.array([ligne["gain"] for ligne in lignes])

# 2. Moyenne et intervalle de confiance calculés sur les k premières parties
k = np.arange(1, len(gains) + 1)
moyennes = np.cumsum(gains) / k
erreurs = np.array([statistiques(gains[:n])["erreur_type"] for n in k])
bas, haut = moyennes - 1.96 * erreurs, moyennes + 1.96 * erreurs

for n in (10, 40, 150):
    print(f"après {n:3} parties : gain moyen {moyennes[n - 1]:5.0f}, "
          f"intervalle ± {1.96 * erreurs[n - 1]:.0f}")

# 3. La figure
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.fill_between(k[1:], bas[1:], haut[1:], alpha=0.25,
                label="intervalle de confiance à 95 %")
ax.plot(k, moyennes, label="gain moyen")
ax.set_xlabel("nombre de parties jouées")
ax.set_ylabel("gain")
ax.set_title("parefeux_devant sur pozzo.json")
ax.grid(alpha=0.3)
ax.legend()
plt.show()
