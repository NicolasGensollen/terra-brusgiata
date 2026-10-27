import numpy as np
 
from .foret import ARBRE, FEU, HABITATION, PAREFEU
from .jeu import DELAI_INTERVENTION, MAX_ACTIONS_PAR_TOUR, REGLES, zone_autour_du_feu, Strategie


def proteger_maisons(etat: dict, budget: int, tour: int) -> Strategie:
    """Protège les habitations intactes les plus menacées par le feu."""
    grille, vegetation = etat["grille"], etat["vegetation"]
    a_proteger = (
        (vegetation == HABITATION) & 
        (grille == ARBRE) & 
        (etat["protection"] == 0) & 
        zone_autour_du_feu(grille, 4)
    )
    n = min(MAX_ACTIONS_PAR_TOUR, budget // REGLES["protection"]["cout"])
    return [
        ("protection", int(l), int(c)) 
        for l, c in np.argwhere(a_proteger)[:n]
    ]


def arroser_devant(etat: dict, budget: int, tour: int) -> Strategie:
    """Arrose la zone située juste devant le point du feu le plus avancé
    dans le sens du vent."""
    feux = np.argwhere(etat["grille"] == FEU)
    vy, vx = etat["vent"]
    ligne, colonne = feux[np.argmax(feux @ np.array([vy, vx]))]
    return [("eau", int(round(ligne + 3 * vy)), int(round(colonne + 3 * vx)))]


def parefeux_devant(etat: dict, budget: int, tour: int) -> Strategie:
    """Creuse des pare-feux à la distance de sécurité, en commençant par les
    cases les plus en aval du vent."""
    grille = etat["grille"]
    anneau = zone_autour_du_feu(grille, 3) & ~zone_autour_du_feu(grille, 2)
    anneau &= (grille == ARBRE) & (etat["vegetation"] != HABITATION)
    cases = np.argwhere(anneau)
    vy, vx = etat["vent"]
    cases = cases[np.argsort(-(cases @ np.array([vy, vx])))]
    n = min(MAX_ACTIONS_PAR_TOUR, budget)
    return [("parefeu", int(l), int(c)) for l, c in cases[:n]]


def contre_feu_devant(etat: dict, budget: int, tour: int) -> Strategie:
    """Allume un contre-feu à 3 cases devant la case en feu la plus avancée."""
    feux = np.argwhere(etat["grille"] == FEU)
    vy, vx = etat["vent"]
    ligne, colonne = feux[np.argmax(feux @ np.array([vy, vx]))]
    return [("contre_feu", int(round(ligne + 3 * vy)), int(round(colonne + 3 * vx)))]


def contre_feu_adosse(etat: dict, budget: int, tour: int) -> Strategie:
    """Creuse des pare-feux devant le front, puis allume des contre-feux
    entre le front et ces pare-feux."""
    grille, vegetation = etat["grille"], etat["vegetation"]
    vy, vx = etat["vent"]
    dl, dc = int(round(vy)), int(round(vx))     # une case vers l'aval
    pare = np.pad(vegetation == PAREFEU, 1)
    pare_en_aval = pare[1 + dl:pare.shape[0] - 1 + dl, 1 + dc:pare.shape[1] - 1 + dc]
    cibles = np.argwhere(pare_en_aval & (grille == ARBRE) & (vegetation != HABITATION)
                         & zone_autour_du_feu(grille, 3))
    actions = [("contre_feu", int(l), int(c)) for l, c in cibles[:2]]
    reste = MAX_ACTIONS_PAR_TOUR - len(actions)
    actions += parefeux_devant(etat, budget - len(actions), tour)[:reste]
    return actions


def fabrique_parefeux(distance: int) -> Strategie:
    """Fabrique une stratégie qui creuse des pare-feux à exactement distance
    cases du feu, en commençant par les cases les plus en aval du vent."""

    def strategie(etat, budget, tour):
        grille = etat["grille"]
        anneau = (
            zone_autour_du_feu(grille, distance) &
            ~zone_autour_du_feu(grille, distance - 1)
        )
        anneau &= (grille == ARBRE) & (etat["vegetation"] != HABITATION)
        cases = np.argwhere(anneau)
        vy, vx = etat["vent"]
        cases = cases[np.argsort(-(cases @ np.array([vy, vx])))]
        n = min(MAX_ACTIONS_PAR_TOUR, budget)
        return [("parefeu", int(l), int(c)) for l, c in cases[:n]]

    return strategie


def fabrique_arrosage(avance: int) -> Strategie:
    """Fabrique une stratégie qui arrose à avance cases devant la case du feu
    la plus avancée dans le sens du vent."""

    def strategie(etat, budget, tour):
        feux = np.argwhere(etat["grille"] == FEU)
        vy, vx = etat["vent"]
        ligne, colonne = feux[np.argmax(feux @ np.array([vy, vx]))]
        return [
            ("eau", int(round(ligne + avance * vy)), int(round(colonne + avance * vx)))
        ]

    return strategie


