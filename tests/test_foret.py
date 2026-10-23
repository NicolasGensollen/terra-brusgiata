from collections import deque
import numpy as np

from terra_brusgiata.foret import (
    ARBRE,
    CENDRE,
    FEU,
    VIDE,
    allumer,
    allumer_bord_gauche,
    compter,
    creer_etat,
    creer_foret,
    humidite_uniforme,
    simuler,
    voisins
)


def foret_test(taille=40, densite=0.7, graine=1):
    return creer_foret(taille, taille, densite, np.random.default_rng(graine))


def composante_connexe(grille, depart):
    """Cases d'arbre ou de feu reliées à depart (parcours en largeur)."""
    h, l = grille.shape
    vus, file = {depart}, deque([depart])
    while file:
        case = file.popleft()
        for v in voisins(*case, h, l):
            if v not in vus and grille[v] in (ARBRE, FEU):
                vus.add(v)
                file.append(v)
    return vus


def test_feu_isole_s_eteint():
    grille = np.full((5, 5), VIDE)
    grille[2, 2] = FEU
    historique = simuler(creer_etat(grille), np.random.default_rng(0))
    assert compter(historique[-1])["feu"] == 0
    assert compter(historique[-1])["cendre"] == 1


def test_coin_deux_voisines():
    assert sorted(voisins(0, 0, 10, 10)) == [(0, 1), (1, 0)]
    assert len(voisins(9, 9, 10, 10)) == 2
    assert len(voisins(0, 5, 10, 10)) == 3
    assert len(voisins(5, 5, 10, 10)) == 4


def test_cendre_reste_cendre():
    grille = foret_test()
    allumer_bord_gauche(grille)
    historique = simuler(creer_etat(grille), np.random.default_rng(3))
    for avant, apres in zip(historique, historique[1:]):
        assert np.all(apres[avant == CENDRE] == CENDRE)


def test_p1_brule_exactement_la_composante():
    grille = foret_test()
    grille[20, 20] = ARBRE
    allumer(grille, 20, 20)
    attendu = composante_connexe(grille, (20, 20))
    fin = simuler(creer_etat(grille), np.random.default_rng(0), p_base=1.0)[-1]
    brulees = {tuple(c) for c in np.argwhere(fin == CENDRE)}
    assert brulees == attendu


def test_p0_rien_ne_brule():
    grille = foret_test()
    allumer_bord_gauche(grille)
    fin = simuler(creer_etat(grille), np.random.default_rng(0), p_base=0.0)[-1]
    assert compter(fin)["arbre"] == compter(grille)["arbre"]


def test_humidite_totale_rien_ne_brule():
    grille = foret_test()
    allumer_bord_gauche(grille)
    etat = creer_etat(grille)
    etat["humidite"] = humidite_uniforme(grille.shape, 1.0)
    fin = simuler(etat, np.random.default_rng(0), p_base=1.0)[-1]
    assert compter(fin)["arbre"] == compter(grille)["arbre"]

def test_vent_fort_pas_de_propagation_contre_le_vent():
    grille = np.full((30, 30), ARBRE)
    allumer(grille, 15, 15)
    etat = creer_etat(grille)
    etat["vent"] = (0.0, 1.0)                # vent soufflant vers la droite
    etat["force_vent"] = 1.0
    fin = simuler(etat, np.random.default_rng(0), p_base=1.0)[-1]
    assert np.all(fin[:, :15] == ARBRE)     # rien à gauche du foyer
    assert np.any(fin[:, 16:] == CENDRE)    # mais le feu est parti à droite


def test_meme_graine_meme_historique():
    resultats = []
    for _ in range(2):
        grille = foret_test()
        allumer_bord_gauche(grille)
        resultats.append(simuler(creer_etat(grille), np.random.default_rng(42)))
    assert len(resultats[0]) == len(resultats[1])
    assert all(np.array_equal(a, b) for a, b in zip(*resultats))


def test_nombre_de_cases_constant():
    grille = foret_test()
    allumer_bord_gauche(grille)
    historique = simuler(creer_etat(grille), np.random.default_rng(5))
    assert all(sum(compter(g).values()) == grille.size for g in historique)


def test_grille_une_case():
    grille = np.array([[FEU]])
    historique = simuler(creer_etat(grille), np.random.default_rng(0))
    assert historique[-1][0, 0] == CENDRE and len(historique) == 2


def test_foret_sans_arbre():
    grille = creer_foret(10, 10, 0.0, np.random.default_rng(0))
    allumer_bord_gauche(grille)
    historique = simuler(creer_etat(grille), np.random.default_rng(0))
    assert len(historique) == 1 and compter(grille)["vide"] == 100


def test_densite_extremes():
    rng = np.random.default_rng(0)
    assert np.all(creer_foret(10, 10, 1.0, rng) == ARBRE)
    assert np.all(creer_foret(10, 10, 0.0, rng) == VIDE)
