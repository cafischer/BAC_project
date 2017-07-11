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
import pylab as pl
import os
from scipy.signal import hilbert
from load_variables import load_params, load_pop, load_lfp
from functions import get_bursts, get_APs_kind, bandpass, circ_r

# <codecell>

folder = '../../simulation/network/data/transient_stronger/'
pop = 'p1'
n_cells = 80
freq = 8 # frequency at which the phases are determined
burst_len = 10 # ISI between APs to identify bursts
min_n_APs = 3 # minimum number of APs for the analysis
    
t, tstop, dt, onset, f, n_trials = load_params(folder)
APs_all = load_pop(folder, pop, n_cells, n_trials)
lfp = load_lfp(folder, n_trials, dt)

window_len_t = 300 # ms
window_len = int(window_len_t / dt)

folder_sav = folder + 'figures/lfp_coherence/'
if not os.path.exists(folder_sav): os.makedirs(folder_sav)

# <codecell>

## Temporal relation of burst firing of pyramidal cells to maximal phase consistency of the lfp (single trial)
r_all = np.zeros([n_trials, 2*window_len+1])
ray_all = np.zeros([n_trials, 2*window_len+1])

# plot: lfp traces and vector strength
fig, (ax1, ax2, ax3) = pl.subplots(3) 
plot_style(ax1, '', 'LFP', [-110,110], [])
plot_style(ax2, '', 'Phase', [-110,110], [])
plot_style(ax3, 'Time relative to burst (ms)', 'Vector \nstrength', [-110,110], [0,1])
ax1.set_xticks([])
ax1.spines['bottom'].set_visible(False)
ax2.set_xticks([])
ax2.spines['bottom'].set_visible(False)
ax1.set_yticks([0, 50])
ax2.set_yticks([-1*np.pi,0, np.pi])
ax2.set_yticklabels(['-pi','0', 'pi'])
ax3.set_yticks([0, 1])
fig.subplots_adjust(hspace=0.3)
    
for trial in np.arange(n_trials):
    ray = np.zeros([n_cells, 2*window_len+1])
    r = np.zeros([n_cells, 2*window_len+1])

    # compute lfp phase
    lfp_band = bandpass(lfp[trial], 1000/dt, freq-1, freq+1, 1) # bandpass filter lfp around freq
    lfp_phases = np.angle(hilbert(lfp_band)) # infer the phase from the Hilbert transform

    for cell in np.arange(n_cells): 

        # prune APs around which a window plus frame cannot be drawn
        APs = np.array(APs_all[cell,trial])
        APs = APs[APs>window_len_t] 
        APs = APs[APs<tstop-window_len_t]

        # find the times of burst and nonburst APs
        (spikes_per_burst, burst_APs, end_burst_t, 
             single_mask, burst_mask) = get_bursts(APs, burst_len)

        # extract the phase for each time point around the AP
        n_APs = np.size(burst_APs)
        phases = np.zeros([n_APs, 2*window_len+1])

        for i, AP in enumerate(burst_APs):
            AP_idx = int(AP/dt)
            phases[i,:] = lfp_phases[AP_idx-window_len:AP_idx+window_len+1]

        if np.size(phases[:,0]) < min_n_APs: # check if the minimal number of APs is fulfilled
            r[cell,:] = np.nan
            ray[cell,:] = np.nan
            print "not enough burst APs for analysis!"
        else:
            # plot: lfp traces and vector strength
            if cell == 0 and trial == 0:  
                n = 5
                APs_tmp = burst_APs[0:n]
                phases_tmp = phases[0:n]
                r_tmp = np.zeros(2*window_len+1)
                for i in np.arange(2*window_len+1):
                    r_tmp[i] = circ_r(phases_tmp[:,i])
                for i in np.arange(n):
                    AP_idx = np.round(APs_tmp[i]/dt)
                    ax1.plot(np.arange(-1*window_len_t, window_len_t+dt, dt), lfp[0][AP_idx-window_len:AP_idx+window_len+1], 'k', label='lfp')
                    ax2.plot(np.arange(-1*window_len_t, window_len_t+dt, dt), phases_tmp[i,:], 'k', label='phase')
                ax3.plot(np.arange(-1*window_len_t, window_len_t+dt, dt), r_tmp, 'k', label='coherence')
                pl.savefig(folder+'Lfpphase_around_burst_'+pop+'_f'+str(f)+'.svg')
                outfile = open(folder_sav+'APs_tmp_burst_'+pop+'.npy', 'w')
                np.save(outfile, APs_tmp)
                outfile = open(folder_sav+'phases_tmp_burst_'+pop+'.npy', 'w')
                np.save(outfile, phases_tmp)
                outfile = open(folder_sav+'r_tmp_burst_'+pop+'.npy', 'w')
                np.save(outfile, r_tmp)

            # compute vector strength and Rayleighs Z from the phases belonging to the same time point 
            for i in np.arange(2*window_len+1):
                r[cell,i] = circ_r(phases[:,i])
                ray[cell,i] = n_APs * r[cell,i]**2

    # get rid of nans
    r = r[~np.any(np.isnan(r),axis=1), :]
    ray = ray[~np.any(np.isnan(ray),axis=1), :]

    # median over all cells
    r_med = np.median(r,0) 
    ray_med = np.median(ray,0)

    # save trial data
    r_all[trial,:] = r_med
    ray_all[trial,:] = ray_med

# save
outfile = open(folder_sav+'r_all_'+pop+'.npy', 'w')
np.save(outfile, r_all)
outfile = open(folder_sav+'ray_all_'+pop+'.npy', 'w')
np.save(outfile, ray_all)

# <codecell>

# plot: Average phase coherence at each point in the time window
mean = np.mean(r_all,0)
std = np.std(r_all,0)

fig, ax = pl.subplots(1)
ax.plot(np.arange(-1*window_len_t, window_len_t+dt, dt), mean, color='k')
#ax.fill_between(np.arange(-1*window_len_t, window_len_t+dt, dt), mean+std, mean-std, color='0.2', alpha=0.4)
ax.axvline(x=0, ymin=0, ymax=1, color='k', linewidth=3)
plot_style(ax, 'Time relative to burst (ms)', 'Vector strength', [-110, 110], [0,1])
pl.savefig(folder_sav+'/Lfp_vec_burst_'+pop+'_f'+str(f)+'.svg')

# <codecell>


