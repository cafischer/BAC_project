from __future__ import division
import numpy as np
from analyses.functions import lowpass


def load_params(folder):
    
    dt = np.load(folder+'dt.npy')
    tstop = np.load(folder+'tstop.npy')
    onset = np.load(folder+'onset.npy')
    t = np.arange(0,tstop,dt)
    f = np.load(folder+'f.npy')
    n_trials = np.load(folder+'n_trials.npy')

    return t, tstop, dt, onset, f, n_trials


def load_pop(folder, pop, n_cells, n_trials):
    
    APs_all = np.zeros([n_cells, n_trials], dtype=object)
    for trial in np.arange(n_trials):
        for cell in np.arange(n_cells):
            APs_all[cell, trial] = np.load(folder+'trial'+str(trial)+'/APs_'+pop+'.npy')[cell]
   

    return APs_all


def load_lfp(folder, n_trials, dt):
    
    lfp = np.zeros([n_trials], dtype=object)
    for trial in np.arange(n_trials):
        vrec = np.load(folder+'trial'+str(trial)+'/vrec.npy')
        lfp[trial] = lowpass(vrec, 1000/dt, 200, 1) # low-pass filter vrec to get lfp

    return lfp

# <codecell>

def load_v(folder, pop, n_cells, n_trials, dt):
    
    v = np.zeros([n_cells,n_trials], dtype=object)
    v_tuft = np.zeros([n_cells,n_trials], dtype=object)
    for trial in np.arange(n_trials):
        for cell in np.arange(n_cells):
            v[cell,trial] = np.load(folder+'trial'+str(trial)+'/v_'+pop+'.npy')[cell]
            if pop == 'p1' or pop == 'p2': 
                v_tuft[cell,trial] = np.load(folder+'trial'+str(trial)+'/v_tuft_'+pop+'.npy')[cell]
            else:
                v_tuft = []

    return v, v_tuft

