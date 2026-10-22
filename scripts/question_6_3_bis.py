import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from terra_brusgiata.affichage import dessiner, legende
from terra_brusgiata.foret import allumer, creer_etat, creer_foret, simuler, vent_depuis_angle

FORCES = (0, 0.5, 1)

# 1. Simuler les trois incendies
historiques = []
for force in FORCES:
    rng = np.random.default_rng(7)
    grille = creer_foret(121, 121, 1.0, rng)     # forêt pleine et sèche
    allumer(grille, 60, 40)
    etat = creer_etat(grille)
    etat["vent"] = vent_depuis_angle(0)          # vent soufflant vers la droite
    etat["force_vent"] = force
    historiques.append(simuler(etat, rng, p_base=0.7, max_tours=45))

# 2. Préparer une figure avec une image par incendie
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
images = [dessiner(ax, h[0], f"force du vent {force}")
          for ax, h, force in zip(axes, historiques, FORCES)]
legende(axes[0])
titre = fig.suptitle("Tour 0")
nb_images = max(len(h) for h in historiques)


# 3. Mettre à jour les trois images en même temps
def mise_a_jour(i):
    for image, historique in zip(images, historiques):
        # un incendie déjà éteint reste figé sur sa dernière grille
        image.set_data(historique[min(i, len(historique) - 1)])
    titre.set_text(f"Tour {i}")
    return images + [titre]


animation = FuncAnimation(fig, mise_a_jour, frames=nb_images,
                          interval=100, repeat=False)
plt.show()
