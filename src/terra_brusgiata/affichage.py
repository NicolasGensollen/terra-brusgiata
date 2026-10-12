import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from .foret import creer_foret


COULEURS = ["#d9c7a3", "#2e8b3a", "#ff7a00", "#3a3a3a"]   # vide, arbre, feu, cendre
NOMS = ["Vide", "Arbre", "Feu", "Cendre"]
CMAP = ListedColormap(COULEURS)
 
 
def dessiner(ax, grille, titre : str =""):
    """Dessine une grille dans des axes existants et renvoie l'image."""
    image = ax.imshow(grille, cmap=CMAP, vmin=0, vmax=3, interpolation="nearest")
    ax.set_title(titre)
    ax.set_xticks([])
    ax.set_yticks([])
    return image
 
 
def afficher(grille, titre : str =""):
    """Affiche une grille dans une nouvelle figure."""
    fig, ax = plt.subplots()
    dessiner(ax, grille, titre)
    legende(ax)
    plt.show()


def legende(ax):
    """Ajoute à ax une légende avec la couleur de chaque état."""
    poignees = [Patch(color=c, label=n) for c, n in zip(COULEURS, NOMS)]
    ax.legend(handles=poignees, loc="upper right", fontsize=8)


def comparer_densites(densites, graine: int = 0, taille: int = 100):
    """Question 2.3 : forêts de différentes densités côte à côte."""
    fig, axes = plt.subplots(1, len(densites), figsize=(4 * len(densites), 4))
    for ax, d in zip(axes, densites):
        rng = np.random.default_rng(graine)
        dessiner(ax, creer_foret(taille, taille, d, rng), f"densité {d}")
    plt.show()


