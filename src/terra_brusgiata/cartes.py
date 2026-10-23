import os
 
import numpy as np
 
from .foret import EAU, FORET, HABITATION, MAQUIS, PRAIRIE, ROCHE, ROUTE
from .terrain import creer_etat_terrain
 
SYMBOLES = {
    "~": EAU,
    "^": ROCHE,
    "=": ROUTE,
    ".": PRAIRIE,
    "m": MAQUIS,
    "T": FORET,
    "H": HABITATION
}

TYPES_VERS_SYMBOLES = {t: s for s, t in SYMBOLES.items()}


def lire_vegetation(chemin):
    """Lit un fichier de carte. Renvoie (vegetation, taille_case)."""
    taille_case = None
    lignes = []
    with open(chemin, encoding="utf-8") as fichier:
        for numero, ligne in enumerate(fichier, start=1):
            ligne = ligne.rstrip("\n")
            if ligne.startswith("#"):
                commentaire = ligne[1:].strip()
                if commentaire.startswith("taille_case"):
                    taille_case = float(commentaire.split("=")[1])
                continue
            if ligne.strip() == "":
                continue
            types = []
            for colonne, symbole in enumerate(ligne, start=1):
                if symbole not in SYMBOLES:
                    raise ValueError(
                        f"{chemin}, ligne {numero}, colonne {colonne} : "
                        f"symbole inconnu {symbole!r}"
                    )
                types.append(SYMBOLES[symbole])
            if lignes and len(types) != len(lignes[0]):
                raise ValueError(
                    f"{chemin}, ligne {numero} : {len(types)} cases "
                    f"au lieu de {len(lignes[0])}"
                )
            lignes.append(types)
    if taille_case is None:
        raise ValueError(f"{chemin} : taille_case manquante")
    return np.array(lignes, dtype=np.int8), taille_case


def ecrire_vegetation(chemin: str, vegetation: np.ndarray, taille_case: int, titre: str = ""):
    """Écrit une carte de végétation au format texte."""
    with open(chemin, "w", encoding="utf-8") as fichier:
        if titre:
            fichier.write(f"# {titre}\n")
        fichier.write(f"# taille_case = {taille_case}\n")
        for ligne in vegetation:
            fichier.write("".join(TYPES_VERS_SYMBOLES[t] for t in ligne) + "\n")


def chemin_altitude(chemin: str) -> str:
    """carte.txt -> carte_altitude.csv"""
    base, _ = os.path.splitext(chemin)
    return base + "_altitude.csv"


def lire_altitude(chemin: str) -> np.ndarray:
    """Lit un fichier de relief CSV."""
    return np.loadtxt(chemin, delimiter=",", ndmin=2)


def ecrire_altitude(chemin: str, altitude: np.ndarray) -> None:
    """Écrit un relief au format CSV, avec une décimale."""
    np.savetxt(chemin, altitude, delimiter=",", fmt="%.1f")

