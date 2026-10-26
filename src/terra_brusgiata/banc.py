import copy
import os
import time
 
import numpy as np
 
from .jeu import jouer, ne_rien_faire, score
from .scenarios import charger_scenario
 
 
def charger_scenarios(chemins: list[str]) -> list[dict]:
    """Renvoie un dictionnaire {nom du scénario : (état de départ,
    paramètres)}."""
    scenarios = {}
    for chemin in chemins:
        nom = os.path.splitext(os.path.basename(chemin))[0]
        scenarios[nom] = charger_scenario(chemin)
    return scenarios


