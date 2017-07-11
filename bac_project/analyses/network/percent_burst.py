import numpy as np
import os
from load_variables import load_params, load_pop
from analyses import functions

__author__ = 'caro'

pop = 'p1'
folder = '../../simulation/network/data/Bahl2_strongerMartinotti/'
n_cells = 80
trial = 0
burst_len = 10

t, tstop, dt, onset, f, n_trials = load_params(folder)
APs_all = load_pop(folder, pop, n_cells, 1)
APs = APs_all[:, trial]
v_tuft = np.load(folder+'trial'+str(trial)+'/v_tuft_'+pop+'.npy')

folder_sav = folder + 'figures/occurence/'
if not os.path.exists(folder_sav): os.makedirs(folder_sav)

n_lflb_p1 = 54
n_lfhb_p1 = 24
n_hfhb_p1 = 2
n_p1 = n_lflb_p1 + n_lfhb_p1 + n_hfhb_p1  # in total 80 p1: ACC24
n_lflb_p2 = 63
n_lfhb_p2 = 14
n_hfhb_p2 = 3
n_p2 = n_lflb_p2 + n_lfhb_p2 + n_hfhb_p2 # in total 80 p2: latPFC6_8_9
n_m2 = 40

if pop == 'p1':
    n = [0, n_lflb_p1, n_lfhb_p1, n_hfhb_p1]
elif pop == 'p2':
    n = [0, n_lflb_p2, n_lfhb_p2, n_hfhb_p2]

fr_mean = np.zeros(len(n)-1)
BAC_percent_mean = np.zeros(len(n)-1)
burst_percent_mean = np.zeros(len(n)-1)
for i in range(2, len(n)+1):
    fr = np.zeros(n[i-1])
    BAC_percent = np.zeros(n[i-1])
    burst_percent = np.zeros(n[i-1])

    for k, j in enumerate(range(np.sum(n[:i-1]), np.sum(n[:i]))):

        # firing rate
        fr[k] = np.size(APs[j]) / (tstop/1000)

        # percent burst
        burst_len = 10
        BAC_percent[k], FAC_percent, other_burst_percent, burst_percent[k] = functions.percentage_burst(APs[j], v_tuft[j],
                                                                                              burst_len, dt)
    print 'mean firing rate ('+pop+' group '+str(i-1)+'): '
    print np.mean(fr)
    fr_mean[i-2] = np.mean(fr)
    print 'mean BAC percent, burst percent ('+pop+' group '+str(i-1)+'): '
    print np.mean(BAC_percent), np.mean(burst_percent)
    BAC_percent_mean[i-2] = np.mean(BAC_percent)
    burst_percent_mean[i-2] = np.mean(burst_percent)

np.savetxt(folder_sav+'fr.txt', fr_mean)
np.savetxt(folder_sav+'BAC_percent.txt', BAC_percent_mean)
np.savetxt(folder_sav+'burst_percent.txt', burst_percent_mean)