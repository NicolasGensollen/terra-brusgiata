import time
 
from terra_brusgiata.strategies import arroser_devant, proteger_maisons
from terra_brusgiata.banc import charger_scenarios, evaluer 

NOMS = ("alata", "pozzo", "nord_est", "deux_foyers")

scenarios = charger_scenarios([f"scenarios/{nom}.json" for nom in NOMS])

references = {}

for strategie in (proteger_maisons, arroser_devant):
    debut = time.perf_counter()
    evaluer(strategie, scenarios, range(30), references)
    print(f"{strategie.__name__} : {time.perf_counter() - debut:.1f} s")

