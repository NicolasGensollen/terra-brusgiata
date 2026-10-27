import numpy as np

from terra_brusgiata.banc import charger_scenarios, evaluer, jouer_partie
from terra_brusgiata.jeu import ne_rien_faire
from terra_brusgiata.strategies import arroser_devant, parefeux_devant, proteger_maisons


NOMS = ("alata", "pozzo", "nord_est", "deux_foyers")
STRATEGIES = (proteger_maisons, arroser_devant, parefeux_devant)
GRAINES = range(30)

scenarios = charger_scenarios([f"scenarios/{nom}.json" for nom in NOMS])

# 1. La durée des parties de référence (evaluer ne la conserve pas)
durees_reference = [
    jouer_partie(etat, parametres, ne_rien_faire, graine)["duree"]
    for etat, parametres in scenarios.values() for graine in GRAINES
]
print(f"{'référence':<18} moyenne {1000 * np.mean(durees_reference):4.0f} ms, "
      f"maximum {1000 * np.max(durees_reference):4.0f} ms")

# 2. La durée des parties de chaque stratégie
references = {}
durees_moyennes = {}
for strategie in STRATEGIES:
    lignes = evaluer(strategie, scenarios, GRAINES, references)
    durees = [l["duree"] for l in lignes]
    durees_moyennes[strategie.__name__] = np.mean(durees)
    print(f"{strategie.__name__:<18} moyenne {1000 * np.mean(durees):4.0f} ms, "
          f"maximum {1000 * np.max(durees):4.0f} ms")

# 3. Estimation pour 10 scénarios et 200 graines
n_parties = 10 * 200
temps_references = n_parties * np.mean(durees_reference)
print(f"\nPour {n_parties} parties :")
print(f"  parties de référence (jouées une seule fois) : {temps_references / 60:.1f} min")
for nom, duree in durees_moyennes.items():
    print(f"  {nom:<18} : {n_parties * duree / 60:.1f} min")
