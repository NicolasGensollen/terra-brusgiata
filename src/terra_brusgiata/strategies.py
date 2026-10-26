import numpy as np
 
from .foret import ARBRE, FEU, HABITATION
from .jeu import MAX_ACTIONS_PAR_TOUR, REGLES, zone_autour_du_feu, Strategie


def proteger_maisons(etat: dict, budget: int, tour: int) -> Strategie:
    """Protège les habitations intactes les plus menacées par le feu."""
    grille, vegetation = etat["grille"], etat["vegetation"]
    a_proteger = (
        (vegetation == HABITATION) & 
        (grille == ARBRE) & 
        (etat["protection"] == 0) & 
        zone_autour_du_feu(grille, 4)
    )
    n = min(MAX_ACTIONS_PAR_TOUR, budget // REGLES["protection"]["cout"])
    return [
        ("protection", int(l), int(c)) 
        for l, c in np.argwhere(a_proteger)[:n]
    ]

