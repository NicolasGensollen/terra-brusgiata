import json
 
import numpy as np
import pytest
 
from terra_brusgiata.foret import (
    ARBRE,
    CENDRE,
    FEU,
    FORET,
    HABITATION,
    MAQUIS,
    PAREFEU,
    VIDE,
    simuler
)
from terra_brusgiata.jeu import (
    DELAI_INTERVENTION,
    DISTANCE_SECURITE,
    EVAPORATION,
    MAX_ACTIONS_PAR_TOUR,
    POIDS_HABITATION,
    REGLES,
    appliquer_action,
    jouer,
    ne_rien_faire,
    score,
    valider_action
)
from terra_brusgiata.scenarios import charger_scenario, jouer_scenario
from terra_brusgiata.terrain import creer_etat_terrain
 
 
def etat_test(taille=20, type_terrain=FORET):
    vegetation = np.full((taille, taille), type_terrain, dtype=np.int8)
    etat = creer_etat_terrain(vegetation, np.zeros(vegetation.shape), 100.0)
    etat["tour"] = DELAI_INTERVENTION          # les interventions sont permises
    return etat
 
 
@pytest.mark.parametrize("action", [
    ("parefeu", 2),                  # mal formée
    ("bulldozer", 2, 2),             # inconnue
    ("parefeu", 20, 2),              # hors de la carte
    ("parefeu", -1, 2),              # hors de la carte
])
def test_actions_invalides(action):
    assert valider_action(etat_test(), action, 100) is not None
 
 
def test_action_valide():
    assert valider_action(etat_test(), ("parefeu", 5, 5), 100) is None


def test_delai_intervention():
    etat = etat_test()
    etat["tour"] = DELAI_INTERVENTION - 1
    assert valider_action(etat, ("parefeu", 5, 5), 100) is not None


def test_budget_insuffisant():
    cout = REGLES["eau"]["cout"]
    assert valider_action(etat_test(), ("eau", 5, 5), cout - 1) is not None
    assert valider_action(etat_test(), ("eau", 5, 5), cout) is None


def test_distance_de_securite():
    etat = etat_test()
    etat["grille"][10, 10] = FEU
    trop_pres = ("parefeu", 10, 10 + DISTANCE_SECURITE - 1)
    assez_loin = ("parefeu", 10, 10 + DISTANCE_SECURITE)
    assert valider_action(etat, trop_pres, 100) is not None
    assert valider_action(etat, assez_loin, 100) is None


def test_pas_de_parefeu_sur_une_maison():
    etat = etat_test(type_terrain=HABITATION)
    assert valider_action(etat, ("parefeu", 5, 5), 100) is not None
    assert valider_action(etat, ("protection", 5, 5), 100) is None
    assert valider_action(etat_test(), ("protection", 5, 5), 100) is not None


def test_effet_parefeu():
    etat = etat_test()
    appliquer_action(etat, ("parefeu", 5, 5))
    assert etat["vegetation"][5, 5] == PAREFEU and etat["grille"][5, 5] == VIDE


def test_effet_eau_au_bord():
    etat = etat_test()
    appliquer_action(etat, ("eau", 0, 0))
    mouille = etat["humidite"] > 0
    # la zone de 3 × 3 cases est coupée par le bord
    assert np.count_nonzero(mouille) == 4 and mouille[1, 1]


def test_effet_contre_feu():
    etat = etat_test()
    appliquer_action(etat, ("contre_feu", 5, 5))
    assert etat["grille"][5, 5] == FEU


def test_protection_puis_expiration():
    vegetation = np.full((1, 30), HABITATION, dtype=np.int8)
    etat = creer_etat_terrain(vegetation, np.zeros(vegetation.shape), 100.0)
    etat["grille"][0, 0] = FEU
    appliquer_action(etat, ("protection", 0, 1))
    duree = REGLES["protection"]["duree"]
    simuler(etat, np.random.default_rng(0), p_base=1.0, max_tours=duree)
    assert etat["grille"][0, 1] == ARBRE


def test_jouer_decompte_le_budget_et_limite_les_actions():
    etat = etat_test(30)
    etat["tour"] = 0
    etat["grille"][15, 15] = FEU

    def creuse_beaucoup(etat, budget, tour):
        intactes = [c for c in range(30) if etat["grille"][0, c] == ARBRE]
        return [("parefeu", 0, c) for c in intactes[:10]]

    rng = np.random.default_rng(0)
    resultat = jouer(etat, creuse_beaucoup, rng, budget=7, p_base=0.6)
    tours = [t for t, a, m in resultat["journal"] if m == "ok"]
    assert len(tours) == 7 and resultat["budget_restant"] == 0
    assert all(tours.count(t) <= MAX_ACTIONS_PAR_TOUR for t in tours)
 
 
def test_strategie_qui_plante():
    etat = etat_test()
    etat["grille"][10, 10] = FEU
 
    def plante(etat, budget, tour):
        raise RuntimeError("boum")
 
    resultat = jouer(etat, plante, np.random.default_rng(0), budget=10)
    assert any("boum" in m for _, _, m in resultat["journal"])
 
 
def test_strategie_ne_peut_pas_tricher():
    etat = etat_test()
    etat["grille"][10, 10] = FEU
 
    def tricheuse(etat, budget, tour):
        etat["grille"][:] = CENDRE              # éteint tout... dans sa copie
        return []
 
    reference = etat_test()
    reference["grille"][10, 10] = FEU
    attendu = jouer(reference, ne_rien_faire, np.random.default_rng(0), budget=0)
    obtenu = jouer(etat, tricheuse, np.random.default_rng(0), budget=0)
    assert np.array_equal(attendu["historique"][-1], obtenu["historique"][-1])
 
 
def test_evaporation():
    etat = etat_test(40)
    etat["tour"] = 0
    etat["grille"][39, 39] = FEU          # un feu loin de la zone arrosée
 
    def arrose(etat, budget, tour):
        return [("eau", 1, 1)] if tour == DELAI_INTERVENTION else []
 
    resultat = jouer(etat, arrose, np.random.default_rng(0), budget=100, p_base=1.0)
    humidites = [h[1, 1] for h in resultat["humidites"]]
    apres = humidites[DELAI_INTERVENTION + 1]
    assert apres == pytest.approx(REGLES["eau"]["humidite"] * (1 - EVAPORATION))
 
 
def test_score():
    vegetation = np.array([[FORET, MAQUIS, HABITATION, HABITATION]])
    etat = creer_etat_terrain(vegetation, np.zeros(vegetation.shape), 100.0)
    etat["grille"][0, 1] = CENDRE
    etat["grille"][0, 3] = CENDRE
    assert score(etat) == 1 + POIDS_HABITATION
 
 
def test_scenario(tmp_path):
    (tmp_path / "petite.txt").write_text("# taille_case = 50\nTTTTT\nTTTTT\nTTHTT\n",
                                         encoding="utf-8")
    scenario = {"titre": "essai", "carte": "petite.txt", "foyers": [[0, 0]],
                "vent": {"angle": 0, "force": 0.5}, "p_base": 1.0, "budget": 10,
                "max_tours": 100, "graine": 3}
    chemin = tmp_path / "essai.json"
    chemin.write_text(json.dumps(scenario), encoding="utf-8")
    etat, parametres = charger_scenario(str(chemin))
    assert etat["grille"][0, 0] == FEU and parametres["budget"] == 10
    resultat = jouer_scenario(str(chemin), ne_rien_faire)
    assert resultat["gain"] == 0

