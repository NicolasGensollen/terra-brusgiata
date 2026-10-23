import numpy as np
 
from terra_brusgiata.foret import (
    CENDRE,
    allumer_bord_gauche,
    creer_etat,
    creer_foret,
    humidite_riviere,
    simuler
)
 
 
def taux_arret(largeur_zone, n_essais=40):
    """Proportion des essais où le feu ne franchit pas la rivière (colonne 50)."""
    arrets = 0
    for graine in range(n_essais):
        rng = np.random.default_rng(graine)
        grille = creer_foret(100, 100, 0.9, rng)
        allumer_bord_gauche(grille)
        etat = creer_etat(grille)
        etat["humidite"] = humidite_riviere(grille.shape, 50, largeur_zone)
        fin = simuler(etat, rng, p_base=1.0, max_tours=5000)[-1]
        if not np.any(fin[:, 51:] == CENDRE):
            arrets += 1
    return arrets / n_essais
 

print("Largeur de la zone humide | Proportion des feux stoppés")
for largeur_zone in range(0, 21, 2):
    print(f"{largeur_zone} cases \t\t\t\t{taux_arret(largeur_zone) * 100}%")

