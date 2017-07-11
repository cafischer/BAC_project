# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# add paths to import files from other folders
import sys
sys.path.insert(0, '../../general_functions')

import pylab as pl
import numpy as np
from neuron import h
from model_output import m_params_reg
from target_output import t_params_reg
import os
from plotting import plot_style
from saving import save_as_txt
%matplotlib inline
# Load NEURON libraries
h.load_file("stdrun.hoc")

# <codecell>

def constcurrent(modelname, amp, dur, delay, tstop=1000, dt=0.025, save=False):
    
    onset = 100
    h.tstop = tstop
    h.dt = dt
    
    # file to save  
    if save: 
        folder = 'figures/reg_spiking/'+modelname+'_'+str(amp)+'_'+str(dur)+'_'+str(delay)+'_'+str(tstop)
        if not os.path.exists(folder): os.makedirs(folder)
    
    # Put an IClamp at the Soma
    stim = h.IClamp(0.5, sec=h.soma) 
    stim.delay = delay
    stim.dur = dur 
    stim.amp = amp

    # Create the Recording Vectors 
    vec_t = h.Vector()
    vec_v = h.Vector()
    vec_t.record(h._ref_t) # Time
    vec_v.record(h.soma(0.5)._ref_v) # Voltage
    vec_AP = h.Vector()
    APc = h.APCount(0.5, sec=h.soma) 
    APc.record(vec_AP) # Time of Action Potentials

    # run simulation
    h.tstop = tstop
    h.v_init = -70
    h.init()
    h.run()

    # Calculate target values
    [t_spikefreq, t_ISI_CV, t_initial_ISI, t_spike_latency, t_AP_peak, 
    t_AHP_depth_fast, t_AHP_depth_slow, t_AHP_time_slow, t_AP_halfwidth, t_spikefreq1amp] = t_params_reg()

    # model output
    [m_spikefreq, m_ISI_CV, m_initial_ISI, m_spike_latency, m_AP_peak, 
    m_AHP_depth_fast, m_AHP_depth_slow, m_AHP_time_slow, m_AP_halfwidth] = m_params_reg(APc, vec_AP, vec_v, vec_t, dur, onset, -65)

    # Plot membrane potential
    fig, ax = pl.subplots(1)
    pl.plot(vec_t, vec_v, 'k')
    plot_style(ax, 'Time (ms)', 'Membrane Potential (mV)', [onset, tstop], [])
    if save: pl.savefig(folder+'/v.svg')
    pl.show()

    print "spikefreq: ", m_spikefreq, "target: ", t_spikefreq
    print "ISI_CV: ", m_ISI_CV, "target: ", t_ISI_CV
    print "initial_ISI: ", m_initial_ISI, "target: ", t_initial_ISI
    print "spike_latency: ", m_spike_latency, "target: ", t_spike_latency
    print "AP_peak: ", m_AP_peak, "target: ", t_AP_peak
    print "AHP_depth_fast: ", m_AHP_depth_fast, "target: ", t_AHP_depth_fast
    print "AHP_depth_slow: ", m_AHP_depth_slow, "target: ", t_AHP_depth_slow
    print "AHP_time_slow: ", m_AHP_time_slow, "target: ", t_AHP_time_slow
    print "AP_halfwidth: ", m_AP_halfwidth, "target: ", t_AP_halfwidth
    
    if save: 
        save_as_txt(folder, '/features_reg_spiking.txt', "spikefreq: " + repr(m_spikefreq) + "\n" 
                + "ISI_CV: " + repr(m_ISI_CV) + "\n"
                + "initial_ISI: " + repr(m_initial_ISI) + "\n"
                + "spike_latency: " + repr(m_spike_latency) + "\n"
                + "AP_peak: " + repr(m_AP_peak) + "\n"
                + "AHP_depth_fast: " + repr(m_AHP_depth_fast) + "\n"
                + "AHP_depth_slow: " + repr(m_AHP_depth_slow) + "\n"
                + "AHP_time_slow: " + repr(m_AHP_time_slow) + "\n"
                + "AP_halfwidth: " + repr(m_AP_halfwidth))
        
    return vec_AP, vec_v

# <codecell>

# Load cell 
modelname = "Martinotti"
h.nrn_load_dll("../../channels/x86_64/.libs/libnrnmech.so")
h.load_file(1,"../../models/"+modelname+".hoc") 

# <codecell>

# Parameters
delay = 200
dur = 10 #1000 
amp = 0.5
tstop = dur + 2 * delay # some time before and after stimulation
tstop = 1000
dt = 0.025

vec_AP, vec_v = constcurrent(modelname, amp, dur, delay, tstop, dt, False)

# <codecell>


