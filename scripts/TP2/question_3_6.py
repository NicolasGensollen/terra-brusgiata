import numpy as np
 
from terra_brusgiata.affichage import animer_terrain
from terra_brusgiata.cartes import charger_carte
from terra_brusgiata.foret import (ARBRE, CENDRE, FEU, HABITATION, simuler, vent_depuis_angle)
 

etat = charger_carte("./maps/golfe_ajaccio.txt")
vegetation, altitude = etat["vegetation"], etat["altitude"]
 
etat["grille"][70, 20] = FEU  # 45, 60
etat["vent"] = vent_depuis_angle(0)          # vent d'ouest, soufflant vers l'est
etat["force_vent"] = 0.5
historique = simuler(etat, np.random.default_rng(1), p_base=0.6)
 
debut, fin = historique[0], historique[-1]
combustible = np.count_nonzero((debut == ARBRE) | (debut == FEU))
brule = fin == CENDRE
maisons = np.count_nonzero(brule & (vegetation == HABITATION))
print(f"{len(historique) - 1} tours, {np.count_nonzero(brule) / combustible:.1%} "
      f"du combustible brûlé, {maisons} cases d'habitation brûlées")
animation = animer_terrain(historique, vegetation, altitude=altitude)

