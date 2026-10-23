import os
import sys
 
import matplotlib.pyplot as plt
import numpy as np
 
from .affichage import COULEURS_TYPES
from .cartes import SYMBOLES, ecrire_vegetation, lire_vegetation
from .foret import FORET, NOMS_TYPES
 
 
def peindre(vegetation, ligne, colonne, type_terrain, taille):
    """Peint un carré de côté 2 × taille - 1 centré sur (ligne, colonne)."""
    hauteur, largeur = vegetation.shape
    l0, l1 = max(ligne - taille + 1, 0), min(ligne + taille, hauteur)
    c0, c1 = max(colonne - taille + 1, 0), min(colonne + taille, largeur)
    vegetation[l0:l1, c0:c1] = type_terrain


