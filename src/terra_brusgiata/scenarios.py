import copy
import json
import os
 
import numpy as np
 
from .cartes import charger_carte
from .foret import FEU, vent_depuis_angle
from .jeu import jouer, ne_rien_faire, score
 
 
def charger_scenario(chemin: str) -> tuple[dict, dict]:
    """Renvoie (etat, parametres) : l'état prêt à jouer, foyers allumés et
    vent réglé, et un dictionnaire avec le titre, p_base, le budget,
    max_tours et la graine."""
    with open(chemin, encoding="utf-8") as fichier:
        scenario = json.load(fichier)
    dossier = os.path.dirname(chemin)
    etat = charger_carte(os.path.join(dossier, scenario["carte"]))
    for ligne, colonne in scenario["foyers"]:
        etat["grille"][ligne, colonne] = FEU
    etat["vent"] = vent_depuis_angle(scenario["vent"]["angle"])
    etat["force_vent"] = scenario["vent"]["force"]
    parametres = {
        cle: scenario[cle]
        for cle in ("titre", "p_base", "budget", "max_tours", "graine")
    }
    return etat, parametres


