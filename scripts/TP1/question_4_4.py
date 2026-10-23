import numpy as np

from terra_brusgiata.affichage import animer
from terra_brusgiata.foret import allumer_bord_gauche, creer_etat, creer_foret, simuler

for p_base in (0.3, 0.6, 0.8, 1.0):
    rng = np.random.default_rng(0)
    grille = creer_foret(150, 150, 0.7, rng)
    allumer_bord_gauche(grille)
    historique = simuler(creer_etat(grille), rng, p_base=p_base)
    print(f"p_base = {p_base} : {len(historique) - 1} tours")
    animation = animer(historique)   # garder la variable, sinon l'animation est détruite
