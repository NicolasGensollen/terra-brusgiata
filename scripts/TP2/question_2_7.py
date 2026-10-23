import numpy as np
 
from terra_brusgiata.foret import ARBRE, FORET, allumer, simuler
from terra_brusgiata.terrain import colline, creer_etat_terrain
 

altitude = colline((101, 101), 50, 50, 300, 12)

for nom, (ligne, colonne) in [("pied", (50, 86)), ("sommet", (50, 50))]:
    surfaces = []

    for graine in range(10):
        vegetation = np.full((101, 101), FORET, dtype=np.int8)
        etat = creer_etat_terrain(vegetation, altitude, 100.0)
        allumer(etat["grille"], ligne, colonne)
        rng = np.random.default_rng(graine)
        fin = simuler(etat, rng, p_base=0.6, max_tours=40)[-1]
        surfaces.append(np.count_nonzero(fin != ARBRE))
    
    print(f"{nom:7} {np.mean(surfaces):7.0f} cases")


