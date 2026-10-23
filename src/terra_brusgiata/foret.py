import math
import numpy as np

VIDE = 0
ARBRE = 1
FEU = 2
CENDRE = 3

# Types de végétation
EAU = 0
ROCHE = 1
ROUTE = 2
PRAIRIE = 3
MAQUIS = 4
FORET = 5
HABITATION = 6

NOMS_ETATS = {
    VIDE: "vide",
    ARBRE: "arbre", 
    FEU: "feu",
    CENDRE: "cendre"
}

NOMS_TYPES = {
    EAU: "eau",
    ROCHE: "roche",
    ROUTE: "route",
    PRAIRIE: "prairie",
    MAQUIS: "maquis",
    FORET: "forêt",
    HABITATION: "habitation"
}

INFLAMMABILITE = {
    EAU: 0.0,
    ROCHE: 0.0,
    ROUTE: 0.0,
    PRAIRIE: 0.7,
    MAQUIS: 1.3,
    FORET: 1.0,
    HABITATION: 0.4
}

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # haut, bas, gauche, droite
 
COEF_PENTE = 0.078   # par degré de pente

def creer_foret(hauteur : int, largeur : int, densite : int, rng):
    """Renvoie une grille où chaque case est ARBRE avec une probabilité densite, VIDE sinon."""
    tirages = rng.random((hauteur, largeur))
    return np.where(tirages < densite, ARBRE, VIDE).astype(np.int8)


def allumer(grille , ligne : int, colonne : int):
    """Met le feu à la case (ligne, colonne) si elle porte un arbre.

    Modifie la grille en place et ne renvoie rien.
    """
    if grille[ligne, colonne] == ARBRE:
        grille[ligne, colonne] = FEU


def allumer_bord_gauche(grille):
    """Enflamme les arbres de la première colonne. Modifie la grille en place."""
    colonne = grille[:, 0]
    colonne[colonne == ARBRE] = FEU


def compter(grille):
    """Renvoie le nombre de cases dans chaque état, sous forme de dictionnaire."""
    return {
        nom: int(np.count_nonzero(grille == etat))
        for etat, nom in NOMS_ETATS.items()
    }


def voisins(ligne: int, colonne: int, hauteur: int, largeur: int) -> list[tuple[int, int]]:
    """Renvoie la liste des coordonnées des voisines existantes (von Neumann)."""
    resultat = []
    for dl, dc in DIRECTIONS:
        l, c = ligne + dl, colonne + dc
        if 0 <= l < hauteur and 0 <= c < largeur:
            resultat.append((l, c))
    return resultat


def etape_deterministe(grille):
    """Renvoie la grille du tour suivant (propagation certaine)."""
    hauteur, largeur = grille.shape
    nouvelle = grille.copy()
    for ligne in range(hauteur):
        for colonne in range(largeur):
            if grille[ligne, colonne] == FEU:
                nouvelle[ligne, colonne] = CENDRE
            elif grille[ligne, colonne] == ARBRE:
                for ligne_voisin, colonne_voisin in voisins(ligne, colonne, hauteur, largeur):
                    if grille[ligne_voisin, colonne_voisin] == FEU:
                        nouvelle[ligne, colonne] = FEU
                        break
    return nouvelle


def simuler_deterministe(grille: np.ndarray) -> tuple[np.ndarray, int]:
    """Applique des étapes jusqu'à extinction.

    Renvoie (grille finale, nombre de tours).
    """
    tours = 0
    while np.any(grille == FEU):
        grille = etape_deterministe(grille)
        tours += 1
    return grille, tours


def creer_etat(grille: np.ndarray) -> dict:
    """Construit le dictionnaire d'état de la simulation.
 
    L'humidité et le vent ont des valeurs neutres : ils n'ont aucun effet
    sur la propagation tant que les parties 5 et 6 ne les utilisent pas.
    """
    return {
        "grille": grille,
        "humidite": np.zeros(grille.shape),           # sol parfaitement sec partout
        "vent": (0.0, 0.0),                           # pas de direction de vent
        "force_vent": 0.0,                            # vent nul
        "vegetation": np.full(grille.shape, FORET),
        "altitude": np.zeros(grille.shape),           # terrain plat
        "taille_case": 1.0,
        "tour": 0,                                    # la simulation n'a pas commencé
    }


