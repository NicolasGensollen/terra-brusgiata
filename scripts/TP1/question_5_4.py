import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from terra_brusgiata.affichage import dessiner, legende
from terra_brusgiata.foret import (
    allumer_bord_gauche,
    compter,
    creer_etat,
    creer_foret,
    humidite_aleatoire,
    humidite_riviere,
    humidite_uniforme,
    simuler
)


def animer_avec_humidite(historique, humidite, titre, intervalle=50):
    """Rejoue l'incendie à gauche, avec la carte d'humidité fixe à droite."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    fig.suptitle(titre)
    image = dessiner(ax1, historique[0], "Tour 0")
    legende(ax1)
    carte = ax2.imshow(humidite, cmap="Blues", vmin=0, vmax=1)
    ax2.set_title("Humidité")
    fig.colorbar(carte, ax=ax2)

    def mise_a_jour(i):
        image.set_data(historique[i])
        ax1.set_title(f"Tour {i}")
        return [image]

    animation = FuncAnimation(fig, mise_a_jour, frames=len(historique),
                              interval=intervalle, repeat=False)
    plt.show()
    return animation


scenarios = [
    ("Humidité uniforme 0,3", lambda forme, rng: humidite_uniforme(forme, 0.3)),
    ("Humidité aléatoire jusqu'à 0,6", lambda forme, rng: humidite_aleatoire(forme, 0.6, rng)),
    ("Rivière en colonne 50, zone de 10 cases", lambda forme, rng: humidite_riviere(forme, 50, 10)),
]

for titre, fabriquer_humidite in scenarios:
    rng = np.random.default_rng(0)
    grille = creer_foret(100, 100, 0.9, rng)
    allumer_bord_gauche(grille)
    etat = creer_etat(grille)
    etat["humidite"] = fabriquer_humidite(grille.shape, rng)
    historique = simuler(etat, rng, p_base=1.0, max_tours=5000)

    debut, fin = compter(historique[0]), compter(historique[-1])
    brules = fin["cendre"] / (debut["arbre"] + debut["feu"])
    print(f"{titre} : {brules:.0%} des arbres brûlés en {len(historique) - 1} tours")

    animation = animer_avec_humidite(historique, etat["humidite"], titre)
