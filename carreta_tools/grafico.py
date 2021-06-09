import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn')

hero = ['Tiny', 'Axe', 'Lone Druid']
winrate = [5, 7, 8]
matches = [7, 4, 3]

# s=tamanho
# marker=marcador
plt.scatter(winrate, matches, s=150)

plt.show()
