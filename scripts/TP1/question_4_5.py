import numpy as np

from terra_brusgiata.foret import allumer_bord_gauche, compter, creer_etat, creer_foret, simuler

def lancer(graine_foret, graine_feu, taille=150, densite=0.7, p_base=0.6):
    """Crée une forêt, allume le bord gauche et simule l'incendie."""
    grille = creer_foret(taille, taille, densite, np.random.default_rng(graine_foret))
    allumer_bord_gauche(grille)
    return simuler(creer_etat(grille), np.random.default_rng(graine_feu), p_base=p_base)
 
 
def proportion_brulee(historique):
    """Proportion des arbres initiaux (y compris ceux en feu) qui ont brûlé."""
    debut, fin = compter(historique[0]), compter(historique[-1])
    return (fin["cendre"] + fin["feu"]) / (debut["arbre"] + debut["feu"])
 
 
for graine in range(5):
    historique = lancer(graine_foret=0, graine_feu=graine, p_base=0.8)
    print(f"graine {graine} : {proportion_brulee(historique):6.1%} brûlés "
          f"en {len(historique) - 1} tours")
 
fin_1 = lancer(graine_foret=0, graine_feu=42)[-1]
fin_2 = lancer(graine_foret=0, graine_feu=42)[-1]
print("Même graine, grilles finales identiques :", np.array_equal(fin_1, fin_2))

