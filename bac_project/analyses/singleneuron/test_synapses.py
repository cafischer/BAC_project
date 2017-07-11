# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from __future__ import division
from neuron import h
import numpy as np
import pylab as pl
import os
from insert_synapses import insert_syn, insert_osc, insert_syn_varweights, make_stim, make_con
%matplotlib inline
# Load NEURON libraries
h.load_file("stdrun.hoc")

# <codecell>

modelname = "Martinotti.hoc"
h.nrn_load_dll("../../channels/x86_64/.libs/libnrnmech.so")
h.load_file(1, "../../models/"+modelname)

# <codecell>

tstop = 1000
dt = 0.025
onset = 0
h.tstop = tstop + onset # set before synapses are inserted 

# <codecell>

# Insert synapses
syn = [[]]*2
syn[0], stim, con = insert_syn(5, ['GABA'], [0.1], onset+200, 0, h.soma, 0.5, 10)
syn[1], stim1, con1 = insert_syn(5, ['NMDA'], [0.05], onset+100, 1, h.soma, 0.5, 20)
#syn[0], stim, con = insert_syn(1, ['GABA_depress'], [0.06], onset, 0, h.soma, 0.5, 14)


#params_exc = {'n_stim':2, 'kinds':['AMPA'], 'weights_mean':[0.00035], 
#              'weights_std':[0.001], 'start':0, 'noise':0.5, 'section':h.dend, 'pos':0.5, 'freq':10}
#syn[0], stim_exc_tmp, con_exc_tmp = insert_syn_varweights(**params_exc) 

#weights: normal: AMPA: 0.00035, NMDA: 0.005, GABA: 0.01 facil: AMPA: 0.00035, NMDA: 0.000035, GABA: 0.06

# <codecell>

# Create the Recording Vectors 
vec_t = h.Vector()
vec_v = h.Vector()
#vec_v_tuft = h.Vector()
#vec_v_tuft.record(h.tuft(0)._ref_v)
vec_t.record(h._ref_t) # Time
vec_v.record(h.soma(0.5)._ref_v) # Voltage

# <codecell>

vec_i = [] # for the individual synaptic currents
for syn_list in list(syn):
    for s in syn_list: 
        tmp = h.Vector()
        tmp.record(s._ref_i)
        vec_i.append(tmp)

# <codecell>

# Run simulation
h.tstop = tstop
h.v_init = -50 
h.init()
h.run()

# <codecell>

# Cut off onset 
v = np.array(vec_v)[int(onset/dt):int(tstop/dt)]
#v_tuft = np.array(vec_v_tuft)[int(onset/h.dt):int(tstop/dt)]
t = np.array(vec_t)[int(onset/dt):int(tstop/dt)]

# <codecell>

## Plot: Currents
currents = [[]] * len(vec_i)
for idx, current in enumerate(vec_i):
    currents[idx] = np.array(current)[int(onset/dt):int(tstop/dt)]
    
# total synapic current
itotal = np.zeros(np.size(t))
for i in currents:
    itotal += i

pl.plot(t, itotal)
pl.xlim(onset,tstop)
pl.show()

for i in currents:
    pl.plot(t, i)
pl.xlim(onset,tstop)
pl.show()

# <codecell>

# Plot: membrane potential
pl.plot(t,v,'k')
#pl.plot(t,v_tuft,'r')
pl.ylabel('Membrane Potential (mV)')
pl.xlabel('Time (ms)')
pl.xlim(onset,tstop)
pl.show()

# <codecell>


