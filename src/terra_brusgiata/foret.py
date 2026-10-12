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


def allumer(grille , ligne : int, colonne : int):
    """Met le feu à la case (ligne, colonne) si elle porte un arbre.

    Modifie la grille en place et ne renvoie rien.
    """
    if grille[ligne, colonne] == ARBRE:
        grille[ligne, colonne] = FEU


def allumer_bord_gauche(grille):
    """Enflamme les arbres de la première colonne. Modifie la grille en place."""
    colonne = grille[:, 0]
    colonne[colonne == ARBRE] = FEU


def compter(grille):
    """Renvoie le nombre de cases dans chaque état, sous forme de dictionnaire."""
    return {
        nom: int(np.count_nonzero(grille == etat))
        for etat, nom in NOMS_ETATS.items()
    }


