import time

import matplotlib.pyplot as plt
import numpy as np

from terra_brusgiata.affichage import image_terrain
from terra_brusgiata.cartes import charger_carte
from terra_brusgiata.foret import ARBRE, CENDRE, FEU, HABITATION, simuler, vent_depuis_angle
from terra_brusgiata.terrain import creer_etat_terrain


N_DEPARTS = 2000        # nombre de points de départ testés
N_GRAINES = 3          # simulations par point de départ
P_BASE = 0.6
VENT = vent_depuis_angle(0)    # vent d'ouest, soufflant vers l'est
FORCE_VENT = 0.5

carte = charger_carte("./maps/golfe_ajaccio.txt")
vegetation, altitude = carte["vegetation"], carte["altitude"]
taille_case = carte["taille_case"]


def habitations_brulees(ligne, colonne):
    """Nombre moyen de cases d'habitation brûlées pour un feu parti de (ligne, colonne)."""
    total = 0
    for graine in range(N_GRAINES):
        etat = creer_etat_terrain(vegetation, altitude, taille_case)
        etat["vent"], etat["force_vent"] = VENT, FORCE_VENT
        etat["grille"][ligne, colonne] = FEU
        fin = simuler(etat, np.random.default_rng(graine), p_base=P_BASE)[-1]
        total += np.count_nonzero((fin == CENDRE) & (vegetation == HABITATION))
    return total / N_GRAINES


# 1. Tirer au hasard des points de départ parmi les cases combustibles (hors habitations)
rng = np.random.default_rng(2026)
candidats = np.argwhere((carte["grille"] == ARBRE) & (vegetation != HABITATION))
departs = candidats[rng.choice(len(candidats), N_DEPARTS, replace=False)]

# 2. Simuler un incendie depuis chacun d'eux
debut = time.perf_counter()
risque = np.array([habitations_brulees(l, c) for l, c in departs])
print(f"{N_DEPARTS * N_GRAINES} simulations en {time.perf_counter() - debut:.0f} s")
print(f"Départs sans aucune habitation brûlée : {np.mean(risque == 0):.0%}")
for rang in np.argsort(risque)[::-1][:5]:
    ligne, colonne = departs[rang]
    print(f"  départ ({ligne}, {colonne}) : {risque[rang]:.0f} cases d'habitation brûlées")

# 3. Carte de risque : les points de départ, colorés selon les habitations brûlées
fig, ax = plt.subplots(figsize=(11, 6.5))
fond = 0.45 * image_terrain(carte["grille"], vegetation) + 0.55   # terrain pâli
ax.imshow(fond, interpolation="nearest")
ax.contour(altitude, levels=10, colors="black", linewidths=0.3, alpha=0.4)
ordre = np.argsort(risque)                    # les points les plus dangereux par-dessus
nuage = ax.scatter(departs[ordre, 1], departs[ordre, 0], c=risque[ordre],
                   cmap="inferno_r", s=18, edgecolors="none")
fig.colorbar(nuage, ax=ax, label="cases d'habitation brûlées (moyenne)", shrink=0.8)
ax.set_title("Carte de risque : habitations menacées selon le point de départ du feu")
ax.set_xticks([])
ax.set_yticks([])
fig.tight_layout()
plt.show()
