import copy
 
import numpy as np
 
from terra_brusgiata.foret import CENDRE, FEU, FORET
from terra_brusgiata.terrain import creer_etat_terrain
 

vegetation = np.full((5, 5), FORET, dtype=np.int8)
for methode in ("copy", "deepcopy"):
    etat = creer_etat_terrain(vegetation.copy(), np.zeros((5, 5)), 100.0)
    copie = etat.copy() if methode == "copy" else copy.deepcopy(etat)
    copie["grille"][0, 0] = CENDRE
    copie["tour"] = 99
    modifiee = etat["grille"][0, 0] == CENDRE
    print(f"{methode:9} grille de l'original modifiée : {modifiee}, "
          f"tour de l'original : {etat['tour']}")


