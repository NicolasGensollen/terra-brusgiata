import numpy as np

from terra_brusgiata.banc import charger_scenarios, chronometrer, jouer_partie
from terra_brusgiata.strategies import arroser_devant, parefeux_devant, proteger_maisons


STRATEGIES = (proteger_maisons, arroser_devant, parefeux_devant)

scenarios = charger_scenarios(["scenarios/pozzo.json"])
etat_depart, parametres = scenarios["pozzo"]

for strategie in STRATEGIES:
    toutes_les_durees = []      # temps de réflexion de chaque tour, en secondes
    duree_des_parties = 0       # durée totale des parties, en secondes
    for graine in range(10):
        chronometree, durees = chronometrer(strategie)
        partie = jouer_partie(etat_depart, parametres, chronometree, graine)
        toutes_les_durees += durees
        duree_des_parties += partie["duree"]
    part = sum(toutes_les_durees) / duree_des_parties
    print(f"{strategie.__name__:<18} {len(toutes_les_durees):5} tours, "
          f"réflexion moyenne {1000 * np.mean(toutes_les_durees):.2f} ms, "
          f"maximale {1000 * max(toutes_les_durees):.2f} ms, "
          f"part de la partie {part:.0%}")
