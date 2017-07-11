from __future__ import division
from general_functions.plotting import plot_style
import numpy as np
import pylab as pl
from scipy.signal import hilbert
import os
from load_variables import load_params, load_pop, load_lfp
from analyses.functions import bandpass


folder = '../../simulation/network/data/Bahl2/'
burst_len = 10

t, tstop, dt, onset, freq, n_trials = load_params(folder)
n_trials = 3
t = np.arange(0, tstop+dt, dt)
APs_all_p1 = load_pop(folder, 'p1', 80, n_trials)
APs_all_p2 = load_pop(folder, 'p2', 80, n_trials)
APs_all_m2 = load_pop(folder, 'm2', 20, n_trials)
lfp = load_lfp(folder, n_trials, dt)
folder_sav = folder + 'figures/' + 'burst_len'+str(burst_len)+ '/plot_all/'
if not os.path.exists(folder_sav): os.makedirs(folder_sav)

# compute underlying oscillatory function
t2 = np.arange(0,tstop+onset,dt) # first with onset to cut the oscillatory function off at the right position
osc = 12*np.cos(2*np.pi*t2*freq/1000) - 60
osc = osc[onset/dt:]

# compute lfp phase
phases = np.zeros([n_trials,np.size(t)])

for trial in np.arange(n_trials):
    # bandpass filter lfp around freq
    lfp_band = bandpass(lfp[trial], 1000/dt, freq-1, freq+1, 1)
    # infer the phase from the Hilbert transform
    phases[trial, :] = np.angle(hilbert(lfp_band))

# lfp_coherence: plot with spiketrains, lfp, oscillation all under another
APs_p1 = APs_all_p1[0,0]
APs_p2 = APs_all_p2[0,0]
APs_m2 = APs_all_m2[0,0]
lfp_trial = lfp[0]
phases_trial = phases[0,:]

fig, (ax1, ax2, ax3, ax4, ax5) = pl.subplots(5)
ax1.plot(APs_p1, np.zeros(np.size(APs_p1)), '|', color='k', markersize=17, mew=1.0)
ax2.plot(APs_m2, np.zeros(np.size(APs_m2)), '|', color='k', markersize=17, mew=1.0)
ax3.plot(APs_p2, np.zeros(np.size(APs_p2)), '|', color='k', markersize=17, mew=1.0)
ax4.plot(t, lfp_trial, color='k')
ax5.plot(t, phases_trial, color='k')
fig.subplots_adjust(hspace=0)
for ax in fig.axes: 
    plot_style(ax, '', '', [200, 1200], [])
    ax.set_yticks([]) 
    ax.yaxis.labelpad = 35
for ax in fig.axes[0:-1]: 
    ax.set_xticks([])
    ax.spines['bottom'].set_visible(False)
ax1.set_ylabel('P1', rotation=0, va='center')   
ax2.set_ylabel('M2', rotation=0, va='center')
ax3.set_ylabel('P2', rotation=0, va='center')
ax4.set_ylabel('LFP', rotation=0, va='center') 
ax5.set_ylabel('Phase', rotation=0, va='center') 
ax5.set_xlabel('Time (ms)')
ax5.set_xticklabels([0,200,400,600,800,1000])
pl.savefig(folder_sav+'spiketrains'+'_f'+str(freq)+'.svg')