def etape(etat: dict, rng, p_base: float = 0.6) -> None:
    """Fait avancer la simulation d'un tour.

    Modifie etat en place : remplace etat["grille"] et incrémente etat["tour"].
    """
    grille = etat["grille"]
    hauteur, largeur = grille.shape
    vy, vx = etat["vent"]
    f = etat["force_vent"]
    nouvelle = grille.copy()
    for l, c in np.argwhere(grille == FEU):
        nouvelle[l, c] = CENDRE
        for vl, vc in voisins(l, c, hauteur, largeur):
            # grille[...] == ARBRE : la cible était un arbre au début du tour
            # nouvelle[...] == ARBRE : pas déjà enflammée pendant ce tour
            if grille[vl, vc] == ARBRE and nouvelle[vl, vc] == ARBRE:
                dy, dx = vl - l, vc - c
                facteur_vent = 1 + f * (dy * vy + dx * vx)
                p = p_base * (1 - etat["humidite"][vl, vc])
                p = p * INFLAMMABILITE[etat["vegetation"][vl, vc]] 
                p = min(1.0, max(0.0, p * facteur_vent))
                if rng.random() < p:
                    nouvelle[vl, vc] = FEU
    etat["grille"] = nouvelle
    etat["tour"] += 1


def simuler(etat: dict, rng, p_base: float = 0.6, max_tours: int = 1000) -> list[np.ndarray]:
    """Simule jusqu'à extinction (ou max_tours). Renvoie la liste des grilles."""
    historique = [etat["grille"].copy()]
    while np.any(etat["grille"] == FEU) and etat["tour"] < max_tours:
        etape(etat, rng, p_base)
        historique.append(etat["grille"].copy())
    return historique


def humidite_uniforme(forme: tuple[int, int], valeur: float) -> np.ndarray:
    """Même humidité partout."""
    return np.full(forme, float(valeur))


def humidite_aleatoire(forme: tuple[int, int], maxi: float, rng) -> np.ndarray:
    """Humidité tirée uniformément entre 0 et maxi pour chaque case."""
    return rng.random(forme) * maxi


HUMIDITE_RIVE = 0.8   # humidité maximale, au bord de l'eau


def humidite_riviere(forme: tuple[int, int], colonne: int, largeur_zone: int) -> np.ndarray:
    """Bande humide verticale centrée sur colonne : humidité HUMIDITE_RIVE au
    bord de l'eau, décroissant linéairement jusqu'à 0 à une distance
    largeur_zone.

    forme : forme de la grille (hauteur, largeur)
    colonne : position de la rivière
    largeur_zone : La distance, en cases, à laquelle l'humidité tombe à zéro.
    """
    hauteur, largeur = forme
    distances = np.abs(np.arange(largeur) - colonne)
    if largeur_zone > 0:
        profil = HUMIDITE_RIVE * np.clip(1 - distances / largeur_zone, 0, 1)
    else:
        profil = np.zeros(largeur)
    return np.tile(profil, (hauteur, 1))


def vent_depuis_angle(angle_degres):
    """Vecteur unitaire (dy, dx) du vent qui souffle VERS la direction donnée.

    0° = vers la droite (est), 90° = vers le haut (nord). L'axe des lignes
    étant orienté vers le bas, « vers le haut » donne un dy négatif.
    """
    a = math.radians(angle_degres)
    return (-math.sin(a), math.cos(a))


def simuler_vent_variable(etat: dict, rng, vent_au_tour, p_base: float = 0.6, max_tours: int = 1000):
    """Comme simuler, mais le vent est recalculé à chaque tour par vent_au_tour(tour)."""
    historique = [etat["grille"].copy()]
    while np.any(etat["grille"] == FEU) and etat["tour"] < max_tours:
        etat["vent"] = vent_au_tour(etat["tour"])
        etape(etat, rng, p_base)
        historique.append(etat["grille"].copy())
    return historique


def facteur_pente(dz: float, taille_case: int) -> float:
    """Facteur multiplicatif dû à la pente, pour une montée de dz mètres
    sur une distance horizontale taille_case (descente si dz < 0)."""
    angle = math.degrees(math.atan(dz / taille_case))
    return math.exp(COEF_PENTE * angle)

