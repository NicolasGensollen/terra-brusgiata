import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from terra_brusgiata.affichage import dessiner, legende
from terra_brusgiata.foret import allumer, creer_etat, creer_foret, simuler_vent_variable, vent_depuis_angle


def bascule(tour):
    return vent_depuis_angle(0) if tour < 30 else vent_depuis_angle(180)


SCENARIOS = [
    ("Vent constant vers la droite", lambda tour: vent_depuis_angle(0)),
    ("Vent qui tourne de 2° par tour", lambda tour: vent_depuis_angle(2 * tour)),
    ("Vent qui bascule au tour 30", bascule),
]

# 1. Simuler les trois incendies
historiques = []
for titre, vent_au_tour in SCENARIOS:
    rng = np.random.default_rng(7)
    grille = creer_foret(121, 121, 1.0, rng)     # forêt pleine et sèche
    allumer(grille, 60, 60)                      # foyer au centre
    etat = creer_etat(grille)
    etat["force_vent"] = 0.8
    historiques.append(simuler_vent_variable(etat, rng, vent_au_tour,
                                             p_base=0.7, max_tours=80))

# 2. Une image et une flèche de vent par incendie
fig, axes = plt.subplots(1, 3, figsize=(13, 4.5))
images, fleches = [], []
for ax, historique, (titre, vent_au_tour) in zip(axes, historiques, SCENARIOS):
    images.append(dessiner(ax, historique[0], titre))
    dy, dx = vent_au_tour(0)
    # flèche en haut à gauche ; angles="xy" respecte l'axe vertical vers le bas
    fleches.append(ax.quiver(12, 12, dx, dy, angles="xy", scale_units="xy",
                             scale=0.07, color="#1f5fbf", width=0.02))
legende(axes[0])
titre_general = fig.suptitle("Tour 0")
nb_images = max(len(h) for h in historiques)


# 3. Mettre à jour les grilles et les flèches à chaque tour
def mise_a_jour(i):
    for image, fleche, historique, (_, vent_au_tour) in zip(images, fleches,
                                                           historiques, SCENARIOS):
        image.set_data(historique[min(i, len(historique) - 1)])
        dy, dx = vent_au_tour(max(i - 1, 0))     # vent utilisé pour arriver ici
        fleche.set_UVC(dx, dy)
    titre_general.set_text(f"Tour {i}")
    return images + fleches + [titre_general]


animation = FuncAnimation(fig, mise_a_jour, frames=nb_images,
                          interval=80, repeat=False)
plt.show()
