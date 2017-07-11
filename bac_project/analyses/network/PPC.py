from __future__ import division
import numpy as np
import os
from analyses.network.load_variables import load_params, load_pop, load_lfp
from analyses.functions import get_phases_fft, get_PPC, get_APs_kind

# load data
folder = '../../simulation/network/data/Bahl2_strongerMartinotti/'
pop = 'p1'
folder_sav = folder + 'figures/PPC/'+pop+'/'
if not os.path.exists(folder_sav): os.makedirs(folder_sav)
n_cells = 80
burst_len = 10  # ISI between APs to identify bursts
f = np.arange(4, 121, 4)  # frequency at which the PPC is determined
np.savetxt(folder_sav+'f.txt', f)
min_APs = 10  # minimum number of APs for PPC analysis
cycles = 5  # number of cycles which should be enclosed by the window (for phase analyis)
df = 0.5  # distance between frequencies coming out of the fft
n_tests = 100

t, tstop, dt, onset, freq, n_trials = load_params(folder)
APs_all = load_pop(folder, pop, n_cells, n_trials)
lfp = load_lfp(folder, n_trials, dt)

# compute the length of the window for fft
window_len_t_min = (1/f[0]) * cycles * 1000  # duration the window for smallest frequency
window_len_min = int(window_len_t_min / dt)
window_len = 1 / ((dt/1000) * df)  # window_len = 1 / ((dt/1000) * df)
window_len_t = window_len * dt
if window_len < window_len_min:  # window_len should contain at least n cycles of each frequency
    raise ValueError('Window for fft too small.')

for kind in ['burst', 'single', 'BAC']:
    # get APs of this kind
    APs_kind = get_APs_kind(kind, APs_all, n_cells, n_trials, burst_len, dt,  folder, pop)

    # save the number per trial and sort out trials with too less spikes
    num_APs = np.zeros([n_cells, n_trials])
    for cell in range(n_cells):
        for trial in range(n_trials):

            APs = APs_kind[cell, trial]

            # prune APs that cannot have a window for fft
            APs = APs[APs < tstop-window_len_t]

            # sort out trials where there are too few APs
            if len(APs) < min_APs:
                APs_kind[cell, trial] = np.nan
            else:
                APs_kind[cell, trial] = APs

            # number of usable bursts for this cell and trial
            num_APs[cell, trial] = len(APs)

    np.savetxt(folder_sav+'num_'+kind+'.txt', num_APs)

    # compute PPC
    PPC = np.zeros([n_cells, len(f)])
    for cell in range(n_cells):
        for i, freq in enumerate(f):

            # compute the phases of the APs
            phases = []
            for trial in range(n_trials):
                if APs_kind[cell, trial] is not np.nan:
                    phases.append(get_phases_fft(APs_kind[cell, trial], freq, lfp[trial], window_len, dt))

            # compute the PPC
            if len(phases) <= 1:
                PPC[cell, i] = np.nan
            else:
                PPC[cell, i] = get_PPC(phases)
    np.savetxt(folder_sav+'PPC_'+kind+'.txt', PPC)