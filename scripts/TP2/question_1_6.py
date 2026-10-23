import numpy as np
 
from terra_brusgiata.foret import (
    CENDRE,
    FORET,
    HABITATION,
    MAQUIS,
    NOMS_TYPES,
    PRAIRIE,
    allumer_bord_gauche,
    simuler
)
from terra_brusgiata.terrain import creer_etat_terrain
 
for type_terrain in (PRAIRIE, MAQUIS, FORET, HABITATION):
    proportions = []
    for graine in range(20):
        vegetation = np.full((100, 100), type_terrain, dtype=np.int8)
        etat = creer_etat_terrain(vegetation, np.zeros((100, 100)), 100.0)
        allumer_bord_gauche(etat["grille"])
        historique = simuler(
            etat,
            np.random.default_rng(graine),
            p_base=0.6,
            max_tours=5000
        )
        proportions.append(np.mean(historique[-1] == CENDRE))
    print(f"{NOMS_TYPES[type_terrain]:10} {np.mean(proportions):6.1%}")


