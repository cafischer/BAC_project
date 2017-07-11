from __future__ import division
import numpy as np
import pylab as pl
from neuron import h
import os
from connectivity.connection import synaptic_input, synaptic_input_fromfile, gen_con_rand
from spatial_organization.spatial_placement import get_positions
from recording.record import rec, rec_APs
from general_functions.saving import save_as_txt
from general_functions import complete_mechanismdir
from analyses import functions
from time import time
from random import Random
import json

h.load_file("stdrun.hoc")  # load NEURON libraries
h("""cvode.active(0)""")  # unvariable time step
h.nrn_load_dll(complete_mechanismdir("../../connectivity/synapse_models/"))  # import synapse models

# folder to save
folder = 'data/'+'test'+'/'

# cell models
h.nrn_load_dll(complete_mechanismdir("../../model/channels/Bahl/"))
h.load_file(1, "../../model/models/Bahl/Pyramidal_reclfp.hoc")
h.load_file(1, "../../model/models/Martinotti_fast.hoc") 

# simulation parameters
tstop = 500  # ms
dt = 0.25
onset = 100  # ms
n_trials = 1
frequencies = 12  # frequency of the oscillation

# network parameters
n_lflb_p1 = 54
n_lfhb_p1 = 24
n_hfhb_p1 = 2
n_p1 = n_lflb_p1 + n_lfhb_p1 + n_hfhb_p1  # in total 80 p1: ACC24
n_lflb_p2 = 63
n_lfhb_p2 = 14
n_hfhb_p2 = 3
n_p2 = n_lflb_p2 + n_lfhb_p2 + n_hfhb_p2 # in total 80 p2: latPFC6_8_9
n_m2 = 50
sidelength = 5  # um
grid_size = 10  # grid size needs to be greater than ceil(sqrt(n_cells))
dist_areal = 1000

# inputs to p1

# low firing, low burst
freq = 10
pos = 0.5

params_stim = {'kind': 'poisson_gen', 'onset': 0, 'tstop': tstop, 'dt': dt,
               'freq': freq, 'pos': pos, 'seed_prng': time()}
