import numpy as np
 
from foret import ARBRE, FEU, HABITATION, PAREFEU, VIDE
 

REGLES = {
    "parefeu": {"cout": 1},
    "eau": {"cout": 6, "humidite": 0.9},          # zone de 3 × 3 cases
    "contre_feu": {"cout": 1},
    "protection": {"cout": 3, "duree": 15},
}
MAX_ACTIONS_PAR_TOUR = 5
DELAI_INTERVENTION = 5       # premier tour où l'on peut agir
DISTANCE_SECURITE = 3        # distance minimale au feu pour creuser un pare-feu
EVAPORATION = 0.1            # part de l'humidité ajoutée évaporée à chaque tour
POIDS_HABITATION = 20

