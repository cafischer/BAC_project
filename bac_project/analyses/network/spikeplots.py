# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from __future__ import division
from general_functions.plotting import plot_style
from general_functions.saving import save_as_txt
import numpy as np
import pylab as pl
import scipy.stats as st
import os
from analyses.network.load_variables import load_params, load_pop, load_lfp, load_v

# <codecell>

folder = '../../simulation/network/data/Bahl2/'

t, tstop, dt, onset, f, n_trials = load_params(folder)
n_trials = 1
trial = 0
#APs_p1 = load_pop(folder, 'p1', 80, n_trials)
#APs_p2 = load_pop(folder, 'p2', 80, n_trials)
APs_m2 = load_pop(folder, 'm2', 20, n_trials)
#v_p1, v_tuft_p1 = load_v(folder, 'p1', 80, n_trials, dt)
#v_p2, v_tuft_p2 = load_v(folder, 'p2', 80, n_trials, dt)
#v_m2, _ = load_v(folder, 'm2', 20, n_trials, dt)


folder_sav = folder + 'figures/spikeplots/'
if not os.path.exists(folder_sav): os.makedirs(folder_sav)
    
#tstop = 1000

# <codecell>

# Raster plots
"""
# raster plot pyramidal 1
fig, ax = pl.subplots(1)
plot_style(ax, 'Time (ms)', 'Cell number', [0, tstop], [-1,len(APs_p1)+1])
for i in np.arange(np.shape(APs_p1)[0]):
    pl.scatter(APs_p1[i,trial],i * np.ones(np.size(APs_p1[i,trial])), s=1)
pl.xlim([0,2000])
pl.savefig(folder_sav+'/Rasterplot_p1.svg') 

# raster plot pyramidal 2
fig, ax = pl.subplots(1)
plot_style(ax, 'Time (ms)', 'Cell number', [0, tstop], [-1,len(APs_p2)+1])
for i in np.arange(np.shape(APs_p2)[0]):
    pl.scatter(APs_p2[i,trial],i * np.ones(np.size(APs_p2[i,trial])), s=1)
pl.xlim([0,2000])
pl.savefig(folder_sav+'/Rasterplot_p2.svg') 
"""
# raster plot martinotti 2
fig, ax = pl.subplots(1)
plot_style(ax, 'Time (ms)', 'Cell number', [0, tstop], [-1,len(APs_p2)+1])
for i in np.arange(np.shape(APs_m2)[0]):
    pl.scatter(APs_m2[i,trial],i * np.ones(np.size(APs_m2[i,trial])), s=1)
pl.xlim([0,2000])
pl.savefig(folder_sav+'/Rasterplot_m2.svg') 

# <codecell>

# Plot: membrane potential single neurons
fig, ax = pl.subplots(1)
plot_style(ax, 'Time (ms)', 'Membrane potential (mV)', [0, tstop], [], True)
pl.plot(t, v_p1[0][0], 'k', label='soma')
pl.plot(t, v_tuft_p1[0][0], 'r', label='tuft')
pl.xlim([0,2000])
pl.savefig(folder_sav+'v_p1.svg') 


fig, ax = pl.subplots(1)
plot_style(ax, 'Time (ms)', 'Membrane potential (mV)', [0, tstop], [], True)
pl.plot(t, v_p2[0][0], 'k', label='soma')
pl.plot(t, v_tuft_p2[0][0], 'r', label='tuft')
pl.savefig(folder_sav+'v_p2.svg')


fig, ax = pl.subplots(1)
plot_style(ax, 'Time (ms)', 'Membrane potential (mV)', [0, tstop], [], True)
pl.plot(t, v_m2[0][0], 'k', label='soma')
pl.savefig(folder_sav+'v_m2.svg')

# <codecell>


