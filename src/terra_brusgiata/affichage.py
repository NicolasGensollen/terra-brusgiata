import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from .foret import creer_foret
from matplotlib.animation import FuncAnimation


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


def animer(historique: list[np.ndarray], intervalle: int = 50):
    """Rejoue un historique de grilles.

    Renvoie l'animation, qu'il faut garder dans une variable.
    """
    fig, ax = plt.subplots()
    image = dessiner(ax, historique[0], "Tour 0")
    legende(ax)

    def mise_a_jour(i):
        image.set_data(historique[i])
        ax.set_title(f"Tour {i}")
        return [image]

    animation = FuncAnimation(
        fig, mise_a_jour, frames=len(historique), interval=intervalle
    )
    plt.show()
    return animation


def afficher_humidite(grille, humidite):
    """Affiche la forêt et la carte d'humidité côte à côte."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    dessiner(ax1, grille, "Forêt")
    image = ax2.imshow(humidite, cmap="Blues", vmin=0, vmax=1)
    ax2.set_title("Humidité")
    fig.colorbar(image, ax=ax2)
    plt.show()

