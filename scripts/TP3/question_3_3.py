import numpy as np
 
from terra_brusgiata.foret import FEU, FORET
from terra_brusgiata.jeu import jouer
from terra_brusgiata.terrain import creer_etat_terrain
 
 
def plante(etat, budget, tour):
    raise RuntimeError("boum")
 
 
vegetation = np.full((20, 20), FORET, dtype=np.int8)
etat = creer_etat_terrain(vegetation, np.zeros((20, 20)), 100.0)
etat["grille"][10, 10] = FEU
resultat = jouer(etat, plante, np.random.default_rng(0), budget=10)
print(len(resultat["historique"]) - 1, "tours ;", resultat["journal"][0])
# 43 tours ; (0, None, 'erreur de la stratégie : boum')


