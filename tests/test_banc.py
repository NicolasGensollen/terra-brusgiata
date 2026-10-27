import csv
import json
import math
 
import numpy as np
import pytest
 
from terra_brusgiata.banc import (
    charger_scenarios,
    chronometrer,
    comparer,
    evaluer,
    exporter_csv,
    jouer_partie,
    statistiques
)
from terra_brusgiata.jeu import ne_rien_faire
from terra_brusgiata.strategies import fabrique_mixte, fabrique_parefeux, parefeux_devant
 
 
@pytest.fixture
def scenarios(tmp_path):
    """Deux petits scénarios sur une carte de 12 × 15 cases."""
    carte = "\n".join(["mmmmmTTTTTmmmmm"] * 6 + ["mmmHHHmmmTTTmmm"] * 6)
    (tmp_path / "petite.txt").write_text("# taille_case = 50\n" + carte + "\n",
                                         encoding="utf-8")
    chemins = []
    for nom, foyer in (("ouest", [6, 1]), ("est", [6, 13])):
        scenario = {"titre": nom, "carte": "petite.txt", "foyers": [foyer],
                    "vent": {"angle": 0, "force": 0.3}, "p_base": 0.8,
                    "budget": 20, "max_tours": 200, "graine": 0}
        chemin = tmp_path / f"{nom}.json"
        chemin.write_text(json.dumps(scenario), encoding="utf-8")
        chemins.append(str(chemin))
    return charger_scenarios(chemins)
 
 
def test_statistiques():
    s = statistiques([2, 4, 6, 8])
    assert s["n"] == 4 and s["moyenne"] == 5
    assert s["ecart_type"] == pytest.approx(math.sqrt(20 / 3))
    assert s["erreur_type"] == pytest.approx(s["ecart_type"] / 2)
    assert s["ic_bas"] < s["moyenne"] < s["ic_haut"]
 
 
def test_une_ligne_par_partie(scenarios):
    lignes = evaluer(parefeux_devant, scenarios, range(3), {})
    assert len(lignes) == 2 * 3
    assert {(l["scenario"], l["graine"]) for l in lignes} == {
        (nom, g) for nom in ("ouest", "est") for g in range(3)}
 
 
def test_ne_rien_faire_gain_nul(scenarios):
    lignes = evaluer(ne_rien_faire, scenarios, range(3), {})
    assert all(l["gain"] == 0 for l in lignes)


def test_mise_en_cache(scenarios):
    references = {}
    evaluer(parefeux_devant, scenarios, range(3), references)
    assert len(references) == 2 * 3
    fictives = {cle: 0 for cle in references}      # références fictives
    lignes = evaluer(parefeux_devant, scenarios, range(3), fictives)
    assert all(l["gain"] == l["score"] for l in lignes)


def test_comparer_avec_soi_meme(scenarios):
    lignes = evaluer(parefeux_devant, scenarios, range(3), {})
    appariee, non_appariee = comparer(lignes, lignes)
    assert appariee["moyenne"] == 0 and appariee["ecart_type"] == 0
    assert non_appariee["moyenne"] == 0


def test_chronometrer(scenarios):
    etat, parametres = scenarios["ouest"]
    strategie, durees = chronometrer(parefeux_devant)
    resultat = jouer_partie(etat, parametres, strategie, 0)
    attendu = jouer_partie(etat, parametres, parefeux_devant, 0)
    assert resultat["score"] == attendu["score"]
    assert len(durees) == resultat["tours"] and all(d >= 0 for d in durees)


def test_fabriques_independantes(scenarios):
    etat, parametres = scenarios["ouest"]
    proche, loin = fabrique_parefeux(3), fabrique_parefeux(6)
    copie = {cle: (v.copy() if isinstance(v, np.ndarray) else v)
             for cle, v in etat.items()}
    copie["tour"] = 5
    actions_proche = proche(copie, 20, 5)
    actions_loin = loin(copie, 20, 5)
    assert actions_proche != actions_loin
    assert proche(copie, 20, 5) == actions_proche   # loin n'a pas modifié proche


def test_mixte_reinitialisee_entre_parties(scenarios):
    etat, parametres = scenarios["ouest"]
    strategie = fabrique_mixte(12)
    premier = jouer_partie(etat, parametres, strategie, 0)
    second = jouer_partie(etat, parametres, strategie, 0)
    assert premier["score"] == second["score"]


def test_export_csv(scenarios, tmp_path):
    lignes = evaluer(parefeux_devant, scenarios, range(2), {})
    chemin = tmp_path / "resultats.csv"
    exporter_csv(lignes, chemin)
    with open(chemin, encoding="utf-8") as fichier:
        relues = list(csv.DictReader(fichier))
    assert len(relues) == len(lignes)
    assert [int(r["gain"]) for r in relues] == [l["gain"] for l in lignes]

