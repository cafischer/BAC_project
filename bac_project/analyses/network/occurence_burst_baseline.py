# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from __future__ import division

# add paths to import files from other folders
import sys
sys.path.insert(0, '../../general_functions')

from plotting import plot_style 
from saving import save_as_txt
import numpy as np
import os
from load_variables import load_params, load_pop
from functions import get_percentage

# <codecell>

folder = '../../simulation/network/data/test/'
pop = 'p1'
n_cells = 80
trial = 0

folder_sav, t, tstop, dt, f, n_trials = load_params(folder)
APs_all_p1 = load_pop(folder, pop, n_cells, 1)
APs_all_p1_base = load_pop('data/test_baseline/', pop, n_cells, 1)

# <codecell>

## Occurence of bursts and BACs compared to baseline

burst_len = 10 # ms

# percentages of occurence for baseline
BAC_percent_base = np.zeros(n_cells)
FAC_percent_base = np.zeros(n_cells)
other_burst_percent_base = np.zeros(n_cells)
burst_percent_base = np.zeros(n_cells)

for cell in np.arange(n_cells): 
        APs = np.array(APs_all_p1_base[cell,0])
        v_tuft = np.load('data/test_baseline/'+'trial'+str(trial)+'/v_tuft_all_'+pop+'.npy')
        (BAC_percent_base[cell], FAC_percent_base[cell], other_burst_percent_base[cell], 
             burst_percent_base[cell]) = get_percentage(APs, v_tuft[cell,:], burst_len, dt)
             
            
# average and std
BAC_percent_base_avg = np.mean(BAC_percent_base, 0)
FAC_percent_base_avg = np.mean(FAC_percent_base, 0)
other_burst_percent_base_avg = np.mean(other_burst_percent_base, 0)
burst_percent_base_avg = np.mean(burst_percent_base, 0)
BAC_percent_base_std = np.std(BAC_percent_base, 0)
FAC_percent_base_std = np.std(FAC_percent_base, 0)
other_burst_percent_base_std = np.std(other_burst_percent_base, 0)
burst_percent_base_std = np.std(burst_percent_base, 0)

# percentages of occurence for oscillatory inhibition
BAC_percent = np.zeros(n_cells)
FAC_percent = np.zeros(n_cells)
other_burst_percent = np.zeros(n_cells)
burst_percent = np.zeros(n_cells)

for cell in np.arange(n_cells): 
        APs = np.array(APs_all_p1[cell,0])
        v_tuft = np.load(folder+'trial'+str(trial)+'/v_tuft_all_'+pop+'.npy')
        (BAC_percent[cell], FAC_percent[cell], other_burst_percent[cell], 
         burst_percent[cell]) = get_percentage(APs, v_tuft[cell,:], burst_len, dt)
            
# average and std
BAC_percent_avg = np.mean(BAC_percent, 0)
FAC_percent_avg = np.mean(FAC_percent, 0)
other_burst_percent_avg = np.mean(other_burst_percent, 0)
burst_percent_avg = np.mean(burst_percent, 0)
BAC_percent_std = np.std(BAC_percent, 0)
FAC_percent_std = np.std(FAC_percent, 0)
other_burst_percent_std = np.std(other_burst_percent, 0)
burst_percent_std = np.std(burst_percent, 0)

# Plot: Occurence of bursts compared to baseline        
fig, ax = pl.subplots(1)
pl.errorbar([0,1], [burst_percent_base_avg, burst_percent_avg], [burst_percent_base_std, burst_percent_std], 
            fmt='-o', color='k', label='burst events')
pl.xticks([0,1])
ax.set_xticklabels(['Baseline', 'Attentional State'])
plot_style(ax, '', 'Proportion of Burst Events', [-0.25,1.25], [pl.ylim()[0], pl.ylim()[1]+0.25])

pl.savefig(folder_sav+'burst_len'+str(burst_len)+'/Percentage_bursts.svg')
save_as_txt(folder_sav+'burst_len'+str(burst_len),'Percentage_bursts',
            'burst_avg: '+str([burst_percent_base_avg, burst_percent_avg])+'\n'
            +'burst_std: '+ str([burst_percent_base_std, burst_percent_std]))
    

# Plot: Occurence of BAC, FAC, others compared to baseline (with respect to all spike events)   
fig, ax = pl.subplots(1)
pl.errorbar([0,1], [BAC_percent_base_avg, BAC_percent_avg], [BAC_percent_base_std, BAC_percent_std], 
            fmt='-o', color='0.0', label='BAC')
pl.errorbar([0,1], [FAC_percent_base_avg, FAC_percent_avg], [FAC_percent_base_std, FAC_percent_std], 
            fmt='-o', color='0.4', label='FAC')
pl.errorbar([0,1], [other_burst_percent_base_avg, other_burst_percent_avg], 
            [other_burst_percent_base_std, other_burst_percent_std], fmt='-o', color='0.8', label='other burst')
pl.xticks([0,1])
ax.set_xticklabels(['Baseline', 'Attentional State'])
plot_style(ax, '', 'Proportion of Events', [-0.25,1.25], [-5, pl.ylim()[1]+20]) # legend above
pl.legend(loc='upper right')
 
pl.savefig(folder_sav+'burst_len'+str(burst_len)+'/Percentage_BACFACother.svg')
save_as_txt(folder_sav+'burst_len'+str(burst_len),'Percentage_BACFACother', 
            'BAC_avg: '+str([BAC_percent_base_avg, BAC_percent_avg]) + '\n'
            +'BAC_std: '+str([BAC_percent_base_std, BAC_percent_std]) + '\n'
            +'FAC_avg: '+str([FAC_percent_base_avg, FAC_percent_avg]) + '\n'
            +'FAC_std: '+str([FAC_percent_base_std, FAC_percent_std]) + '\n'
            +'other_burst_avg: '+str([other_burst_percent_base_avg, other_burst_percent_avg]) + '\n'
            +'other_burst_std: '+str([other_burst_percent_base_std, other_burst_percent_std]))

# <codecell>


