import numpy as np

VIDE = 0
ARBRE = 1
FEU = 2
CENDRE = 3
 
NOMS_ETATS = {
    VIDE: "vide",
    ARBRE: "arbre", 
    FEU: "feu",
    CENDRE: "cendre"
}
 
 
def creer_foret(hauteur : int, largeur : int, densite : int, rng):
    """Renvoie une grille où chaque case est ARBRE avec une probabilité densite, VIDE sinon."""
    tirages = rng.random((hauteur, largeur))
    return np.where(tirages < densite, ARBRE, VIDE).astype(np.int8)

