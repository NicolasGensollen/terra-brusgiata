import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from .foret import creer_foret, CENDRE, FEU, NOMS_TYPES
from matplotlib.animation import FuncAnimation


COULEURS = ["#d9c7a3", "#2e8b3a", "#ff7a00", "#3a3a3a"]   # vide, arbre, feu, cendre
NOMS = ["Vide", "Arbre", "Feu", "Cendre"]
CMAP = ListedColormap(COULEURS)

COULEURS_TYPES = np.array([
    [0.23, 0.48, 0.84],   # eau
    [0.62, 0.62, 0.62],   # roche
    [0.33, 0.33, 0.33],   # route
    [0.79, 0.84, 0.49],   # prairie
    [0.48, 0.60, 0.23],   # maquis
    [0.12, 0.42, 0.18],   # forêt
    [0.85, 0.33, 0.31],   # habitation
    [0.80, 0.66, 0.47],   # pare-feu
])
COULEUR_FEU = np.array([1.0, 0.48, 0.0])
COULEUR_CENDRE = np.array([0.15, 0.15, 0.15])
COULEUR_EAU_LARGUEE = np.array([0.25, 0.55, 1.0])

 
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


def image_terrain(grille: np.ndarray, vegetation: np.ndarray) -> np.ndarray:
    """Image RGB : couleur de la végétation, sauf sur le feu et la cendre."""
    image = COULEURS_TYPES[vegetation]          # forme (hauteur, largeur, 3)
    image[grille == FEU] = COULEUR_FEU
    image[grille == CENDRE] = COULEUR_CENDRE
    return image


def legende_terrain(ax):
    """Légende des types de végétation, du feu et de la cendre."""
    poignees = [
        Patch(color=COULEURS_TYPES[t], label=nom)
        for t, nom in NOMS_TYPES.items()
    ]
    poignees += [
        Patch(color=COULEUR_FEU, label="feu"),
        Patch(color=COULEUR_CENDRE, label="cendre")
    ]
    ax.legend(
        handles=poignees,
        loc="upper left",
        bbox_to_anchor=(1.01, 1),
        fontsize=8
    )


def dessiner_terrain(ax, grille: np.ndarray, vegetation: np.ndarray, titre: str = "", altitude=None):
    """Dessine le terrain dans ax et renvoie l'image créée."""
    image = ax.imshow(
        image_terrain(grille, vegetation),
        interpolation="nearest"
    )
    if altitude is not None and altitude.max() > altitude.min():
        ax.contour(
            altitude,
            levels=10,
            colors="black",
            linewidths=0.4,
            alpha=0.6
        )
    ax.set_title(titre)
    ax.set_xticks([])
    ax.set_yticks([])
    return image


def animer_terrain(historique: list[np.ndarray], vegetation: np.ndarray, intervalle: int = 50, altitude=None):
    """Rejoue un historique sur le terrain. Renvoie l'animation."""
    fig, ax = plt.subplots(figsize=(9, 6))
    image = dessiner_terrain(ax, historique[0], vegetation, "Tour 0", altitude)
    legende_terrain(ax)
    fig.tight_layout()

    def mise_a_jour(i):
        image.set_data(image_terrain(historique[i], vegetation))
        ax.set_title(f"Tour {i}")
        return [image]

    animation = FuncAnimation(fig, mise_a_jour, frames=len(historique),
                              interval=intervalle, repeat=False)
    plt.show()
    return animation


def afficher_relief(altitude, titre="Relief"):
    """Affiche le relief en couleurs, avec courbes de niveau et barre d'échelle."""
    fig, ax = plt.subplots()
    image = ax.imshow(altitude, cmap="terrain")
    ax.contour(altitude, levels=10, colors="black", linewidths=0.4)
    ax.set_title(titre)
    fig.colorbar(image, ax=ax, label="altitude (m)")
    plt.show()


def image_partie(resultat: dict, i: int) -> np.ndarray:
    """Image du tour i d'une partie : terrain, feu, pare-feux et eau larguée."""
    image = image_terrain(resultat["historique"][i], resultat["vegetations"][i])
    eau = resultat["humidites"][i] - resultat["humidites"][0]     # humidité ajoutée
    opacite = np.clip(eau, 0, 1)[:, :, np.newaxis] * 0.7
    return (1 - opacite) * image + opacite * COULEUR_EAU_LARGUEE


def animer_partie(resultat: dict, altitude: np.ndarray | None = None, intervalle: int = 50):
    """Rejoue une partie : feu, pare-feux, eau larguée et budget restant."""
    fig, ax = plt.subplots(figsize=(9, 6))
    image = dessiner_terrain(
        ax,
        resultat["historique"][0],
        resultat["vegetations"][0],
        "",
        altitude
    )
    image.set_data(image_partie(resultat, 0))
    legende_terrain(ax)
    fig.tight_layout()

    def mise_a_jour(i):
        image.set_data(image_partie(resultat, i))
        ax.set_title(f"Tour {i}  —  budget restant : {resultat['budgets'][i]}")
        return [image]

    animation = FuncAnimation(fig, mise_a_jour, frames=len(resultat["historique"]),
                              interval=intervalle, repeat=False)
    plt.show()
    return animation

