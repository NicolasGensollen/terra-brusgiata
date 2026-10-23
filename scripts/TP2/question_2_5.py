import matplotlib.pyplot as plt
import numpy as np

from terra_brusgiata.affichage import afficher_relief, animer_terrain, dessiner_terrain, legende_terrain
from terra_brusgiata.foret import EAU, FEU, FORET, HABITATION, MAQUIS, PRAIRIE, ROUTE, simuler
from terra_brusgiata.terrain import creer_etat_terrain, relief_collines

# 1. Un relief : deux collines et une petite butte
forme = (80, 100)
altitude = relief_collines(forme, [(30, 35, 400, 14), (55, 70, 250, 10), (15, 80, 120, 6)])
afficher_relief(altitude, "Relief : deux collines et une butte")

# 2. Une végétation qui suit le relief
vegetation = np.full(forme, MAQUIS, dtype=np.int8)
vegetation[altitude > 150] = FORET           # forêt sur les hauteurs
vegetation[altitude < 15] = PRAIRIE          # prairies en plaine
vegetation[:, 50:52] = EAU                   # une rivière nord-sud
vegetation[72, :] = ROUTE                    # une route au sud
vegetation[58:64, 8:16] = HABITATION         # un hameau dans la plaine

etat = creer_etat_terrain(vegetation, altitude, 50.0)

# 3. Le terrain avec ses courbes de niveau
fig, ax = plt.subplots(figsize=(9, 6))
dessiner_terrain(ax, etat["grille"], vegetation, "Terrain et courbes de niveau", altitude)
legende_terrain(ax)
fig.tight_layout()
plt.show()

# 4. Un feu qui part du pied de la grande colline
etat["grille"][55, 30] = FEU
historique = simuler(etat, np.random.default_rng(0), p_base=0.6)
print(f"Incendie terminé en {len(historique) - 1} tours")
animation = animer_terrain(historique, vegetation, altitude=altitude)
