import numpy as np
 
from foret import ARBRE, FEU, HABITATION, PAREFEU, VIDE
 

REGLES = {
    "parefeu": {"cout": 1},
    "eau": {"cout": 6, "humidite": 0.9},          # zone de 3 × 3 cases
    "contre_feu": {"cout": 1},
    "protection": {"cout": 3, "duree": 15},
}
MAX_ACTIONS_PAR_TOUR = 5
DELAI_INTERVENTION = 5       # premier tour où l'on peut agir
DISTANCE_SECURITE = 3        # distance minimale au feu pour creuser un pare-feu
EVAPORATION = 0.1            # part de l'humidité ajoutée évaporée à chaque tour
POIDS_HABITATION = 20


def feu_a_proximite(grille: np.ndarray, ligne: int, colonne: int, rayon: int) -> bool:
    """Vrai s'il y a une case en feu à moins de rayon cases, diagonales comprises."""
    fenetre = grille[max(ligne - rayon + 1, 0):ligne + rayon,
                     max(colonne - rayon + 1, 0):colonne + rayon]
    return bool(np.any(fenetre == FEU))


def valider_action(etat: dict, action: tuple[str, int, int], budget: int) -> str | None:
    """Renvoie None si l'action est permise, sinon un message expliquant la raison du refus."""
    if not (isinstance(action, tuple) and len(action) == 3):
        return f"action mal formée : {action!r}"
    nom, ligne, colonne = action
    if nom not in REGLES:
        return f"action inconnue : {nom!r}"
    grille, vegetation = etat["grille"], etat["vegetation"]
    hauteur, largeur = grille.shape
    if not (0 <= ligne < hauteur and 0 <= colonne < largeur):
        return f"case ({ligne}, {colonne}) hors de la carte"
    if etat["tour"] < DELAI_INTERVENTION:
        return f"aucune intervention avant le tour {DELAI_INTERVENTION}"
    cout = REGLES[nom]["cout"]
    if cout > budget:
        return f"budget insuffisant ({budget} restant, {cout} nécessaires)"
    if nom in ("parefeu", "contre_feu"):
        if grille[ligne, colonne] != ARBRE:
            return f"case ({ligne}, {colonne}) non combustible ou déjà touchée"
        if vegetation[ligne, colonne] == HABITATION:
            return f"case ({ligne}, {colonne}) : action interdite sur une habitation"
    if nom == "parefeu":
        if feu_a_proximite(grille, ligne, colonne, DISTANCE_SECURITE):
            return f"case ({ligne}, {colonne}) trop proche du feu"
    if nom == "protection":
        maison_intacte = (
            vegetation[ligne, colonne] == HABITATION
            and grille[ligne, colonne] == ARBRE
        )
        if not maison_intacte:
            return f"case ({ligne}, {colonne}) : aucune habitation intacte"
    return None


def appliquer_action(etat: dict, action: tuple[str, int, int]) -> None:
    """Applique une action supposée valide. Modifie etat en place."""
    nom, ligne, colonne = action
    if nom == "parefeu":
        etat["vegetation"][ligne, colonne] = PAREFEU
        etat["grille"][ligne, colonne] = VIDE
    elif nom == "eau":
        l0, c0 = max(ligne - 1, 0), max(colonne - 1, 0)
        zone = etat["humidite"][l0:ligne + 2, c0:colonne + 2]
        zone[:] = np.maximum(zone, REGLES["eau"]["humidite"])
    elif nom == "contre_feu":
        etat["grille"][ligne, colonne] = FEU
    elif nom == "protection":
        etat["protection"][ligne, colonne] = REGLES["protection"]["duree"]


