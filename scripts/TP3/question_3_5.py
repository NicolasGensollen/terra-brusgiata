import matplotlib.pyplot as plt
import numpy as np

from terra_brusgiata.affichage import animer_partie, image_partie, legende_terrain
from terra_brusgiata.cartes import charger_carte
from terra_brusgiata.foret import FEU, vent_depuis_angle
from terra_brusgiata.jeu import jouer, resumer_journal


# 1. La carte du golfe d'Ajaccio, un feu au nord de la ville, un vent d'ouest
etat = charger_carte("./maps/golfe_ajaccio.txt")
etat["grille"][45, 60] = FEU
etat["vent"] = vent_depuis_angle(0)
etat["force_vent"] = 0.5

# 2. Une stratégie « scénarisée » : un plan d'actions fixé à l'avance, tour par tour.
#    Elle utilise les quatre actions, et commet volontairement quelques erreurs.
PLAN = {
    3: [("eau", 45, 66)],                                   # trop tôt : refusée
    5: [("protection", 48, 62), ("protection", 49, 61),     # maisons au sud du feu
        ("protection", 49, 62), ("protection", 50, 61),
        ("protection", 30, 30)],                            # pas une maison : refusée
    6: [("parefeu", ligne, 72) for ligne in range(37, 42)],     # ligne de pare-feux
    7: [("parefeu", ligne, 72) for ligne in range(42, 47)],     # à l'est du feu,
    8: [("parefeu", ligne, 72) for ligne in range(47, 52)],     # en aval du vent
    9: [("eau", 45, 67), ("contre_feu", 45, 71)],           # eau et contre-feu adossé
    10: [("parefeu", 45, 61)],                              # déjà brûlée : refusée
    12: [("eau", 38, 66)] + [("parefeu", 36, c) for c in range(66, 71)],  # 6 actions
}


def demonstration(etat, budget, tour):
    return PLAN.get(tour, [])


resultat = jouer(etat, demonstration, np.random.default_rng(1), budget=60, p_base=0.6)

# 3. Le journal : un résumé, puis le détail des refus
resumer_journal(resultat)
print("\nDétail des refus :")
for tour, action, message in resultat["journal"]:
    if message != "ok":
        print(f"  tour {tour:2} : {action} -> {message}")
print(f"\nPartie terminée en {len(resultat['historique']) - 1} tours, "
      f"budget restant : {resultat['budget_restant']}")

# 4. Trois instantanés de la partie, zoomés sur la zone des actions
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for ax, tour in zip(axes, (9, 13, 30)):
    ax.imshow(image_partie(resultat, tour), interpolation="nearest")
    ax.set_xlim(48, 88)          # colonnes affichées
    ax.set_ylim(62, 28)          # lignes affichées, de bas en haut
    ax.set_title(f"Tour {tour} — budget restant : {resultat['budgets'][tour]}")
    ax.set_xticks([])
    ax.set_yticks([])
legende_terrain(axes[2])
fig.tight_layout()
plt.show()

# 5. L'animation complète
animation = animer_partie(resultat, altitude=etat["altitude"])
