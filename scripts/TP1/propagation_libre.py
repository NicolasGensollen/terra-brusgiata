import numpy as np
from terra_brusgiata.foret import creer_foret, allumer_bord_gauche, compter, simuler_deterministe
from terra_brusgiata.affichage import afficher


rng = np.random.default_rng(42)
g = creer_foret(10, 10, 0.7, rng)
afficher(g)
print("On met le feu !")
allumer_bord_gauche(g)
afficher(g)
g2, tours = simuler_deterministe(g)
print(f"Il a fallu {tours} pour que tout brûle...")
afficher(g2)
