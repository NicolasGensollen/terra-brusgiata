import copy
import os
import time
 
import numpy as np
 
from .jeu import jouer, ne_rien_faire, score, Strategie
from .scenarios import charger_scenario
 
 
def charger_scenarios(chemins: list[str]) -> list[dict]:
    """Renvoie un dictionnaire {nom du scénario : (état de départ,
    paramètres)}."""
    scenarios = {}
    for chemin in chemins:
        nom = os.path.splitext(os.path.basename(chemin))[0]
        scenarios[nom] = charger_scenario(chemin)
    return scenarios


def jouer_partie(etat_depart: dict, parametres: dict, strategie: Strategie, graine: int) -> dict:
    """Joue une partie sur une copie de l'état de départ. 

    Renvoie un dictionnaire avec le score final, le nombre de tours et la durée de la
    partie en secondes."""
    etat = copy.deepcopy(etat_depart)
    rng = np.random.default_rng(graine)
    debut = time.perf_counter()
    resultat = jouer(
        etat,
        strategie,
        rng,
        parametres["budget"],
        parametres["p_base"],
        parametres["max_tours"]
    )
    return {
        "score": score(etat),
        "tours": len(resultat["historique"]) - 1,
        "duree": time.perf_counter() - debut
    }


def evaluer(strategie: Strategie, scenarios: dict, graines: list[int], references: dict):
    """Joue la stratégie sur chaque scénario et chaque graine. 

    Renvoie une liste de dictionnaires, un par partie, avec les clés :
        - "scenario"
        - "graine"
        - "score"
        - "reference"
        - "gain"
        - "tours"
        - "duree".
    """
    lignes = []
    for nom, (etat_depart, parametres) in scenarios.items():
        for graine in graines:
            if (nom, graine) not in references:
                partie = jouer_partie(etat_depart, parametres, ne_rien_faire, graine)
                references[(nom, graine)] = partie["score"]
            partie = jouer_partie(etat_depart, parametres, strategie, graine)
            reference = references[(nom, graine)]
            lignes.append(
                {
                    "scenario": nom,
                    "graine": graine,
                    "score": partie["score"], 
                    "reference": reference,
                    "gain": partie["score"] - reference,
                    "tours": partie["tours"], 
                    "duree": partie["duree"]
                }
            )
    return lignes


