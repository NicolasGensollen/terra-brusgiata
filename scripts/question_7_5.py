import matplotlib.pyplot as plt

from terra_brusgiata.experiences import courbe_percolation


for taille in (50, 100, 200):
    d, m, e = courbe_percolation(taille)
    plt.errorbar(d, m, yerr=e, marker="o", markersize=3, capsize=2,
                 label=f"{taille} × {taille}")
plt.axvline(0.5927, color="gray", linestyle="--", label="seuil théorique ≈ 0,593")
plt.xlabel("Densité d'arbres")
plt.ylabel("Proportion d'arbres brûlés")
plt.legend()
plt.savefig("./figures/question_7_5.png")
plt.show()


