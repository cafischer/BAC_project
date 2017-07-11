from __future__ import division
from analyses.functions import circ_median
import numpy as np
import matplotlib.pyplot as plt

phases = [0, 0.1, 0.6, 0.1, 0.2, np.pi, np.pi+0.3]

print phases
print np.mod(phases, 2*np.pi)

print circ_median(phases)

# plot
N = len(phases)
bottom = 0
max_height = 4

theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
#radii = max_height*np.random.rand(N)
width = 0.1 #(2*np.pi) / N

ax = plt.subplot(111, polar=True)
bars = ax.bar(phases, np.ones(len(phases)), width=width, bottom=bottom)

# Use custom colors and opacity
for r, bar in zip(phases, bars):
    #bar.set_facecolor(plt.cm.jet(r / 10.))
    bar.set_alpha(0.8)

plt.show()


# circ histogram
phases = np.mod(phases, 2*np.pi)
bar_width = 0.5
x = np.arange(0, 2*np.pi + bar_width, bar_width)
#number = np.ones(len(phases))
bottom = 0
n_cells = 1

number, x_tmp, _ = plt.hist(phases, bins=x) #, weights=np.ones(np.size(phases))/n_cells)

ax = plt.subplot(111, polar=True)
bars = ax.bar(x_tmp[:-1], number, width=bar_width, bottom=bottom)

# Use custom colors and opacity
for r, bar in zip(phases, bars):
    bar.set_facecolor(plt.cm.jet(r / 10.))
    bar.set_alpha(0.8)

plt.show()