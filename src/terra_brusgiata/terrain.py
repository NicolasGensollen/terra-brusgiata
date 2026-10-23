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


def colline(forme, ligne, colonne, hauteur, rayon):
    """Colline en cloche (gaussienne) centrée sur (ligne, colonne)."""
    lignes = np.arange(forme[0])[:, np.newaxis]     # colonne de numéros de ligne
    colonnes = np.arange(forme[1])[np.newaxis, :]   # ligne de numéros de colonne
    d2 = (lignes - ligne) ** 2 + (colonnes - colonne) ** 2
    return hauteur * np.exp(-d2 / (2 * rayon ** 2))


def relief_collines(forme, collines):
    """Somme de collines, données par une liste de
    (ligne, colonne, hauteur, rayon)."""
    altitude = np.zeros(forme)
    for ligne, colonne, hauteur, rayon in collines:
        altitude += colline(forme, ligne, colonne, hauteur, rayon)
    return altitude


def plan_incline(forme, pente_degres, taille_case):
    """Terrain qui monte vers le haut de la carte avec une pente constante."""
    denivele_par_case = taille_case * np.tan(np.radians(pente_degres))
    lignes = np.arange(forme[0])[:, np.newaxis]
    return np.tile((forme[0] - 1 - lignes) * denivele_par_case, (1, forme[1]))


def lisser(altitude: np.ndarray) -> np.ndarray:
    """Remplace chaque case par la moyenne d'elle-même et de ses 4 voisines."""
    bord = np.pad(altitude, 1, mode="edge")      # recopie les bords
    return (
        bord[1:-1, 1:-1] + 
        bord[:-2, 1:-1] + 
        bord[2:, 1:-1] + 
        bord[1:-1, :-2] + 
        bord[1:-1, 2:]
    ) / 5


def relief_aleatoire(forme: tuple[int, int], amplitude, n_lissages: int, rng):
    """Relief aléatoire : bruit lissé n_lissages fois, puis ramené entre 0 et amplitude."""
    altitude = rng.random(forme)
    for _ in range(n_lissages):
        altitude = lisser(altitude)
    altitude = altitude - altitude.min()
    return amplitude * altitude / altitude.max()

