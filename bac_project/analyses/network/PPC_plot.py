from __future__ import division
import numpy as np
import scipy.stats as st
from general_functions.plotting import plot_style
import pylab as pl

pop = 'p1'
folder = '../../simulation/network/data/Bahl2_strongerMartinotti/'
folder_sav = folder + 'figures/PPC/'+pop+'/'

# load PPC data
#f = np.loadtxt('f.txt')
f = np.arange(4, 121, 4)
PPC_burst = np.loadtxt(folder_sav+'PPC_burst.txt')
PPC_single = np.loadtxt(folder_sav+'PPC_single.txt')
PPC_BAC = np.loadtxt(folder_sav+'PPC_BAC.txt')
df = f[1]-f[0]

# plot burst PPC
fig, ax = pl.subplots(1)
ax.errorbar(f, st.nanmean(PPC_burst, 0), st.nanstd(PPC_burst, 0), fmt='-o', color='k', markerfacecolor='k',
            label='burst')
plot_style(ax, 'Frequency (Hz)', 'burst PPC', [f[0]-df, f[-1]+df], [])
pl.show()
pl.savefig(folder_sav+'PPC_burst.svg')

# plot: burst and single PPC
fig, ax = pl.subplots(1)
ax.errorbar(f, st.nanmean(PPC_burst, 0), st.nanstd(PPC_burst, 0), fmt='-o', color='k', markerfacecolor='#fc8d59',
            label='burst')
ax.errorbar(f, st.nanmean(PPC_single, 0), st.nanstd(PPC_single, 0), fmt='-o', color='k', markerfacecolor='#99d594',
            label='single \nspike')
plot_style(ax, 'Frequency (Hz)', 'PPC', [f[0]-df, f[-1]+df], [], True)
pl.show()
pl.savefig(folder_sav+'PPC_burstsingle.svg')

# plot: difference of burst and single PPC
PPC_diff = PPC_burst - PPC_single
fig, ax = pl.subplots(1)
ax.errorbar(f, st.nanmean(PPC_diff, 0), st.nanstd(PPC_diff, 0), fmt='-o', color='k', markerfacecolor='k')
pl.axhline(0, 0, 1, color='k', linewidth=3)
plot_style(ax, 'Frequency (Hz)', 'Difference \nburst to single PPC', [f[0]-df, f[-1]+df], [])
pl.show()
pl.savefig(folder_sav+'PPCdiff.svg')

# plot: BAC PPC
fig, ax = pl.subplots(1)
ax.errorbar(f, st.nanmean(PPC_BAC, 0), st.nanstd(PPC_BAC, 0), fmt='-o', color='k', markerfacecolor='#998ec3',
            label='BAC')
ax.errorbar(f, st.nanmean(PPC_burst, 0), st.nanstd(PPC_burst, 0), fmt='-o', color='k', markerfacecolor='#fc8d59',
            label='burst')
ax.errorbar(f, st.nanmean(PPC_single, 0), st.nanstd(PPC_single, 0), fmt='-o', color='k', markerfacecolor='#99d594',
            label='single \nspike')
plot_style(ax, 'Frequency (Hz)', 'BAC PPC', [f[0]-df, f[-1]+df], [])
pl.show()
pl.savefig(folder_sav+'PPC_BAC.svg')


# PPC per group
n_lflb_p1 = 54
n_lfhb_p1 = 24
n_hfhb_p1 = 2
n_p1 = n_lflb_p1 + n_lfhb_p1 + n_hfhb_p1  # in total 80 p1: ACC24
n_lflb_p2 = 63
n_lfhb_p2 = 14
n_hfhb_p2 = 3
n_p2 = n_lflb_p2 + n_lfhb_p2 + n_hfhb_p2  # in total 80 p2: latPFC6_8_9
n_m2 = 40

if pop == 'p1':
    n = [0, n_lflb_p1, n_lfhb_p1, n_hfhb_p1]
elif pop == 'p2':
    n = [0, n_lflb_p2, n_lfhb_p2, n_hfhb_p2]

for i in range(2, len(n)+1):
    PPC_burst_group = PPC_burst[range(np.sum(n[:i-1]), np.sum(n[:i]))]
    PPC_single_group = PPC_single[range(np.sum(n[:i-1]), np.sum(n[:i]))]
    PPC_BAC_group = PPC_BAC[range(np.sum(n[:i-1]), np.sum(n[:i]))]

    # plot burst PPC
    fig, ax = pl.subplots(1)
    ax.errorbar(f, st.nanmean(PPC_burst_group, 0), st.nanstd(PPC_burst_group, 0), fmt='-o', color='k',
                markerfacecolor='k', label='burst')
    plot_style(ax, 'Frequency (Hz)', 'burst PPC', [f[0]-df, f[-1]+df], [])
    pl.show()
    pl.savefig(folder_sav+'PPC_burst_group'+str(i-2)+'.svg')

    # plot: burst and single PPC
    fig, ax = pl.subplots(1)
    ax.errorbar(f, st.nanmean(PPC_burst_group, 0), st.nanstd(PPC_burst_group, 0),
                fmt='-o', color='k', markerfacecolor='#fc8d59',
                label='burst')
    ax.errorbar(f, st.nanmean(PPC_single_group, 0), st.nanstd(PPC_single_group, 0), fmt='-o', color='k',
                markerfacecolor='#99d594', label='single \nspike')
    plot_style(ax, 'Frequency (Hz)', 'PPC', [f[0]-df, f[-1]+df], [], True)
    pl.show()
    pl.savefig(folder_sav+'PPC_burstsingle_group'+str(i-2)+'.svg')

    # plot: difference of burst and single PPC
    PPC_diff = PPC_burst_group - PPC_single_group
    fig, ax = pl.subplots(1)
    ax.errorbar(f, st.nanmean(PPC_diff, 0), st.nanstd(PPC_diff, 0), fmt='-o', color='k', markerfacecolor='k')
    pl.axhline(0, 0, 1, color='k', linewidth=3)
    plot_style(ax, 'Frequency (Hz)', 'Difference \nburst to single PPC', [f[0]-df, f[-1]+df], [])
    pl.show()
    pl.savefig(folder_sav+'PPCdiff_group'+str(i-2)+'.svg')

    # plot: BAC PPC
    fig, ax = pl.subplots(1)
    ax.errorbar(f, st.nanmean(PPC_BAC_group, 0), st.nanstd(PPC_BAC_group, 0), fmt='-o', color='k',
                markerfacecolor='#998ec3', label='BAC')
    ax.errorbar(f, st.nanmean(PPC_burst_group, 0), st.nanstd(PPC_burst_group, 0), fmt='-o', color='k',
                markerfacecolor='#fc8d59', label='burst')
    ax.errorbar(f, st.nanmean(PPC_single_group, 0), st.nanstd(PPC_single_group, 0), fmt='-o', color='k',
                markerfacecolor='#99d594', label='single \nspike')
    plot_style(ax, 'Frequency (Hz)', 'BAC PPC', [f[0]-df, f[-1]+df], [])
    pl.show()
    pl.savefig(folder_sav+'PPC_BAC_group'+str(i-2)+'.svg')