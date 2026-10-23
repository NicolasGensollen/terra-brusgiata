import matplotlib.pyplot as plt

from terra_brusgiata.experiences import courbe_percolation


d, m, e = courbe_percolation(100)
plt.errorbar(d, m, yerr=e, marker="o", markersize=3, capsize=2)
plt.xlabel("Densité d'arbres")
plt.ylabel("Proportion d'arbres brûlés")
plt.show()


