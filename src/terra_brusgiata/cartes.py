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


