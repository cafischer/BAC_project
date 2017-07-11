import numpy as np
import pylab as pl
from neuron import h
h.load_file("stdrun.hoc")

"""Compare whether model from Bahl is the same to reformulated model"""

__author__ = 'caro'


h.nrn_load_dll("../../model/models/Bahl/channels/i686/.libs/libnrnmech.so")

v = [0] * 2
for model in [0,1]:

    if model == 0:
        h.load_file("../../model/models/Bahl/init_model2.hoc")

        # inject current
        clamp = h.IClamp(0.5, sec=h.soma)
        clamp.amp = 2
        clamp.dur = 2
        clamp.delay = 100

        clamp2 = h.IClamp(0.5, sec=h.tuft)
        clamp2.amp = 2.5
        clamp2.dur = 2
        clamp2.delay = 100

        # record membrane potential
        v_vec = h.Vector()
        v_vec.record(h.soma(0.5)._ref_v)

    else:
        h.load_file(1, "../../model/models/Bahl/Pyramidal.hoc")
        cell = h.Pyramidal()

        # inject current
        clamp = h.IClamp(0.5, sec=cell.soma)
        clamp.amp = 2
        clamp.dur = 2
        clamp.delay = 100

        clamp2 = h.IClamp(0.5, sec=cell.tuft)
        clamp2.amp = 2.5
        clamp2.dur = 2
        clamp2.delay = 100

        # record membrane potential
        v_vec = h.Vector()
        v_vec.record(cell.soma(0.5)._ref_v)

    # run simulation
    h.tstop = 300
    h.init()
    h.run()

    v[model] = v_vec.to_python()

# plot
t = np.arange(0, h.tstop+h.dt, h.dt)
pl.figure()
pl.plot(t, v[0], 'r', label='Bahl2_original')
pl.plot(t, v[1], 'k', label='Bahl2_replication')
pl.legend()
pl.show()

