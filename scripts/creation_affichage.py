import numpy as np
from terra_brusgiata.foret import creer_foret, allumer_bord_gauche, compter
from terra_brusgiata.affichage import afficher


rng = np.random.default_rng(42)
g = creer_foret(10, 10, 0.6, rng)
print(compter(g))
afficher(g)
