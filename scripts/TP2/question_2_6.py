import numpy as np
 
from terra_brusgiata.foret import ARBRE, FORET, allumer, simuler
from terra_brusgiata.terrain import creer_etat_terrain, plan_incline


print("pente  montée  descente")
for pente in (0, 5, 10, 20):
    montees, descentes = [], []
    for graine in range(10):
        vegetation = np.full((101, 101), FORET, dtype=np.int8)
        altitude = plan_incline((101, 101), pente, 100.0)
        etat = creer_etat_terrain(vegetation, altitude, 100.0)
        allumer(etat["grille"], 50, 50)
        rng = np.random.default_rng(graine)
        fin = simuler(etat, rng, p_base=0.6, max_tours=30)[-1]
        lignes_brulees = np.argwhere(fin != ARBRE)[:, 0]
        montees.append(50 - lignes_brulees.min())
        descentes.append(lignes_brulees.max() - 50)
    print(f"{pente:4}° {np.mean(montees):7.1f} {np.mean(descentes):9.1f}")
