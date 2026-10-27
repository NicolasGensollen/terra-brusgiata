import matplotlib.pyplot as plt
import numpy as np

from terra_brusgiata.banc import charger_scenarios, evaluer
from terra_brusgiata.strategies import arroser_devant, parefeux_devant, proteger_maisons


NOMS = ("alata", "pozzo", "nord_est", "deux_foyers")
STRATEGIES = (proteger_maisons, arroser_devant, parefeux_devant)
ETIQUETTES = ("protéger", "arroser", "pare-feux")


# 1. Évaluer les trois stratégies sur les quatre scénarios, graines 0 à 29
scenarios = charger_scenarios([f"scenarios/{nom}.json" for nom in NOMS])
references = {}
resultats = {
    s.__name__: evaluer(s, scenarios, range(30), references)
    for s in STRATEGIES
}

# 2. Les quartiles, pour lire les boîtes avec des valeurs précises
for scenario in NOMS:
    print(scenario)
    for strategie in STRATEGIES:
        gains = [
            l["gain"] for l in resultats[strategie.__name__]
            if l["scenario"] == scenario
        ]
        q1, mediane, q3 = np.percentile(gains, [25, 50, 75])
        print(f"  {strategie.__name__:<18} Q1 {q1:6.0f}   médiane {mediane:6.0f}"
              f"   Q3 {q3:6.0f}   moyenne {np.mean(gains):6.0f}")

# 3. Une boîte à moustaches par stratégie, une figure par scénario
fig, axes = plt.subplots(1, 4, figsize=(14, 4.2), sharey=True)
for ax, scenario in zip(axes, NOMS):
    donnees = [[l["gain"] for l in resultats[s.__name__] if l["scenario"] == scenario]
               for s in STRATEGIES]
    ax.boxplot(donnees)
    ax.set_xticks([1, 2, 3], ETIQUETTES)
    ax.axhline(0, color="gray", linestyle="--")      # ne rien faire
    ax.set_title(scenario)
axes[0].set_ylabel("gain")
fig.tight_layout()
plt.show()
