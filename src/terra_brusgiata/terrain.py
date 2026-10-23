import numpy as np
 
from .foret import ARBRE, INFLAMMABILITE, VIDE, creer_etat
 
# Tableau d'inflammabilité indexé par le type : TABLE_INFLAMMABILITE[MAQUIS] == 1.3
TABLE_INFLAMMABILITE = np.array([INFLAMMABILITE[t] for t in sorted(INFLAMMABILITE)])
 
 
def grille_depuis_vegetation(vegetation):
    """Grille d'états initiale : ARBRE sur les cases combustibles, VIDE ailleurs."""
    return np.where(TABLE_INFLAMMABILITE[vegetation] > 0, ARBRE, VIDE).astype(np.int8)
 
 
def creer_etat_terrain(vegetation, altitude, taille_case):
    """État complet à partir d'une carte de végétation, d'un relief et
    de la taille des cases."""
    etat = creer_etat(grille_depuis_vegetation(vegetation))
    etat["vegetation"] = vegetation
    etat["altitude"] = altitude
    etat["taille_case"] = taille_case
    return etat