params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i1_lflb_p1 = {'n_stim': 80, 'cell': 'pyramidal', 'section': 'dend', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i2_lflb_p1 = {'n_stim': 20, 'cell': 'pyramidal', 'section': 'dend', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i3_lflb_p1 = {'n_stim': 100, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i4_lflb_p1 = {'n_stim': 100, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'GABA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i5_lflb_p1 = {'n_stim': 30, 'cell': 'pyramidal', 'section': 'soma', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_stim = {'kind': 'transient_osc', 'freq_osc': frequencies, 'freq': freq, 'onset': 0, 'tstop': tstop, 'dt': dt, 'pos': pos,
               'transient': tstop, 'seed_prng': time()}
params_syn = {'kind': 'GABA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i6_lflb_p1 = {'n_stim': 50, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_lflb_p1 = [params_i1_lflb_p1, params_i2_lflb_p1, params_i3_lflb_p1, params_i4_lflb_p1, params_i5_lflb_p1,
                  params_i6_lflb_p1]

# low firing, high burst
freq = 10
pos = 0.5

params_stim = {'kind': 'poisson_gen', 'onset': 0, 'tstop': tstop, 'dt': dt,
               'freq': freq, 'pos': pos, 'seed_prng': time()}
params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i1_lfhb_p1 = {'n_stim': 50, 'cell': 'pyramidal', 'section': 'dend', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i2_lfhb_p1 = {'n_stim': 65, 'cell': 'pyramidal', 'section': 'dend', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i3_lfhb_p1 = {'n_stim': 100, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i4_lfhb_p1 = {'n_stim': 100, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'GABA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i5_lfhb_p1 = {'n_stim': 30, 'cell': 'pyramidal', 'section': 'soma', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_stim = {'kind': 'osc', 'freq_osc': frequencies,
               'freq': freq, 'onset': 0, 'tstop': tstop, 'dt': dt, 'pos': pos, 'seed_prng': time()}
params_syn = {'kind': 'GABA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i6_lfhb_p1 = {'n_stim': 50, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_lfhb_p1 = [params_i1_lfhb_p1, params_i2_lfhb_p1, params_i3_lfhb_p1, params_i4_lfhb_p1, params_i5_lfhb_p1,
                  params_i6_lfhb_p1]

# high firing, high burst
freq = 10
pos = 0.5

params_stim = {'kind': 'poisson_gen', 'onset': 0, 'tstop': tstop, 'dt': dt,
               'freq': freq, 'pos': pos, 'seed_prng': time()}
params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i1_hfhb_p1 = {'n_stim': 270, 'cell': 'pyramidal', 'section': 'dend', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i2_hfhb_p1 = {'n_stim': 0, 'cell': 'pyramidal', 'section': 'dend', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i3_hfhb_p1 = {'n_stim': 200, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i4_hfhb_p1 = {'n_stim': 60, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'GABA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i5_hfhb_p1 = {'n_stim': 10, 'cell': 'pyramidal', 'section': 'soma', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_stim = {'kind': 'osc', 'freq_osc': frequencies, 'freq': freq, 'onset': 0,
               'tstop': tstop, 'dt': dt, 'pos': pos, 'seed_prng': time()}
params_syn = {'kind': 'GABA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i6_hfhb_p1 = {'n_stim': 50, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_hfhb_p1 = [params_i1_hfhb_p1, params_i2_hfhb_p1, params_i3_hfhb_p1, params_i4_hfhb_p1, params_i5_hfhb_p1,
                  params_i6_hfhb_p1]


# inputs to p2

# low firing, low burst
freq = 10
pos = 0.5

params_stim = {'kind': 'poisson_gen', 'onset': 0, 'tstop': tstop, 'dt': dt,
               'freq': freq, 'pos': pos, 'seed_prng': time()}
params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i1_lflb_p2 = {'n_stim': 80, 'cell': 'pyramidal', 'section': 'dend', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i2_lflb_p2 = {'n_stim': 20, 'cell': 'pyramidal', 'section': 'dend', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i3_lflb_p2 = {'n_stim': 100, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i4_lflb_p2 = {'n_stim': 100, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'GABA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i5_lflb_p2 = {'n_stim': 30, 'cell': 'pyramidal', 'section': 'soma', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_lflb_p2 = [params_i1_lflb_p2, params_i2_lflb_p2, params_i3_lflb_p2, params_i4_lflb_p2, params_i5_lflb_p2]

# low firing, high burst
freq = 10
pos = 0.5

params_stim = {'kind': 'poisson_gen', 'onset': 0, 'tstop': tstop, 'dt': dt,
               'freq': freq, 'pos': pos, 'seed_prng': time()}
params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i1_lfhb_p2 = {'n_stim': 50, 'cell': 'pyramidal', 'section': 'dend', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i2_lfhb_p2 = {'n_stim': 65, 'cell': 'pyramidal', 'section': 'dend', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i3_lfhb_p2 = {'n_stim': 100, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i4_lfhb_p2 = {'n_stim': 100, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'GABA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i5_lfhb_p2 = {'n_stim': 30, 'cell': 'pyramidal', 'section': 'soma', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_lfhb_p2 = [params_i1_lfhb_p2, params_i2_lfhb_p2, params_i3_lfhb_p2, params_i4_lfhb_p2, params_i5_lfhb_p2]

# high firing, high burst
freq = 10
pos = 0.5

params_stim = {'kind': 'poisson_gen', 'onset': 0, 'tstop': tstop, 'dt': dt,
               'freq': freq, 'pos': pos, 'seed_prng': time()}
params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i1_hfhb_p2 = {'n_stim': 270, 'cell': 'pyramidal', 'section': 'dend', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i2_hfhb_p2 = {'n_stim': 0, 'cell': 'pyramidal', 'section': 'dend', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i3_hfhb_p2 = {'n_stim': 200, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i4_hfhb_p2 = {'n_stim': 60, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_syn = {'kind': 'GABA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i5_hfhb_p2 = {'n_stim': 10, 'cell': 'pyramidal', 'section': 'soma', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_hfhb_p2 = [params_i1_hfhb_p2, params_i2_hfhb_p2, params_i3_hfhb_p2, params_i4_hfhb_p2, params_i5_hfhb_p2]

# inputs to m2
params_stim = {'kind': 'poisson_gen', 'onset': 0, 'tstop': tstop, 'dt': dt,
               'freq': freq, 'pos': pos, 'seed_prng': time()}
params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i1m2 = {'n_stim': 20, 'cell': 'pyramidal', 'section': 'soma', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_stim = {'kind': 'poisson_gen', 'onset': 0, 'tstop': tstop, 'dt': dt,
               'freq': freq, 'pos': pos, 'seed_prng': time()}
params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i2m2 = {'n_stim': 20, 'cell': 'pyramidal', 'section': 'soma', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_stim = {'kind': 'poisson_gen', 'onset': 0, 'tstop': tstop, 'dt': dt,
               'freq': freq, 'pos': pos, 'seed_prng': time()}
params_syn = {'kind': 'GABA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_i3m2 = {'n_stim': 10, 'cell': 'pyramidal', 'section': 'soma', 'params_stim': params_stim,
               'params_syn': params_syn, 'params_weight': params_weight}

params_m2 = [params_i1m2, params_i2m2, params_i3m2]

# parameters of the connections

# connection probabilities (prob = desired_n_inputs / n_presynaptic_neurons)
prob_p1p1_AMPA = 0.12  # / n_p1
prob_p1p1_NMDA = 0.03  # / n_p1
prob_p1m2_AMPA = 0.65   # 40 / n_p1
prob_p1m2_NMDA = 0.35  # 10 / n_p1
prob_p2p2_AMPA = 0.12  # / n_p2
prob_p2p2_NMDA = 0.03  # / n_p2
prob_p2m2_AMPA = 0.68  # 0 / n_p2
prob_p2m2_NMDA = 0.17  # 0 / n_p2
prob_m2p2_GABA = 0.79  # 32 / n_m2

# p1p1
params_p1p1 = [0]*2

params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_p1p1[0] = {'prob': prob_p1p1_AMPA, 'params_syn': params_syn, 'params_weight': params_weight, 'thresh': -20,
                  'delay': 1.1, 'seed_prng': time()}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_p1p1[1] = {'prob': prob_p1p1_NMDA, 'params_syn': params_syn, 'params_weight': params_weight, 'thresh': -20,
                  'delay': 1.1, 'seed_prng': time()}

# p1m2
params_p1m2 = [0]*2

params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_p1m2[0] = {'prob': prob_p1m2_AMPA, 'params_syn': params_syn, 'params_weight': params_weight, 'thresh': -20,
                  'delay': 1.1, 'seed_prng': time()}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_p1m2[1] = {'prob': prob_p1m2_NMDA, 'params_syn': params_syn, 'params_weight': params_weight, 'thresh': -20,
                  'delay': 1.1, 'seed_prng': time()}

# p2p2
params_p2p2 = [0]*2

params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_p2p2[0] = {'prob': prob_p2p2_AMPA, 'params_syn': params_syn, 'params_weight': params_weight, 'thresh': -20,
                  'delay': 1.1, 'seed_prng': time()}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_p2p2[1] = {'prob': prob_p2p2_NMDA, 'params_syn': params_syn, 'params_weight': params_weight, 'thresh': -20,
                  'delay': 1.1, 'seed_prng': time()}

# p2m2
params_p2m2 = [0]*2

params_syn = {'kind': 'AMPA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_p2m2[0] = {'prob': prob_p2m2_AMPA, 'params_syn': params_syn, 'params_weight': params_weight, 'thresh': -20,
                  'delay': 1.1, 'seed_prng': time()}

params_syn = {'kind': 'NMDA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_p2m2[1] = {'prob': prob_p2m2_NMDA, 'params_syn': params_syn, 'params_weight': params_weight, 'thresh': -20,
                  'delay': 1.1, 'seed_prng': time()}

# m2p2
params_m2p2 = [0]*1

params_syn = {'kind': 'GABA', 'pos': pos}
params_weight = {'kind': 'same', 'weight': 0.002}
params_m2p2[0] = {'prob': prob_m2p2_GABA, 'params_syn': params_syn, 'params_weight': params_weight, 'thresh': -20,
                  'delay': 1.1, 'seed_prng': time()}


# Create neurons with spatial arrangement
seed_positions = time()
prng = Random()  # pseudo random number generator
prng.seed(seed_positions)
x_p, y_p, z_p = get_positions(grid_size, sidelength, prng)
x_m, y_m, z_m = get_positions(grid_size, sidelength, prng)

# create first pyramidal cell population
pyrs1 = [0]* n_p1
x_p1 = [0]*np.size(x_p)
for i in np.arange(n_p1):
    x_p1[i] = x_p[i]+dist_areal
    pyrs1[i] = h.Pyramidal()
    pyrs1[i].position(x_p1[i], y_p[i], z_p[i]) # just shift first pyramidal cell population away

# create second pyramidal cell population
pyrs2 = [0]*(n_p2)
for i in np.arange(n_p2):
    pyrs2[i] = h.Pyramidal() 
    pyrs2[i].position(x_p[i], y_p[i], z_p[i])

# create martinotti cell population
mars2 = [0]*n_m2
for i in np.arange(n_m2):
    mars2[i] = h.Martinotti()
    mars2[i].position(x_m[i], y_m[i], z_m[i])


# save parameters

if not os.path.exists(folder):
    os.makedirs(folder)

# parameters
save_as_txt(folder, 'params', 'tstop: '+str(tstop)+'\n'+'dt: '+str(dt)+'\n'+'onset: '+str(onset)
            +'\n'+'n_trials: '+str(n_trials)+'\n'+'frequency: '+str(frequencies)
            +'\n'+'n_lflb_p1: '+str(n_lflb_p1)+'\n'+'n_lfhb_p1: '+str(n_lfhb_p1)+'\n'+'n_hfhb_p1: '+str(n_hfhb_p1)
            +'\n'+'n_lflb_p2: '+str(n_lflb_p2)+'\n'+'n_lfhb_p2: '+str(n_lfhb_p2)+'\n'+'n_hfhb_p2: '+str(n_hfhb_p2)
            +'\n'+'n_m2: '+str(n_m2)
            +'\n'+'params_lflb_p1: '+str(params_lflb_p1)+'\n'+'params_lfhb_p1: '+str(params_lfhb_p1)
            +'\n'+'params_hfhb_p1: '+str(params_hfhb_p1)
            +'\n'+'params_lflb_p2: '+str(params_lflb_p2)+'\n'+'params_lfhb_p1: '+str(params_lfhb_p2)
            +'\n'+'params_hfhb_p1: '+str(params_hfhb_p2)
            +'\n'+'params_m2: '+str(params_m2)
            +'\n'+'params_p1p1: '+str(params_p1p1)+'\n'+'params_p1m2: '+str(params_p1m2)
            +'\n'+'params_p2p2: '+str(params_p2p2)+'\n'+'params_p2m2: '+str(params_p2m2)
            +'\n'+'params_m2p2: '+str(params_m2p2)
            +'\n'+'prob_p1p1_AMPA: '+str(prob_p1p1_AMPA)+'\n'+'prob_p1p1_NMDA: '+str(prob_p1p1_NMDA)
            +'\n'+'prob_p1m2_AMPA: '+str(prob_p1m2_AMPA)+'\n'+'prob_p1m2_NMDA: '+str(prob_p1m2_NMDA)
            +'\n'+'prob_p2p2_AMPA: '+str(prob_p2p2_AMPA)+'\n'+'prob_p2p2_NMDA: '+str(prob_p2p2_NMDA)
            +'\n'+'prob_p2m2_AMPA: '+str(prob_p2m2_AMPA)+'\n'+'prob_p2m2_NMDA: '+str(prob_p2m2_NMDA)
            +'\n'+'prob_m2p2_GABA: '+str(prob_m2p2_GABA))

# parameter positioning
with open(folder+'seed_positions.json', 'w') as f:
    json.dump({'n': grid_size, 'sidelength': sidelength, 'seed_prng': seed_positions}, f)

# time
outfile = open(folder+'dt.npy', 'w')
np.save(outfile, dt)
outfile = open(folder+'tstop.npy', 'w')
np.save(outfile, tstop)
outfile = open(folder+'onset.npy', 'w')
np.save(outfile, onset)

# frequency
outfile = open(folder+'frequencies.npy', 'w')
np.save(outfile, frequencies)

# number of trials
outfile = open(folder+'n_trials.npy', 'w')
np.save(outfile, n_trials)

# number of cells
outfile = open(folder+'n_p1.npy', 'w')
np.save(outfile, n_p1)        
outfile = open(folder+'n_p2.npy', 'w')
np.save(outfile, n_p2)        
outfile = open(folder+'n_m2.npy', 'w')
np.save(outfile, n_m2)

# connection parameters
with open(folder+'params_lflb_p1.json', 'w') as f:
    json.dump(params_lflb_p1, f)
with open(folder+'params_lfhb_p1.json', 'w') as f:
    json.dump(params_lfhb_p1, f)
with open(folder+'params_hfhb_p1.json', 'w') as f:
    json.dump(params_hfhb_p1, f)
with open(folder+'params_lflb_p2.json', 'w') as f:
    json.dump(params_lflb_p2, f)
with open(folder+'params_lfhb_p2.json', 'w') as f:
    json.dump(params_lfhb_p2, f)
with open(folder+'params_hfhb_p2.json', 'w') as f:
    json.dump(params_hfhb_p2, f)
with open(folder+'params_m2.json', 'w') as f:
    json.dump(params_m2, f)
with open(folder+'params_p1p1.json', 'w') as f:
    json.dump(params_p1p1, f)
with open(folder+'params_p1m2.json', 'w') as f:
    json.dump(params_p1m2, f)
with open(folder+'params_p2p2.json', 'w') as f:
    json.dump(params_p2p2, f)
with open(folder+'params_p2m2.json', 'w') as f:
    json.dump(params_p2m2, f)
with open(folder+'params_m2p2.json', 'w') as f:
    json.dump(params_m2p2, f)

# create connections

# pyramidal 1 --> pyramidal 1 dend
pre = [p.soma for p in pyrs1]
post = [p.dend for p in pyrs1]

for params in params_p1p1: syn_p1p1, con_p1p1, weights_p1p1, connections_p1p1 = gen_con_rand(pre, post, params)

# pyramidal 1 --> martinotti 2
pre = [p.soma for p in pyrs1]
post = [m.soma for m in mars2]
    
for params in params_p1m2: syn_p1m2, con_p1m2, weights_p1m2, connections_p1m2 = gen_con_rand(pre, post, params)

# pyramidal 2 --> pyramidal 2
pre = [p.soma for p in pyrs2]
post = [p.dend for p in pyrs2]

for params in params_p2p2: syn_p2p2, con_p2p2, weights_p2p2, connections_p2p2 = gen_con_rand(pre, post, params)

# pyramidal 2 --> martinotti 2
pre = [p.soma for p in pyrs2]
post = [m.soma for m in mars2]

for params in params_p2m2: syn_p2m2, con_p2m2, weights_p2m2, connections_p2m2 = gen_con_rand(pre, post, params)

# martinotti 2 --> pyramidal 2
pre = [m.soma for m in mars2]
post = [p.tuft for p in pyrs2]

for params in params_m2p2: syn_m2p2, con_m2p2, weights_m2p2, connections_m2p2 = gen_con_rand(pre, post, params)

# save connections
connections = [connections_p1p1, connections_p1m2, connections_p2p2, connections_p2m2,
               connections_m2p2]
with open(folder+'connections.npy', 'w') as file:
    np.save(file, connections)

# recordings

# membrane potential p1 
vec_v_p1 = [[]]*len(pyrs1)
vec_v_tuft_p1 = [[]]*len(pyrs1)
for i in np.arange(len(pyrs1)):      
    vec_v_p1[i] = rec(pyrs1[i].soma, 'v')
    vec_v_tuft_p1[i] = rec(pyrs1[i].tuft, 'v')

# membrane potential p2 
vec_v_p2 = [[]]*len(pyrs2)
vec_v_tuft_p2 = [[]]*len(pyrs2)
for i in np.arange(len(pyrs2)): 
    vec_v_p2[i] = rec(pyrs2[i].soma, 'v')
    vec_v_tuft_p2[i] = rec(pyrs2[i].tuft, 'v')

# membrane potential m2
vec_v_m2 = [[]]*len(mars2)
for i in np.arange(len(mars2)): 
    vec_v_m2[i] = rec(mars2[i].soma, 'v')

# spiketimes p1
vec_APs_p1 = [0]*len(pyrs1)
APcount_p1 = [0]*len(pyrs1)
for i in np.arange(len(pyrs1)):
    vec_APs_p1[i], APcount_p1[i] = rec_APs(pyrs1[i].soma)

# spiketimes p2
vec_APs_p2 = [0]*len(pyrs2)
APcount_p2 = [0]*len(pyrs2)
for i in np.arange(len(pyrs2)):
    vec_APs_p2[i], APcount_p2[i] = rec_APs(pyrs2[i].soma)

# spiketimes m2
vec_APs_m2 = [0]*len(mars2)
APcount_m2 = [0]*len(mars2)
for i in np.arange(len(mars2)):
    vec_APs_m2[i], APcount_m2[i] = rec_APs(mars2[i].soma)

# extracellular recording
h.load_file(1, "../../recording/LFP/extracell_rec.hoc")
h.setelec(grid_size*sidelength/2, grid_size*sidelength/2, grid_size*sidelength/2)  # middle of area 2
h.setelec(0, 0, 0)
vec_vrec = h.Vector()
vec_vrec.record(h._ref_vrec)


for trial in np.arange(n_trials):
    # insert random inputs
    # inputs to p1
    syn_ip1 = np.zeros([n_p1, np.size(params_lflb_p1)], dtype=object)
    stim_ip1 = np.zeros([n_p1, np.size(params_lflb_p1)], dtype=object)
    con_ip1 = np.zeros([n_p1, np.size(params_lflb_p1)], dtype=object)
    weights_ip1 = np.zeros([n_p1, np.size(params_lflb_p1)], dtype=object)
    spiketimes_ip1 = np.zeros([n_p1, np.size(params_lflb_p1)], dtype=object)

    for i in range(0, n_lflb_p1):
        for j, params in enumerate(params_lflb_p1):
            params['cell'] = pyrs1[i]
            syn_ip1[i, j], stim_ip1[i, j], con_ip1[i, j], weights_ip1[i, j], spiketimes_ip1[i, j] = synaptic_input(**params)

    for i in range(n_lflb_p1, n_lflb_p1+n_lfhb_p1):
        for j, params in enumerate(params_lfhb_p1):
            params['cell'] = pyrs1[i]
            syn_ip1[i, j], stim_ip1[i, j], con_ip1[i, j], weights_ip1[i, j], spiketimes_ip1[i, j] = synaptic_input(**params)

    for i in range(n_lfhb_p1+n_lflb_p1, n_lflb_p1+n_lfhb_p1+n_hfhb_p1):
        for j, params in enumerate(params_hfhb_p1):
            params['cell'] = pyrs1[i]
            syn_ip1[i, j], stim_ip1[i, j], con_ip1[i, j], weights_ip1[i, j], spiketimes_ip1[i, j] = synaptic_input(**params)


    # inputs to p2
    syn_ip2 = np.zeros([n_p2, np.size(params_lflb_p2)], dtype=object)
    stim_ip2 = np.zeros([n_p2, np.size(params_lflb_p2)], dtype=object)
    con_ip2 = np.zeros([n_p2, np.size(params_lflb_p2)], dtype=object)
    weights_ip2 = np.zeros([n_p2, np.size(params_lflb_p2)], dtype=object)
    spiketimes_ip2 = np.zeros([n_p2, np.size(params_lflb_p2)], dtype=object)

    for i in range(0, n_lflb_p2):
        for j, params in enumerate(params_lflb_p2):
            params['cell'] = pyrs2[i]
            syn_ip2[i, j], stim_ip2[i, j], con_ip2[i, j], weights_ip2[i, j], spiketimes_ip2[i, j] = synaptic_input(**params)

    for i in range(n_lflb_p2, n_lflb_p2+n_lfhb_p2):
        for j, params in enumerate(params_lfhb_p2):
            params['cell'] = pyrs2[i]
            syn_ip2[i, j], stim_ip2[i, j], con_ip2[i, j], weights_ip2[i, j], spiketimes_ip2[i, j] = synaptic_input(**params)

    for i in range(n_lfhb_p2+n_lflb_p2, n_lflb_p2+n_lfhb_p2+n_hfhb_p2):
        for j, params in enumerate(params_hfhb_p2):
            params['cell'] = pyrs2[i]
            syn_ip2[i, j], stim_ip2[i, j], con_ip2[i, j], weights_ip2[i, j], spiketimes_ip2[i, j] = synaptic_input(**params)

    # inputs to m2
    syn_im2 = np.zeros([n_m2, np.size(params_m2)], dtype=object)
    stim_im2 = np.zeros([n_m2, np.size(params_m2)], dtype=object)
    con_im2 = np.zeros([n_m2, np.size(params_m2)], dtype=object)
    weights_im2 = np.zeros([n_m2, np.size(params_m2)], dtype=object)
    spiketimes_im2 = np.zeros([n_m2, np.size(params_m2)], dtype=object)

    for i, cell in enumerate(mars2):
        for j, params in enumerate(params_m2):
            params['cell'] = cell
            syn_im2[i, j], stim_im2[i, j], con_im2[i, j], weights_im2[i, j], spiketimes_im2[i, j] = synaptic_input(**params)
 
    # Run
    start_time = time()  # measure time it takes to run
    h.tstop = tstop + onset
    h.steps_per_ms = 1 / dt
    h.dt = dt
    h.v_init = -70
    h.init()
    h.run()
    print "trial: " + str(trial)
    print "time to run (s): " + str(time.time() - start_time)

    # Convert to arrays and cut off onset    
    vrec = np.array(vec_vrec)[onset/dt:]
   
    APs_p1 = [[]]*len(pyrs1)
    APs_p2 = [[]]*len(pyrs2)
    APs_m2 = [[]]*len(mars2)
    
    for i, APs in enumerate(vec_APs_p1):
        APs = np.array(APs)
        if APs.size > 0:
            APs = APs[APs > onset]
            APs = APs[APs <= tstop+onset]
            APs_p1[i] = APs - onset

    for i,APs in enumerate(vec_APs_p2):
        APs = np.array(APs)
        if APs.size > 0:
            APs = APs[APs > onset]
            APs = APs[APs <= tstop+onset]
            APs_p2[i] = APs - onset
    
    for i,APs in enumerate(vec_APs_m2):
        APs = np.array(APs)
        if APs.size > 0:
            APs = APs[APs > onset]
            APs = APs[APs <= tstop+onset]
            APs_m2[i] = APs - onset

    v_p1 = [[]]*len(pyrs1)
    v_tuft_p1 = [[]]*len(pyrs1)
    v_p2 = [[]]*len(pyrs2)
    v_tuft_p2 = [[]]*len(pyrs2)
    v_m2 = [[]]*len(mars2)
    
    for i, v in enumerate(vec_v_p1):
        v_p1[i] = np.array(v)[onset/dt:]
    
    for i, v in enumerate(vec_v_tuft_p1):
        v_tuft_p1[i] = np.array(v)[onset/dt:]

    for i, v in enumerate(vec_v_p2):
        v_p2[i] = np.array(v)[onset/dt:]
        
    for i, v in enumerate(vec_v_tuft_p2):
        v_tuft_p2[i] = np.array(v)[onset/dt:]
    
    for i, v in enumerate(vec_v_m2):
        v_m2[i] = np.array(v)[onset/dt:]

    # Save variables
    folder_sav = folder+'trial'+str(trial)+'/'
    if not os.path.exists(folder_sav): os.makedirs(folder_sav)

    # APs
    outfile = open(folder_sav+'APs_p1.npy', 'w')
    np.save(outfile, APs_p1)
    outfile = open(folder_sav+'APs_p2.npy', 'w')
    np.save(outfile, APs_p2)
    outfile = open(folder_sav+'APs_m2.npy', 'w')
    np.save(outfile, APs_m2)

    # extracellular recording
    outfile = open(folder_sav+'vrec.npy', 'w')
    np.save(outfile, vrec)

    # membrane potential
    outfile = open(folder_sav+'v_p1.npy', 'w')
    np.save(outfile, v_p1)
    outfile = open(folder_sav+'v_tuft_p1.npy', 'w')
    np.save(outfile, v_tuft_p1)
    outfile = open(folder_sav+'v_p2.npy', 'w')
    np.save(outfile, v_p2)
    outfile = open(folder_sav+'v_tuft_p2.npy', 'w')
    np.save(outfile, v_tuft_p2)
    outfile = open(folder_sav+'v_m2.npy', 'w')
    np.save(outfile, v_m2)

    # spiketimes
    for i, cell in enumerate(pyrs1):
        for j in range(len(params_lflb_p1)):
            spiketimes_ip1[i, j] = [st.to_python() for st in spiketimes_ip1[i, j]]
    outfile = open(folder+'/spiketimes_ip1.npy', 'w')
    np.save(outfile, spiketimes_ip1)

    for i, cell in enumerate(pyrs2):
        for j in range(len(params_lflb_p2)):
            spiketimes_ip2[i, j] = [st.to_python() for st in spiketimes_ip2[i, j]]
    outfile = open(folder+'/spiketimes_ip2.npy', 'w')
    np.save(outfile, spiketimes_ip2)

    for i, cell in enumerate(mars2):
        for j, params in enumerate(params_m2):
            spiketimes_im2[i, j] = [st.to_python() for st in spiketimes_im2[i, j]]
    outfile = open(folder+'/spiketimes_im2.npy', 'w')
    np.save(outfile, spiketimes_im2)


# Evaluation

n = [0, n_lflb_p1, n_lfhb_p1, n_hfhb_p1]
for i in range(2, len(n)):
    fr = np.zeros(n[i])
    BAC_percent = np.zeros(n[i])
    burst_percent = np.zeros(n[i])

    for j in range(np.sum(n[:i-1]), np.sum(n[:i])-1):

        # firing rate
        fr[j] = np.size(APs_p1[j]) / (tstop/1000)

        # percent burst
        burst_len = 10
        BAC_percent[j], FAC_percent, other_burst_percent, burst_percent[j] = functions.percentage_burst(APs_p1[j], v_tuft_p1[j],
                                                                                              burst_len, dt)
    print 'mean firing rate (p1 group '+str(i)+'): '
    print np.mean(fr)
    print 'mean BAC percent, burst percent (p1 group '+str(i)+'): '
    print np.mean(BAC_percent), np.mean(burst_percent)

n = [0, n_lflb_p2, n_lfhb_p2, n_hfhb_p2]
for i in range(2, len(n)):
    fr = np.zeros(n[i])
    BAC_percent = np.zeros(n[i])
    burst_percent = np.zeros(n[i])

    for j in range(np.sum(n[:i-1]), np.sum(n[:i])-1):

        # firing rate
        fr[j] = np.size(APs_p2[j]) / (tstop/1000)

        # percent burst
        burst_len = 10
        BAC_percent[j], FAC_percent, other_burst_percent, burst_percent[j] = functions.percentage_burst(APs_p2[j], v_tuft_p2[j],
                                                                                              burst_len, dt)
    print 'mean firing rate (p2 '+str(i)+'): '
    print np.mean(fr)
    print 'mean BAC percent, burst percent (p2'+str(i)+'): '
    print np.mean(BAC_percent), np.mean(burst_percent)


v_p1 = np.array(vec_v_p1[0])[onset/h.dt:]
v_tuft_p1 = np.array(vec_v_tuft_p1[0])[onset/h.dt:]
v_p2 = np.array(vec_v_p2[0])[onset/h.dt:]
v_tuft_p2 = np.array(vec_v_tuft_p2[0])[onset/h.dt:]
v_m2 = np.array(vec_v_m2[0])[onset/h.dt:]

t = np.arange(0, tstop+dt, dt)

# Plot: membrane potential single neurons
pl.figure(1)
pl.plot(t, v_p1, 'k', label='soma')
pl.plot(t, v_tuft_p1, 'r', label='tuft')
pl.legend(loc='upper right', prop={'size':12})
pl.ylabel('Membrane potential (mV)')
pl.xlabel('Time (ms)')
pl.title('P1')
pl.xlim([0, 2000])
pl.show()

pl.figure(2)
pl.plot(t, v_p2, 'k', label='soma')
pl.plot(t, v_tuft_p2, 'r', label='tuft')
pl.legend(loc='upper right', prop={'size':12})
pl.ylabel('Membrane potential (mV)')
pl.xlabel('Time (ms)')
pl.title('P2')
pl.xlim([0, 2000])

pl.figure(3)
pl.plot(t, v_m2, 'k', label='soma')
pl.legend(loc='upper right',prop={'size':12})
pl.ylabel('Membrane potential (mV)')
pl.xlabel('Time (ms)')
pl.title('M2')
pl.xlim([0, 2000])

# Raster plots
t = np.arange(0,tstop,dt)

# raster plot p1
fig, ax = pl.subplots(1)
for i in np.arange(0, len(APs_p1)):
    pl.scatter(APs_p1[i], i * np.ones(len(APs_p1[i])), s=1, color='k')
pl.ylabel('# Neuron')
pl.xlabel('Time (ms)')
pl.title('P1')
pl.ylim([0,n_p1])
pl.xlim(0, 2000)
pl.show()

# raster plot p2
fig, ax = pl.subplots(1)
for i in np.arange(0, len(APs_p2)):
    pl.scatter(APs_p2[i], i * np.ones(len(APs_p2[i])), s=1, color='k')
    pl.ylabel('# Neuron')
pl.xlabel('Time (ms)')
pl.title('P2')
pl.ylim([0,n_p2])
pl.xlim(0, 2000)
pl.show()

# raster plot m2
fig, ax = pl.subplots(1)
for i in np.arange(0, len(APs_m2)):
    pl.scatter(APs_m2[i], i * np.ones(len(APs_m2[i])), s=1, color='r')
pl.ylabel('# Neuron')
pl.xlabel('Time (ms)')
pl.title('M2')
pl.ylim([0,n_m2])
pl.xlim(0, 2000)
pl.show()

# oscillatory inhibitory input to p1
fig, ax = pl.subplots(1)
for i in np.arange(0,len(APs_p1)):
    pl.scatter(spiketimes_ip1[i,5][0],i * np.ones(len(spiketimes_ip1[i,5][0])), s=1, color='k')
pl.ylabel('# Neuron')
pl.xlabel('Time (ms)')
pl.ylim([0,n_p1])
pl.xlim(0, 1000)

# raster plot p1
fig, ax = pl.subplots(1)
for i in np.arange(0,len(APs_p1)):
    pl.scatter(APs_p1[i],i * np.ones(len(APs_p1[i])), s=1, color='k')
pl.ylabel('# Neuron')
pl.xlabel('Time (ms)')
pl.ylim([0,n_p1])
pl.xlim(0, 1000)
pl.show()


