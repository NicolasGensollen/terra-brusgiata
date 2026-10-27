import copy
import os
import time
import csv
import math

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


def exporter_csv(lignes: list[dict], chemin: str) -> None:
    """Écrit les lignes de résultats dans un fichier CSV."""
    with open(chemin, "w", newline="", encoding="utf-8") as fichier:
        ecrivain = csv.DictWriter(fichier, fieldnames=list(lignes[0].keys()))
        ecrivain.writeheader()
        ecrivain.writerows(lignes)


def statistiques(valeurs: list[float]) -> dict:
    """Moyenne, écart-type, erreur-type et intervalle de confiance à 95 %."""
    valeurs = np.asarray(valeurs, dtype=float)
    n = len(valeurs)
    moyenne = float(np.mean(valeurs))
    ecart_type = float(np.std(valeurs, ddof=1)) if n > 1 else 0.0
    erreur = ecart_type / math.sqrt(n)
    return {
        "n": n,
        "moyenne": moyenne,
        "ecart_type": ecart_type,
        "erreur_type": erreur,
        "ic_bas": moyenne - 1.96 * erreur,
        "ic_haut": moyenne + 1.96 * erreur
    }


def resumer(lignes: list[dict]) -> None:
    """Affiche les statistiques du gain par scénario, puis sur l'ensemble."""
    noms = sorted({ligne["scenario"] for ligne in lignes})
    print(
        f"{'scénario':<14}{'n':>5}{'gain moyen':>12}{'écart-type':>12}"
        f"{'IC 95 %':>22}"
    )
    for nom in noms + ["TOTAL"]:
        gains = [l["gain"] for l in lignes if nom in ("TOTAL", l["scenario"])]
        s = statistiques(gains)
        ic = f"[{s['ic_bas']:.0f} ; {s['ic_haut']:.0f}]"
        print(
            f"{nom:<14}{s['n']:>5}{s['moyenne']:>12.0f}"
            f"{s['ecart_type']:>12.0f}{ic:>22}"
        )


def comparer(lignes_a: list[dict], lignes_b: list[dict]) -> tuple[dict, dict]:
    """Compare deux stratégies évaluées sur les mêmes scénarios et les mêmes graines. 

    Renvoie deux dictionnaires de statistiques sur la différence des gains : 
    la comparaison appariée, puis la comparaison non appariée.
    """
    gains_b = {
        (l["scenario"], l["graine"]): l["gain"] for l in lignes_b
    }
    differences = [
        l["gain"] - gains_b[(l["scenario"], l["graine"])] for l in lignes_a
    ]
    appariee = statistiques(differences)
    sa = statistiques([l["gain"] for l in lignes_a])
    sb = statistiques([l["gain"] for l in lignes_b])
    erreur = math.sqrt(sa["erreur_type"] ** 2 + sb["erreur_type"] ** 2)
    moyenne = sa["moyenne"] - sb["moyenne"]
    non_appariee = {
        "moyenne": moyenne,
        "erreur_type": erreur,
        "ic_bas": moyenne - 1.96 * erreur,
        "ic_haut": moyenne + 1.96 * erreur
    }
    return appariee, non_appariee


def chronometrer(strategie):
    """Renvoie (strategie_chronometree, durees) : une stratégie qui se comporte
    exactement comme strategie, mais qui ajoute à la liste durees la durée de
    chacun de ses appels."""
    durees = []

    def strategie_chronometree(etat, budget, tour):
        debut = time.perf_counter()
        actions = strategie(etat, budget, tour)
        durees.append(time.perf_counter() - debut)
        return actions

    return strategie_chronometree, durees


