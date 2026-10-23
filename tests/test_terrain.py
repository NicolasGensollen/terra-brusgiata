import math
 
import numpy as np
import pytest
 
from terra_brusgiata.cartes import charger_carte, lire_vegetation, sauvegarder_carte
from terra_brusgiata.editeur import peindre
from terra_brusgiata.foret import (ARBRE, CENDRE, EAU, FEU, FORET, HABITATION, MAQUIS, PRAIRIE,
                   ROCHE, ROUTE, VIDE, allumer, facteur_pente, simuler)
from terra_brusgiata.terrain import creer_etat_terrain, grille_depuis_vegetation, plan_incline
 
 
def etat_uniforme(type_terrain, taille=30, altitude=None, taille_case=100.0):
    vegetation = np.full((taille, taille), type_terrain, dtype=np.int8)
    if altitude is None:
        altitude = np.zeros(vegetation.shape)
    return creer_etat_terrain(vegetation, altitude, taille_case)
 
 
def test_grille_depuis_vegetation():
    vegetation = np.array([[EAU, ROCHE, ROUTE, PRAIRIE, MAQUIS, FORET, HABITATION]])
    attendu = [[VIDE, VIDE, VIDE, ARBRE, ARBRE, ARBRE, ARBRE]]
    assert grille_depuis_vegetation(vegetation).tolist() == attendu
 
 
@pytest.mark.parametrize("type_terrain", [EAU, ROCHE, ROUTE])
def test_types_incombustibles(type_terrain):
    etat = etat_uniforme(type_terrain)
    etat["grille"][15, 15] = FEU          # on force un feu au milieu
    fin = simuler(etat, np.random.default_rng(0), p_base=1.0)[-1]
    assert np.count_nonzero(fin == CENDRE) == 1


def test_facteur_pente():
    assert facteur_pente(0, 100) == 1
    assert facteur_pente(30, 100) > 1 > facteur_pente(-30, 100)
    assert math.isclose(facteur_pente(30, 100) * facteur_pente(-30, 100), 1)


def test_feu_monte_plus_vite():
    etat = etat_uniforme(FORET, 41, plan_incline((41, 41), 10, 100.0))
    allumer(etat["grille"], 20, 20)
    fin = simuler(etat, np.random.default_rng(0), p_base=0.6, max_tours=15)[-1]
    lignes_brulees = np.argwhere(fin != ARBRE)[:, 0]
    montee = 20 - lignes_brulees.min()        # le terrain monte vers le haut
    descente = lignes_brulees.max() - 20
    assert montee > descente


def test_aller_retour(tmp_path):
    rng = np.random.default_rng(0)
    vegetation = rng.integers(0, 7, (12, 17)).astype(np.int8)
    altitude = np.round(rng.random((12, 17)) * 500, 1)
    chemin = str(tmp_path / "carte.txt")
    sauvegarder_carte(chemin, creer_etat_terrain(vegetation, altitude, 25.0), "essai")
    relue = charger_carte(chemin)
    assert np.array_equal(relue["vegetation"], vegetation)
    assert np.allclose(relue["altitude"], altitude)
    assert relue["taille_case"] == 25.0


@pytest.mark.parametrize("contenu", [
    "# taille_case = 10\nTTx\n",            # symbole inconnu
    "# taille_case = 10\nTTT\nTT\n",        # ligne trop courte
    "TTT\nTTT\n",                           # taille_case absente
])
def test_fichiers_invalides(tmp_path, contenu):
    chemin = tmp_path / "carte.txt"
    chemin.write_text(contenu, encoding="utf-8")
    with pytest.raises(ValueError):
        lire_vegetation(chemin)


def test_carte_sans_relief(tmp_path):
    chemin = tmp_path / "plate.txt"
    chemin.write_text("# taille_case = 10\nTTm\n~~.\n", encoding="utf-8")
    etat = charger_carte(str(chemin))
    assert np.all(etat["altitude"] == 0) and etat["altitude"].shape == (2, 3)


def test_peindre_aux_bords():
    vegetation = np.full((5, 5), FORET, dtype=np.int8)
    peindre(vegetation, 0, 0, EAU, 2)
    peindre(vegetation, 4, 4, ROCHE, 3)
    assert np.count_nonzero(vegetation == EAU) == 4      # carré 2 × 2 dans le coin
    assert np.count_nonzero(vegetation == ROCHE) == 9    # carré 3 × 3 dans le coin

