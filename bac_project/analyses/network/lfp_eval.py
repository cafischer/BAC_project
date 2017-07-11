# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from __future__ import division
from general_functions.plotting import plot_style
import numpy as np
import pylab as pl
import scipy
import os
from load_variables import load_params, load_lfp

# <codecell>

folder = '../../simulation/network/data/Bahl2/'

freq = 16  # freq of oscillatory inhibition
t, tstop, dt, onset, f, n_trials = load_params(folder)
t = np.arange(0, tstop+dt, dt)
n_trials = 1
lfp = load_lfp(folder, n_trials, dt)
lfp = lfp[0]
folder_sav = folder + 'figures/lfp_eval/'
if not os.path.exists(folder_sav): os.makedirs(folder_sav)

# <codecell>

# fft of lfp
lfp_fft = np.fft.fft(lfp)
ps = np.abs(lfp_fft)**2
freqs = np.fft.fftfreq(lfp.size, d=dt/1000)

fig, ax = pl.subplots(1)
pl.plot(freqs[1:np.size(freqs)/2], ps[1:np.size(freqs)/2], 'k')
plot_style(ax, 'Frequency (Hz)', 'Power of the LFP', [], [0,2500000000])
ax.set_xscale('log')
pl.xlim([1, 1000])
pl.savefig(folder_sav+'LFP_power.svg') 

# <codecell>

# Plot lfp and underlying oscillation

lfp = (lfp - np.mean(lfp)) / np.max(lfp)  # normalize lfp

# compute underlying oscillatory function
t2 = np.arange(0, 2*tstop+onset-dt, dt)  # first with onset to cut the oscillatory function off at the right position
osc = np.cos(2*np.pi*t2*freq/1000)
osc = osc[onset/dt:]

# plot: fp and oscillatory inhibition
fig, ax = pl.subplots(1)
pl.plot(t, lfp, 'k', label='LFP')
pl.plot(t, osc[0:np.size(t)], 'b', label='inh. osc.')
plot_style(ax, 'Time (ms)', '', [0, 1000], [pl.ylim()[0]-0.25, pl.ylim()[1]+0.25], True)

# cross correlation between lfp and oscillatory inhibition
corr = scipy.signal.correlate(osc, lfp, mode='valid')

fig, ax = pl.subplots(1)
ax.plot(t-tstop/2, corr, 'k') 
plot_style(ax, 'Time (ms)', 'Cross correlation \n between LFP and Cosine', [-200, 200], [])

# <codecell>


