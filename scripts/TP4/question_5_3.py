import matplotlib.pyplot as plt

from terra_brusgiata.banc import charger_scenarios, evaluer, statistiques
from terra_brusgiata.strategies import fabrique_mixte, fabrique_parefeux


NOMS = ("alata", "pozzo", "nord_est", "deux_foyers")
GRAINES = range(20)                    # mêmes graines qu'à la question 5.2
BUDGETS_EAU = (0, 12, 24, 36, 48, 60, 72)

scenarios = charger_scenarios([f"scenarios/{nom}.json" for nom in NOMS])
references = {}

# 1. Évaluer la stratégie mixte pour chaque budget d'eau
resultats_mixte = {}
for budget_eau in BUDGETS_EAU:
    lignes = evaluer(fabrique_mixte(budget_eau), scenarios, GRAINES, references)
    resultats_mixte[budget_eau] = lignes
    s = statistiques([l["gain"] for l in lignes])
    print(f"budget d'eau {budget_eau:2} : gain moyen {s['moyenne']:5.0f}, "
          f"IC 95 % [{s['ic_bas']:.0f} ; {s['ic_haut']:.0f}]")


# 2. Repérer les configurations qui jouent exactement les mêmes parties
def signature(lignes):
    return tuple(l["gain"] for l in lignes)


parefeux_3 = evaluer(fabrique_parefeux(3), scenarios, GRAINES, references)
print("\nbudget d'eau 0 identique à fabrique_parefeux(3) :",
      signature(resultats_mixte[0]) == signature(parefeux_3))
print("budgets d'eau 60 et 72 identiques :",
      signature(resultats_mixte[60]) == signature(resultats_mixte[72]))

# 3. Le gain moyen en fonction du budget d'eau
stats = [statistiques([l["gain"] for l in resultats_mixte[b]]) for b in BUDGETS_EAU]
plt.errorbar(BUDGETS_EAU, [s["moyenne"] for s in stats],
             yerr=[1.96 * s["erreur_type"] for s in stats], marker="o", capsize=4)
plt.xlabel("budget d'eau")
plt.ylabel("gain moyen (graines 0 à 19)")
plt.title("fabrique_mixte")
plt.grid(alpha=0.3)
plt.show()
