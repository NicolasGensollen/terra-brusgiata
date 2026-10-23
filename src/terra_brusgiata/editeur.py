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


def editer_carte(vegetation):
    """Ouvre l'éditeur sur une copie de vegetation et renvoie la carte
    modifiée quand la fenêtre est fermée."""
    vegetation = vegetation.copy()
    outil = {"type": FORET, "taille": 1, "appui": False}

    fig, ax = plt.subplots(figsize=(9, 6))
    image = ax.imshow(COULEURS_TYPES[vegetation], interpolation="nearest")

    def titre():
        nom = NOMS_TYPES[outil["type"]]
        ax.set_title(f"Type : {nom}  —  pinceau : {outil['taille']}")

    def rafraichir():
        image.set_data(COULEURS_TYPES[vegetation])
        titre()
        fig.canvas.draw_idle()

    def peindre_evenement(evenement):
        if evenement.inaxes is ax and evenement.xdata is not None:
            colonne, ligne = round(evenement.xdata), round(evenement.ydata)
            peindre(vegetation, ligne, colonne, outil["type"], outil["taille"])
            rafraichir()

    def au_clic(evenement):
        if evenement.button == 1:
            outil["appui"] = True
            peindre_evenement(evenement)

    def au_relachement(evenement):
        outil["appui"] = False

    def au_mouvement(evenement):
        if outil["appui"]:
            peindre_evenement(evenement)

    def a_la_touche(evenement):
        if evenement.key in SYMBOLES:
            outil["type"] = SYMBOLES[evenement.key]
        elif evenement.key == "+":
            outil["taille"] += 1
        elif evenement.key == "-" and outil["taille"] > 1:
            outil["taille"] -= 1
        rafraichir()
 
    fig.canvas.mpl_connect("button_press_event", au_clic)
    fig.canvas.mpl_connect("button_release_event", au_relachement)
    fig.canvas.mpl_connect("motion_notify_event", au_mouvement)
    fig.canvas.mpl_connect("key_press_event", a_la_touche)
    titre()
    plt.show()
    return vegetation

def main():
    chemin = sys.argv[1]
    if os.path.exists(chemin):
        vegetation, taille_case = lire_vegetation(chemin)
    else:
        hauteur = int(input("Nombre de lignes : "))
        largeur = int(input("Nombre de colonnes : "))
        taille_case = float(input("Taille d'une case (m) : "))
        vegetation = np.full((hauteur, largeur), FORET, dtype=np.int8)
    vegetation = editer_carte(vegetation)
    ecrire_vegetation(chemin, vegetation, taille_case)
    print(f"Carte sauvegardée dans {chemin}")

