from terra_brusgiata.banc import charger_scenarios, evaluer, statistiques
from terra_brusgiata.strategies import fabrique_arrosage, fabrique_mixte, fabrique_parefeux


NOMS = ("alata", "pozzo", "nord_est", "deux_foyers")
GRAINES_ENTRAINEMENT = range(20)
GRAINES_TEST = range(1000, 1020)
FABRIQUES = {"parefeux": fabrique_parefeux, "arrosage": fabrique_arrosage,
             "mixte": fabrique_mixte}
VALEURS = {"parefeux": (3, 4, 5, 6, 7, 8, 10),
           "arrosage": (0, 1, 2, 3, 4, 6, 8),
           "mixte": (0, 12, 24, 36, 48, 60, 72)}

scenarios = charger_scenarios([f"scenarios/{nom}.json" for nom in NOMS])
references = {}


def gain_moyen(lignes):
    return statistiques([l["gain"] for l in lignes])["moyenne"]


# 1. Entraînement : évaluer toutes les configurations des questions 5.2 et 5.3
entrainement = {}
for nom, valeurs in VALEURS.items():
    for valeur in valeurs:
        entrainement[(nom, valeur)] = evaluer(FABRIQUES[nom](valeur), scenarios,
                                              GRAINES_ENTRAINEMENT, references)

# 2. Retenir les huit meilleures, en écartant les configurations identiques
classement = sorted(entrainement, key=lambda c: -gain_moyen(entrainement[c]))
retenues, deja_vus = [], set()
for configuration in classement:
    signature = tuple(l["gain"] for l in entrainement[configuration])
    if signature not in deja_vus:
        deja_vus.add(signature)
        retenues.append(configuration)
retenues = retenues[:8]

# 3. Test : réévaluer les huit configurations retenues sur de nouvelles graines
test = {configuration: evaluer(FABRIQUES[configuration[0]](configuration[1]),
                               scenarios, GRAINES_TEST, references)
        for configuration in retenues}
rangs_test = sorted(retenues, key=lambda c: -gain_moyen(test[c]))

print(f"{'configuration':<14}{'entraînement':>14}{'rang':>6}{'test':>8}{'rang':>6}")
for rang, configuration in enumerate(retenues, start=1):
    nom, valeur = configuration
    print(f"{nom + ' ' + str(valeur):<14}"
          f"{gain_moyen(entrainement[configuration]):>14.0f}{rang:>6}"
          f"{gain_moyen(test[configuration]):>8.0f}"
          f"{rangs_test.index(configuration) + 1:>6}")
