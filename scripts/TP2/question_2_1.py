from terra_brusgiata.foret import facteur_pente

import math


TAILLE_CASE = 100.0   # mètres ; n'importe quelle valeur positive convient

print(f"{'Pente':>6} | {'dz (m)':>7} | {'Facteur':>7}")
print("-" * 27)
for angle in (0, 10, -10, 30):
    dz = TAILLE_CASE * math.tan(math.radians(angle))   # dénivelé correspondant
    print(f"{angle:+5d}° | {dz:7.1f} | {facteur_pente(dz, TAILLE_CASE):7.2f}")

# Vérification : montée et descente se compensent
for angle in (10, 30):
    dz = TAILLE_CASE * math.tan(math.radians(angle))
    produit = facteur_pente(dz, TAILLE_CASE) * facteur_pente(-dz, TAILLE_CASE)
    print(f"facteur(+{angle}°) × facteur(-{angle}°) = {produit:.6f}")
