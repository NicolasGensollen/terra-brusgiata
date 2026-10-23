import matplotlib.pyplot as plt
import numpy as np

from terra_brusgiata.terrain import relief_aleatoire


fig, axes = plt.subplots(1, 3, figsize=(13, 4))
for ax, n_lissages in zip(axes, (1, 10, 50)):
    rng = np.random.default_rng(0)               # même bruit de départ pour les trois
    altitude = relief_aleatoire((100, 100), 300, n_lissages, rng)
    image = ax.imshow(altitude, cmap="terrain", vmin=0, vmax=300)
    ax.contour(altitude, levels=10, colors="black", linewidths=0.4)
    ax.set_title(f"{n_lissages} lissage{'s' if n_lissages > 1 else ''}")
    ax.set_xticks([])
    ax.set_yticks([])
fig.colorbar(image, ax=axes, label="altitude (m)", shrink=0.9)
plt.savefig("./figures/TP2/question_2_4.png")
plt.show()
