import matplotlib.pyplot as plt
import numpy as np

from terra_brusgiata.affichage import dessiner_terrain, legende_terrain
from terra_brusgiata.cartes import sauvegarder_carte
from terra_brusgiata.editeur import peindre
from terra_brusgiata.foret import (ARBRE, CENDRE, EAU, FEU, FORET, HABITATION, MAQUIS, PRAIRIE,
                   ROCHE, ROUTE, simuler)
from terra_brusgiata.terrain import creer_etat_terrain, relief_collines


# 1. Végétation : du maquis partout, puis on peint les éléments du paysage
vegetation = np.full((60, 80), MAQUIS, dtype=np.int8)
vegetation[:, 8:10] = EAU                          # rivière à l'ouest
vegetation[52, :] = ROUTE                          # route au sud
vegetation[:12, 50:] = FORET                       # forêt au nord-est
vegetation[40:52, 12:30] = PRAIRIE                 # prairies près de la route
peindre(vegetation, 30, 45, ROCHE, 2)              # crête rocheuse au sommet
for colonne in range(36, 46, 3):                   # village sur le flanc nord
    peindre(vegetation, 20, colonne, HABITATION, 2)

# 2. Relief : une colline principale et une plus petite
altitude = relief_collines(vegetation.shape, [(30, 45, 250, 12), (45, 65, 120, 8)])
etat = creer_etat_terrain(vegetation, altitude, 50.0)
sauvegarder_carte("village.txt", etat, "Village à flanc de colline")


# 3. Recherche du point de départ le plus dangereux pour le village
def habitations_brulees(ligne, colonne, n_graines=5):
    total = 0
    for graine in range(n_graines):
        essai = creer_etat_terrain(vegetation, altitude, 50.0)
        essai["grille"][ligne, colonne] = FEU
        fin = simuler(essai, np.random.default_rng(graine), p_base=0.4)[-1]
        total += np.count_nonzero((fin == CENDRE) & (vegetation == HABITATION))
    return total / n_graines


resultats = {}
for ligne in range(2, 60, 4):
    for colonne in range(2, 80, 4):
        case_libre = vegetation[ligne, colonne] != HABITATION
        if etat["grille"][ligne, colonne] == ARBRE and case_libre:
            resultats[(ligne, colonne)] = habitations_brulees(ligne, colonne)
pire = max(resultats, key=resultats.get)
nb_maisons = np.count_nonzero(vegetation == HABITATION)
print(f"Point le plus dangereux : {pire}, {resultats[pire]:.1f} cases "
      f"d'habitation brûlées sur {nb_maisons}")

# 4. Affichage : la carte à gauche, le risque selon le point de départ à droite
fig, (ax_carte, ax_risque) = plt.subplots(1, 2, figsize=(14, 5))
dessiner_terrain(ax_carte, etat["grille"], vegetation, "Scénario village.txt", altitude)
legende_terrain(ax_carte)

ax_risque.imshow(np.full(vegetation.shape + (3,), 0.92))    # fond gris clair
ax_risque.contour(altitude, levels=10, colors="black", linewidths=0.4, alpha=0.6)
maisons = np.argwhere(vegetation == HABITATION)
ax_risque.scatter(maisons[:, 1], maisons[:, 0], marker="s", s=6, c="#d9534f")
departs = np.array(list(resultats.keys()))
valeurs = np.array(list(resultats.values()))
nuage = ax_risque.scatter(departs[:, 1], departs[:, 0], c=valeurs,
                          cmap="inferno_r", s=40)
ax_risque.scatter(pire[1], pire[0], marker="*", s=300, c="cyan", edgecolors="black")
ax_risque.set_title("Habitations brûlées selon le point de départ")
ax_risque.set_xticks([])
ax_risque.set_yticks([])
fig.colorbar(nuage, ax=ax_risque, label="cases d'habitation brûlées (moyenne)")
fig.tight_layout()
plt.show()
