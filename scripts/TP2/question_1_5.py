import matplotlib.pyplot as plt
import numpy as np

from terra_brusgiata.affichage import animer_terrain, dessiner_terrain, legende_terrain
from terra_brusgiata.foret import (
    EAU,
    FORET,
    HABITATION,
    MAQUIS,
    PRAIRIE,
    ROCHE,
    ROUTE,
    allumer_bord_gauche,
    simuler
)
from terra_brusgiata.terrain import creer_etat_terrain

# 1. Une petite carte qui contient tous les types de végétation
vegetation = np.full((60, 90), FORET, dtype=np.int8)
vegetation[:, 30:55] = MAQUIS          # une bande de maquis au milieu
vegetation[:, 55:75] = PRAIRIE         # puis des prairies
vegetation[:, 75:77] = EAU             # une rivière
vegetation[40, :] = ROUTE              # une route horizontale
vegetation[10:20, 60:70] = HABITATION  # un village dans les prairies
vegetation[45:55, 10:20] = ROCHE       # un massif rocheux dans la forêt

etat = creer_etat_terrain(vegetation, np.zeros(vegetation.shape), 100.0)

# 2. La carte avant l'incendie
fig, ax = plt.subplots(figsize=(9, 5))
dessiner_terrain(ax, etat["grille"], vegetation, "Carte avant l'incendie")
legende_terrain(ax)
fig.tight_layout()
plt.show()

# 3. L'incendie, allumé sur le bord gauche
allumer_bord_gauche(etat["grille"])
historique = simuler(etat, np.random.default_rng(0), p_base=0.6)
print(f"Incendie terminé en {len(historique) - 1} tours")
animation = animer_terrain(historique, vegetation)
