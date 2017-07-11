from __future__ import division
from general_functions.plotting import plot_style
from general_functions.saving import save_as_txt
import numpy as np
import pylab as pl
import os
from load_variables import load_params, load_pop
from analyses.functions import percentage_burst

# <codecell>

folder = '../../simulation/network/data/Bahl2/'
n_cells = 80
trial = 0
burst_len = 10 

t, tstop, dt, onset, f, n_trials = load_params(folder)
APs_all_p1 = load_pop(folder, 'p1', n_cells, 1)
APs_all_p2 = load_pop(folder, 'p2', n_cells, 1)

folder_sav = folder + 'figures/occurence/'
if not os.path.exists(folder_sav): os.makedirs(folder_sav)

# <markdowncell>

# folder = '../../simulation/network/data/BAC_f16/'
# folder_sav = folder + 'figures/occurence/'
# 
# BAC_percent_p1 = np.load(folder_sav+'BAC_percent_p1.npy')
# FAC_percent_p1 = np.load(folder_sav+'FAC_percent_p1.npy')
# other_burst_percent_p1 = np.load(folder_sav+'other_burst_percent_p1.npy')
# BAC_percent_p2 = np.load(folder_sav+'BAC_percent_p2.npy')
# FAC_percent_p2 = np.load(folder_sav+'FAC_percent_p2.npy')
# other_burst_percent_p2 = np.load(folder_sav+'other_burst_percent_p2.npy')

# <codecell>

## Occurence of bursts and BACs compared to baseline

# percentages of occurence p1
BAC_percent_p1 = np.zeros(n_cells)
FAC_percent_p1 = np.zeros(n_cells)
other_burst_percent_p1 = np.zeros(n_cells)
burst_percent_p1 = np.zeros(n_cells)

for cell in np.arange(n_cells): 
        APs = np.array(APs_all_p1[cell,0])
        v_tuft = np.load(folder+'trial'+str(trial)+'/v_tuft_p1.npy')
        (BAC_percent_p1[cell], FAC_percent_p1[cell], other_burst_percent_p1[cell], 
         burst_percent_p1[cell]) = percentage_burst(APs, v_tuft[cell,:], burst_len, dt)
        
# percentages of occurence p2
BAC_percent_p2 = np.zeros(n_cells)
FAC_percent_p2 = np.zeros(n_cells)
other_burst_percent_p2 = np.zeros(n_cells)
burst_percent_p2 = np.zeros(n_cells)

for cell in np.arange(n_cells): 
        APs = np.array(APs_all_p2[cell,0])
        v_tuft = np.load(folder+'trial'+str(trial)+'/v_tuft_p2.npy')
        (BAC_percent_p2[cell], FAC_percent_p2[cell], other_burst_percent_p2[cell], 
         burst_percent_p2[cell]) = percentage_burst(APs, v_tuft[cell,:], burst_len, dt)

# Save: Occurence of bursts        
outfile = open(folder_sav+'BAC_percent_p1.npy', 'w')
np.save(outfile, BAC_percent_p1)
outfile = open(folder_sav+'FAC_percent_p1.npy', 'w')
np.save(outfile, FAC_percent_p1)
outfile = open(folder_sav+'other_burst_percent_p1.npy', 'w')
np.save(outfile, other_burst_percent_p1)
outfile = open(folder_sav+'BAC_percent_p2.npy', 'w')
np.save(outfile, BAC_percent_p2)
outfile = open(folder_sav+'FAC_percent_p2.npy', 'w')
np.save(outfile, FAC_percent_p2)
outfile = open(folder_sav+'other_burst_percent_p2.npy', 'w')
np.save(outfile, other_burst_percent_p2)
    
# Plot: Occurence of BAC, FAC, others (with respect to all spike events)   
fig, ax = pl.subplots(1)
error_k = {'capsize':5, 'markeredgewidth':2} 
pl.bar(0.1, np.mean(BAC_percent_p1,0), 0.1, yerr=np.std(BAC_percent_p1,0), color='#998ec3', ecolor='k', error_kw=error_k, label='BAC')
pl.bar(0.4, np.mean(FAC_percent_p1,0), 0.1, yerr=np.std(FAC_percent_p1,0), color='#f1a340', ecolor='k', error_kw=error_k, label='FAC')
pl.bar(0.7, np.mean(other_burst_percent_p1,0), 0.1, yerr=np.std(other_burst_percent_p1,0), color='#f7f7f7', ecolor='k', error_kw=error_k, label='Others')

pl.bar(0.2, np.mean(BAC_percent_p2,0), 0.1, yerr=np.std(BAC_percent_p2,0), color='#998ec3', ecolor='k', error_kw=error_k)
pl.bar(0.5, np.mean(FAC_percent_p2,0), 0.1, yerr=np.std(FAC_percent_p2,0), color='#f1a340', ecolor='k', error_kw=error_k)
pl.bar(0.8, np.mean(other_burst_percent_p2,0), 0.1, yerr=np.std(other_burst_percent_p2,0), color='#f7f7f7', ecolor='k', error_kw=error_k)

pl.xticks([0.15, 0.25, 0.45, 0.55, 0.75, 0.85])
ax.set_xticklabels(['P1', 'P2', 'P1', 'P2', 'P1', 'P2'])
plot_style(ax, '', 'Percentage \nof Events', [0,1], [0, 80], True) 
 
pl.savefig(folder_sav+'Percentage_BACFACother.svg')
save_as_txt(folder_sav,'Percentage_BACFACother', 
            'BAC_avg_p1: '+str(np.mean(BAC_percent_p1,0))+'\n'+'BAC__avg_p2: '+str(np.mean(BAC_percent_p2,0)) + '\n'
            +'FAC_avg_p1: '+str(np.mean(FAC_percent_p1,0))+'\n'+'FAC_avg_p2: '+str(np.mean(FAC_percent_p2,0)) + '\n'
            +'other_burst_avg_p1: '+str(np.mean(other_burst_percent_p1,0))+'\n'+'other_burst_avg_p2: '+str(np.mean(other_burst_percent_p2,0)))

# <codecell>


