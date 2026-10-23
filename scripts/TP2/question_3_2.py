import matplotlib.pyplot as plt

from terra_brusgiata.affichage import dessiner_terrain, legende_terrain
from terra_brusgiata.cartes import lire_vegetation
from terra_brusgiata.foret import NOMS_TYPES
from terra_brusgiata.terrain import grille_depuis_vegetation

# 1. Quelques fichiers de carte, un correct et plusieurs avec une erreur
CARTE_CORRECTE = """\
# Petite vallée avec village
# taille_case = 50
TTTTTTTmmmmmmm....~~....mmmTTT
TTTTTTmmmmmmm.....~~.....mmmTT
TTTTTmmmmmm....HH.~~......mmmT
TTTTmmmmm.....HHH.~~.......mmm
TTTmmmmm......HH..~~........mm

==============================
TTmmmm........^^..~~......mmmm
TTTmmmm......^^^^.~~.....mmmTT
TTTTmmmmm.....^^..~~....mmmTTT
"""
fichiers = {
    "correcte.txt": CARTE_CORRECTE,
    "symbole_inconnu.txt": "# taille_case = 50\nTTTmm..~\nTTmXm..~\n",
    "ligne_trop_longue.txt": "# taille_case = 50\nTTTmm..~\nTTmmm..~~~\n",
    "sans_taille.txt": "# Une carte sans taille de case\nTTTmm..~\n",
    "espace_en_fin.txt": "# taille_case = 50\nTTTmm..~ \n",
}
for nom, contenu in fichiers.items():
    with open(nom, "w", encoding="utf-8") as fichier:
        fichier.write(contenu)

# 2. Lecture de la carte correcte
vegetation, taille_case = lire_vegetation("correcte.txt")
print("Carte correcte :")
print("  forme :", vegetation.shape, " taille_case :", taille_case)
print("  première ligne :", [NOMS_TYPES[t] for t in vegetation[0, :8]], "...")

# 3. Lecture des cartes incorrectes : chacune doit lever une ValueError
print("\nCartes incorrectes :")
for nom in fichiers:
    if nom == "correcte.txt":
        continue
    try:
        lire_vegetation(nom)
        print(f"  {nom} : aucune erreur détectée (problème !)")
    except ValueError as erreur:
        print(f"  {erreur}")

# 4. Affichage de la carte correcte, à côté du texte du fichier
fig, (ax_texte, ax_carte) = plt.subplots(1, 2, figsize=(13, 4))
lignes_carte = [l for l in CARTE_CORRECTE.splitlines() if l and not l.startswith("#")]
ax_texte.text(0, 1, "\n".join(lignes_carte), family="monospace", fontsize=10,
              va="top", transform=ax_texte.transAxes)
ax_texte.set_title("Contenu du fichier")
ax_texte.axis("off")

grille = grille_depuis_vegetation(vegetation)
hauteur, largeur = vegetation.shape
dessiner_terrain(ax_carte, grille, vegetation,
                 f"Carte lue : {hauteur} × {largeur} cases de {taille_case:g} m")
legende_terrain(ax_carte)
fig.tight_layout()
plt.show()
