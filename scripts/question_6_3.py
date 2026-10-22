import matplotlib.pyplot as plt
import numpy as np
 
from terra_brusgiata.affichage import dessiner, legende
from terra_brusgiata.foret import allumer, creer_etat, creer_foret, simuler, vent_depuis_angle
 
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for ax, force in zip(axes, (0, 0.5, 1)):
    rng = np.random.default_rng(7)
    grille = creer_foret(121, 121, 1.0, rng)     # forêt pleine et sèche
    allumer(grille, 60, 40)
    etat = creer_etat(grille)
    etat["vent"] = vent_depuis_angle(0)          # vent soufflant vers la droite
    etat["force_vent"] = force
    historique = simuler(etat, rng, p_base=0.7, max_tours=45)
    dessiner(ax, historique[-1], f"force du vent {force}")
legende(axes[0])
plt.show()


