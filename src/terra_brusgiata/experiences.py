import time
 
import matplotlib.pyplot as plt
import numpy as np
 
from foret import (
    ARBRE,
    CENDRE,
    FEU,
    allumer_bord_gauche,
    creer_etat,
    creer_foret,
    simuler
)
 
 
def bilan(historique: list[np.ndarray]) -> dict:
    """Statistiques d'un incendie à partir de son historique."""
    debut, fin = historique[0], historique[-1]
    vegetation = np.count_nonzero((debut == ARBRE) | (debut == FEU))
    brules = np.count_nonzero((fin == CENDRE) | (fin == FEU))
    return {
        "proportion_brulee": brules / vegetation if vegetation else 0.0,
        "duree": len(historique) - 1,
        "max_en_feu": max(int(np.count_nonzero(g == FEU)) for g in historique),
    }


