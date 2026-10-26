import json
 
from terra_brusgiata.jeu import resumer_journal
from terra_brusgiata.scenarios import jouer_scenario
from terra_brusgiata.strategies import arroser_devant, parefeux_devant, proteger_maisons
from terra_brusgiata.affichage import animer_partie
 
 
STRATEGIES = (proteger_maisons, arroser_devant, parefeux_devant)
 
for graine in (1, 2):
    for nom in ("alata", "pozzo"):
        with open(f"scenarios/{nom}.json", encoding="utf-8") as fichier:
            scenario = json.load(fichier)
        scenario["graine"] = graine
        with open("scenarios/essai.json", "w", encoding="utf-8") as fichier:
            json.dump(scenario, fichier)
        gains = [jouer_scenario("scenarios/essai.json", s)["gain"]
                 for s in STRATEGIES]
        print(graine, nom, gains)


resultat = jouer_scenario("scenarios/alata.json", parefeux_devant)
resumer_journal(resultat)
animation = animer_partie(resultat, altitude=resultat["etat_final"]["altitude"])

