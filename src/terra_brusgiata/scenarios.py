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


def jouer_scenario(chemin: str, strategie):
     """Joue un scénario avec une stratégie et avec la stratégie de référence."""
     etat, parametres = charger_scenario(chemin)
     reference = copy.deepcopy(etat)

     def partie(etat_depart, strat):
         rng = np.random.default_rng(parametres["graine"])
         return jouer(
             etat_depart,
             strat,
             rng,
             parametres["budget"],
             parametres["p_base"],
             parametres["max_tours"]
         )

     resultat = partie(etat, strategie)
     partie(reference, ne_rien_faire)
     resultat["score"] = score(etat)
     resultat["score_reference"] = score(reference)
     resultat["gain"] = resultat["score"] - resultat["score_reference"]
     resultat["etat_final"] = etat
     return resultat
