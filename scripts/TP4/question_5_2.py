import matplotlib.pyplot as plt

from terra_brusgiata.banc import charger_scenarios, evaluer, statistiques
from terra_brusgiata.strategies import fabrique_arrosage, fabrique_parefeux


NOMS = ("alata", "pozzo", "nord_est", "deux_foyers")
GRAINES = range(20)                    # graines d'entraînement
REGLAGES = {"parefeux": (fabrique_parefeux, (3, 4, 5, 6, 7, 8, 10), "distance"),
            "arrosage": (fabrique_arrosage, (0, 1, 2, 3, 4, 6, 8), "avance")}

scenarios = charger_scenarios([f"scenarios/{nom}.json" for nom in NOMS])
references = {}

# 1. Évaluer chaque valeur du paramètre, pour chacune des deux fabriques
resultats_reglages = {}
for nom, (fabrique, valeurs, _) in REGLAGES.items():
    for valeur in valeurs:
        lignes = evaluer(fabrique(valeur), scenarios, GRAINES, references)
        resultats_reglages[(nom, valeur)] = lignes
        s = statistiques([l["gain"] for l in lignes])
        print(f"{nom} {valeur:2} : gain moyen {s['moyenne']:5.0f}, "
              f"IC 95 % [{s['ic_bas']:.0f} ; {s['ic_haut']:.0f}]")

# 2. Le gain moyen en fonction du paramètre, avec les intervalles de confiance
fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
for ax, (nom, (fabrique, valeurs, parametre)) in zip(axes, REGLAGES.items()):
    stats = [statistiques([l["gain"] for l in resultats_reglages[(nom, v)]])
             for v in valeurs]
    ax.errorbar(valeurs, [s["moyenne"] for s in stats],
                yerr=[1.96 * s["erreur_type"] for s in stats],
                marker="o", capsize=4)
    ax.set_title(fabrique.__name__)
    ax.set_xlabel(parametre)
    ax.grid(alpha=0.3)
axes[0].set_ylabel("gain moyen (graines 0 à 19)")
fig.tight_layout()
plt.show()
