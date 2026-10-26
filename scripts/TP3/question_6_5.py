import json
import re
from collections import Counter

import matplotlib.pyplot as plt

from terra_brusgiata.affichage import image_partie, legende_terrain
from terra_brusgiata.scenarios import jouer_scenario
from terra_brusgiata.strategies import contre_feu_adosse, contre_feu_devant, parefeux_devant


SCENARIO = "scenarios/alata.json"
STRATEGIES = (contre_feu_devant, contre_feu_adosse, parefeux_devant)


def scenario_avec_graine(graine):
    """Copie temporaire de alata.json avec une autre graine. Renvoie son chemin."""
    with open(SCENARIO, encoding="utf-8") as fichier:
        scenario = json.load(fichier)
    scenario["graine"] = graine
    chemin = "scenarios/essai.json"         # dans le même dossier que la carte
    with open(chemin, "w", encoding="utf-8") as fichier:
        json.dump(scenario, fichier)
    return chemin


def resumer_par_raison(resultat):
    """Comme resumer_journal, mais en regroupant les refus qui ne diffèrent
    que par les coordonnées de la case."""
    journal = resultat["journal"]
    acceptees = Counter(a[0] for _, a, m in journal if m == "ok")
    refus = Counter(re.sub(r"\(-?\d+, -?\d+\)", "(…)", m)
                    for _, a, m in journal if m != "ok")
    print("  actions acceptées :", dict(acceptees))
    for raison, nombre in refus.most_common():
        print(f"  {nombre:4} refus : {raison}")


# 1. Les gains sur trois graines
print(f"{'graine':>6}" + "".join(f"{s.__name__:>20}" for s in STRATEGIES))
for graine in (1, 2, 3):
    chemin = scenario_avec_graine(graine)
    gains = [jouer_scenario(chemin, s)["gain"] for s in STRATEGIES]
    print(f"{graine:>6}" + "".join(f"{g:>20}" for g in gains))

# 2. Le détail des deux parties avec contre-feu, sur la graine du scénario
resultats = {}
for strategie in (contre_feu_devant, contre_feu_adosse):
    resultat = jouer_scenario(SCENARIO, strategie)
    resultats[strategie.__name__] = resultat
    print(f"\n{strategie.__name__} : gain {resultat['gain']}, "
          f"fin au tour {len(resultat['historique']) - 1}")
    resumer_par_raison(resultat)

# 3. Trois instantanés de chaque partie, zoomés sur le foyer
fig, axes = plt.subplots(2, 3, figsize=(15, 9))
for ligne_axes, (nom, resultat) in zip(axes, resultats.items()):
    fin = len(resultat["historique"]) - 1
    for ax, tour in zip(ligne_axes, (8, 20, fin)):
        ax.imshow(image_partie(resultat, tour), interpolation="nearest")
        ax.set_xlim(35, 100)
        ax.set_ylim(75, 15)
        ax.set_title(f"{nom} — tour {tour}")
        ax.set_xticks([])
        ax.set_yticks([])
legende_terrain(axes[0, 2])
fig.tight_layout()
plt.show()
