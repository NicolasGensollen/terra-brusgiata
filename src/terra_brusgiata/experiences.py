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


def experience(
    densite: float,
    n_repetitions: int,
    graine: int,
    taille: int = 100,
    p_base: float = 1.0
) -> tuple[float, float]:
    """Lance n_repetitions simulations indépendantes.

    Renvoie (moyenne, écart-type) de la proportion d'arbres brûlés.
    """
    graines = np.random.SeedSequence(graine).spawn(n_repetitions)
    proportions = []
    for graine in graines:
        rng = np.random.default_rng(graine)
        grille = creer_foret(taille, taille, densite, rng)
        allumer_bord_gauche(grille)
        historique = simuler(
            creer_etat(grille),
            rng,
            p_base=p_base,
            max_tours=10_000
        )
        proportions.append(bilan(historique)["proportion_brulee"])
    return float(np.mean(proportions)), float(np.std(proportions))


