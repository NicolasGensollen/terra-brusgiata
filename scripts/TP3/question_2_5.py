import numpy as np
 
from terra_brusgiata.foret import FEU, FORET
from terra_brusgiata.jeu import appliquer_action, valider_action

from terra_brusgiata.terrain import creer_etat_terrain
 

vegetation = np.full((20, 20), FORET, dtype=np.int8)
etat = creer_etat_terrain(vegetation, np.zeros((20, 20)), 100.0)
etat["tour"] = 5
etat["grille"][10, 10] = FEU
 
essais = [
    ("parefeu", 10, 15),
    ("parefeu", 10, 12),
    ("eau", 0, 0),
    ("protection", 3, 3), 
    ("contre_feu", 5, 5), 
    ("bulldozer", 1, 1),
    ("eau", 25, 3), 
    ("parefeu", 4)
]

for action in essais:
    raison = valider_action(etat, action, budget=100)
    if raison is None:
        appliquer_action(etat, action)
        print(f"{action} : acceptée")
    else:
        print(f"{action} : refusée, {raison}")
 
print("Pare-feu :", etat["vegetation"][10, 15], etat["grille"][10, 15])
print("Eau :", etat["humidite"][:3, :3])
print("Contre-feu :", etat["grille"][5, 5])


