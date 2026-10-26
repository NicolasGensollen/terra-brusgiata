import os

import matplotlib.pyplot as plt
import numpy as np

from terra_brusgiata.affichage import dessiner_terrain, image_partie, legende_terrain
from terra_brusgiata.foret import FEU, NOMS_TYPES
from terra_brusgiata.jeu import ne_rien_faire
from terra_brusgiata.scenarios import charger_scenario, jouer_scenario


CHEMIN = "scenarios/alata.json"

# ---------------------------------------------------------------- question 5.1
etat, parametres = charger_scenario(CHEMIN)
print("Paramètres :", parametres)
foyers = [tuple(int(x) for x in case) for case in np.argwhere(etat["grille"] == FEU)]
print("Foyers allumés :", foyers,
      "dans :", [NOMS_TYPES[etat["vegetation"][l, c]] for l, c in foyers])
print("Vent :", etat["vent"], " force :", etat["force_vent"])
print("Carte :", etat["vegetation"].shape, " taille des cases :", etat["taille_case"])

# Le chemin de la carte doit marcher quel que soit le dossier de lancement
dossier_initial = os.getcwd()
os.chdir("..")
try:
    charger_scenario(os.path.join(dossier_initial, CHEMIN))
    print("Chargement depuis un autre dossier : OK")
finally:
    os.chdir(dossier_initial)

fig, ax = plt.subplots(figsize=(9, 6))
dessiner_terrain(ax, etat["grille"], etat["vegetation"],
                 parametres["titre"], etat["altitude"])
for ligne, colonne in foyers:
    ax.plot(colonne, ligne, "o", ms=14, mfc="none", mec="orange", mew=2.5)
legende_terrain(ax)
fig.tight_layout()
plt.show()


# ---------------------------------------------------------------- question 5.2
def ligne_de_parefeux(etat, budget, tour):
    """Petite stratégie de test : une ligne de pare-feux à l'est du foyer."""
    if 5 <= tour <= 8:
        debut = 37 + 5 * (tour - 5)
        return [("parefeu", ligne, 72) for ligne in range(debut, debut + 5)]
    return []


# Une stratégie qui ne fait rien doit avoir un gain nul
resultat = jouer_scenario(CHEMIN, ne_rien_faire)
print(f"\nne_rien_faire : score {resultat['score']}, "
      f"référence {resultat['score_reference']}, gain {resultat['gain']}")
assert resultat["gain"] == 0

# Rejouer le même scénario donne exactement le même résultat
for strategie in (ligne_de_parefeux, ligne_de_parefeux):
    resultat = jouer_scenario(CHEMIN, strategie)
    print(f"{strategie.__name__} : score {resultat['score']}, "
          f"référence {resultat['score_reference']}, gain {resultat['gain']}")

# Comparaison visuelle : fin de partie sans intervention et avec la stratégie
reference = jouer_scenario(CHEMIN, ne_rien_faire)
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
for ax, res, nom in ((axes[0], reference, "Sans intervention"),
                     (axes[1], resultat, "Avec une ligne de pare-feux")):
    fin = len(res["historique"]) - 1
    ax.imshow(image_partie(res, fin), interpolation="nearest")
    ax.set_title(f"{nom} : score {res['score']}, fin au tour {fin}")
    ax.set_xticks([])
    ax.set_yticks([])
legende_terrain(axes[1])
fig.tight_layout()
plt.show()
