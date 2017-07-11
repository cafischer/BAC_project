from __future__ import division
from general_functions.plotting import plot_style
from general_functions import *
import numpy as np
import matplotlib.pyplot as pl
import os
from neuron import h 
from recording.record import rec

# load NEURON libraries
h.load_file("stdrun.hoc")
h("""cvode.active(0)""")  # unvariable time step
h.nrn_load_dll(complete_mechanismdir("../../model/channels"))


# Load cell 
modelname = "Pyramidal.hoc"
h.load_file(1, "../../model/models/"+modelname)


def constcurrent(folder, cell, amp, dur, delay, onset, tstop=1000, dt=0.025):
    
    # save  
    #if not os.path.exists(folder): os.makedirs(folder)
    
    # Put an IClamp at the soma
    stim = h.IClamp(0.5, sec=cell.soma) 
    stim.delay = delay
    stim.dur = dur 
    stim.amp = amp
    
    # Put an IClamp at the tuft
    stim = h.IClamp(0.5, sec=cell.tuft) 
    stim.delay = delay
    stim.dur = dur 
    stim.amp = amp

    # create the recording vectors 
    vec_v = []
    d = []
    for i, section in enumerate([cell.soma, cell.apic, cell.tuft]):
        for j, pos in enumerate(np.arange(0, 1.1, 0.25)):
            vec_v_tmp = rec(section, 'v')
            vec_v.append(vec_v_tmp)
            if i == 0: d.append(pos*section.L)
            if i == 1: d.append(pos*section.L + cell.soma.L)
            if i == 2: d.append(pos*section.L + cell.soma.L + cell.apic.L)
            
    section = cell.tuft
    vec_ina = rec(section, 'ina')
    vec_ica = rec(section, 'ica')
    vec_ik = rec(section, 'ik')
    vec_ih = rec(section, 'Iqq_ih')

    # run simulation
    h.tstop = tstop + onset
    h.steps_per_ms = 1 / dt
    h.dt = dt
    h.v_init = -70
    h.init()
    h.run()

    # cut off onset 
    v = []
    for vec in vec_v:
        v.append(np.array(vec)[time2idx(onset, dt):-1])
    
    # Plot: time vs distance to soma vs membrane potential
    v = np.array(v)
    t = np.arange(0,tstop,dt)
    d = np.array(d)
    
    fig, ax = pl.subplots(1)
    plot_style(ax, 'Time (ms)', 'Distance to soma (um)', [0, tstop], [0, np.max(d)])
    pl.pcolor(t, d, v)
    pl.colorbar()
    pl.show()
    #pl.savefig(folder+'t_dist_v.svg')
    
    # Plot: membrane potential
    t = np.arange(0,tstop,dt)
    
    fig, ax = pl.subplots(1)
    plot_style(ax, 'Time (ms)', 'Membrane potential (mV)', [], [])
    ax.plot(t, v[0], 'k')
    ax.plot(t, v[-1], 'r')
    pl.show()
    
    # Plot_currents
    ina = np.array(vec_ina)[time2idx(onset, dt):-1]
    ica = np.array(vec_ica)[time2idx(onset, dt):-1]
    ik = np.array(vec_ik)[time2idx(onset, dt):-1]
    ih = np.array(vec_ih)[time2idx(onset, dt):-1]
    
    fig, ax = pl.subplots(1)
    ax.plot(t, ina,'g', label='Na+')
    ax.plot(t, ica,'y', label='Ca2+')
    ax.plot(t, ik,'r', label='K+')
    ax.plot(t, ih,'b', label='H')
    ax.plot(t,v[-1]*-0.0001 - 0.006,'k', label='v_tuft')
    plot_style(ax, 'Time (ms)', 'Current', [0,tstop+100], [], True)
    pl.show()
    return v
    
if __name__ == '__main__':

    folder = '/figures/currents/'
    onset = 100
    tstop = 120
    dt = 0.25
    delay = onset + 5
    dur = 80
    amp = 0.4

    cell = h.Pyramidal()

    v = constcurrent(folder, cell, amp, dur, delay, onset, tstop, dt)