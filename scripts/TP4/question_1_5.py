from terra_brusgiata.strategies import arroser_devant, parefeux_devant, proteger_maisons
from terra_brusgiata.banc import evaluer, exporter_csv, charger_scenarios


NOMS = ("alata", "pozzo", "nord_est", "deux_foyers")
GRAINES = range(30)

# 1. Charger une seule fois les quatre scénarios publics
scenarios = charger_scenarios([f"scenarios/{nom}.json" for nom in NOMS])

# 2. Le cache des parties de référence, partagé par toutes les évaluations
references = {}

# 3. Évaluer les trois stratégies du sujet 3 et enregistrer les résultats
resultats = {}
for strategie in (proteger_maisons, arroser_devant, parefeux_devant):
    lignes = evaluer(strategie, scenarios, GRAINES, references)
    resultats[strategie.__name__] = lignes
    exporter_csv(lignes, f"{strategie.__name__}.csv")
    print(f"{strategie.__name__} : {len(lignes)} parties évaluées")

print(f"{len(references)} parties de référence en cache")
