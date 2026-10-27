import numpy as np

from terra_brusgiata.banc import charger_scenarios, comparer, evaluer
from terra_brusgiata.strategies import arroser_devant, parefeux_devant, proteger_maisons


NOMS = ("alata", "pozzo", "nord_est", "deux_foyers")
STRATEGIES = (proteger_maisons, arroser_devant, parefeux_devant)

# 1. Évaluer les trois stratégies sur les mêmes parties (graines 0 à 29)
scenarios = charger_scenarios([f"scenarios/{nom}.json" for nom in NOMS])
references = {}
resultats = {s.__name__: evaluer(s, scenarios, range(30), references)
             for s in STRATEGIES}

# 2. Comparer les stratégies deux à deux
paires = (("parefeux_devant", "arroser_devant"),
          ("arroser_devant", "proteger_maisons"),
          ("parefeux_devant", "proteger_maisons"))
for a, b in paires:
    appariee, non_appariee = comparer(resultats[a], resultats[b])
    gains_a = [l["gain"] for l in resultats[a]]
    gains_b = [l["gain"] for l in resultats[b]]
    correlation = np.corrcoef(gains_a, gains_b)[0, 1]
    largeur_a = appariee["ic_haut"] - appariee["ic_bas"]
    largeur_n = non_appariee["ic_haut"] - non_appariee["ic_bas"]
    print(f"{a} − {b}")
    print(f"  différence moyenne : {appariee['moyenne']:.0f}")
    print(f"  appariée     : [{appariee['ic_bas']:.0f} ; {appariee['ic_haut']:.0f}]"
          f"  (largeur {largeur_a:.0f})")
    print(f"  non appariée : [{non_appariee['ic_bas']:.0f} ; {non_appariee['ic_haut']:.0f}]"
          f"  (largeur {largeur_n:.0f})")
    print(f"  corrélation des gains : {correlation:.2f}, "
          f"intervalle {largeur_n / largeur_a:.1f} fois plus étroit en apparié")
