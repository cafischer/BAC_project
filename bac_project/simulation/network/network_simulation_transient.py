from __future__ import division
import numpy as np
import pylab as pl
from neuron import h
import os
from connectivity.connection import synaptic_input, synaptic_input_fromfile, gen_con_rand
from spatial_organization.spatial_placement import get_positions
from recording.record import rec, rec_APs
from general_functions.saving import save_as_txt
from analyses import functions
import time

# load NEURON libraries
h.load_file("stdrun.hoc")
h("""cvode.active(0)""") # unvariable time step
h.nrn_load_dll("../../model/channels/x86_64/.libs/libnrnmech.so")

# import synapse models
h.nrn_load_dll("../../connectivity/synapse_models/x86_64/.libs/libnrnmech.so")

# folder to save
folder = 'data/'+'transient_test2'+'/'

# cell models
h.load_file(1, "../../model/models/Pyramidal_reclfp.hoc")
h.load_file(1, "../../model/models/Martinotti_fast.hoc") 

# simulation parameters
transient = 2000
tstop = 2000 # ms
dt = 0.25
onset = 200 # ms
n_trials = 10

# frequency of the oscillation
f = 8

# network parameters
n_p1 = 80 
n_p2 = 80
n_m2 = 20 
dist = 5 # um
grid_size = 10 # grid size needs to be greater than ceil(sqrt(n_cells))
dist_areal = 1000

# inputs to p1
freq = 10
pos = 0.5

params_stim = {'kind':'poisson', 'onset':onset, 'tstop':tstop, 'freq': freq, 'start':0, 'noise':1, 'pos':pos}
params_syn = {'kind':'AMPA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.00035, 'std':0.00017} 
params_i1p1 = {'n_stim':100, 'cell':'pyramidal', 'section':'dend', 'params_stim':params_stim, 'params_syn':params_syn, 'params_weight':params_weight}

params_stim = {'kind':'poisson', 'onset':onset, 'tstop':tstop, 'freq': freq, 'start':0, 'noise':1, 'pos':pos}
params_syn = {'kind':'NMDA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.005, 'std':0.0025} 
params_i2p1 = {'n_stim':100, 'cell':'pyramidal', 'section':'dend', 'params_stim':params_stim, 'params_syn':params_syn, 'params_weight':params_weight}

params_stim = {'kind':'poisson', 'onset':onset, 'tstop':tstop, 'freq': freq, 'start':0, 'noise':1, 'pos':pos}
params_syn = {'kind':'AMPA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.00035, 'std':0.00017} 
params_i3p1 = {'n_stim':100, 'cell':'pyramidal', 'section':'tuft', 'params_stim':params_stim, 'params_syn':params_syn, 'params_weight':params_weight}

params_stim = {'kind':'poisson', 'onset':onset, 'tstop':tstop, 'freq': freq, 'start':0, 'noise':1, 'pos':pos}
params_syn = {'kind':'NMDA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.005, 'std':0.0025} 
params_i4p1 = {'n_stim':100, 'cell':'pyramidal', 'section':'tuft', 'params_stim':params_stim, 'params_syn':params_syn, 'params_weight':params_weight}

params_stim = {'kind':'poisson', 'onset':onset, 'tstop':tstop, 'freq': freq, 'start':0, 'noise':1, 'pos':pos}
params_syn = {'kind':'GABA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.005, 'std':0.0025} 
params_i5p1 = {'n_stim':10, 'cell':'pyramidal', 'section':'soma', 'params_stim':params_stim, 'params_syn':params_syn, 'params_weight':params_weight}

params_stim = {'kind':'transient_osc','freq_osc':f, 'freq':freq, 'onset':onset, 'tstop':tstop, 'transient':transient, 'dt':dt, 'pos':pos}
params_syn = {'kind':'GABA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.005, 'std':0.0025} 
params_i6p1 = {'n_stim':100, 'cell':'pyramidal', 'section':'tuft', 'params_stim':params_stim, 'params_syn':params_syn, 'params_weight':params_weight}

params_p1 = [params_i1p1, params_i2p1, params_i3p1, params_i4p1, params_i5p1, params_i6p1]

# inputs to p2
params_stim = {'kind':'poisson', 'onset':onset, 'tstop':tstop, 'freq': freq, 'start':0, 'noise':1, 'pos':pos}
params_syn = {'kind':'AMPA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.00035, 'std':0.00017} 
params_i1p2 = {'n_stim':80, 'cell':'pyramidal', 'section':'dend', 'params_stim':params_stim, 'params_syn':params_syn, 'params_weight':params_weight}
 
params_stim = {'kind':'poisson', 'onset':onset, 'tstop':tstop, 'freq': freq, 'start':0, 'noise':1, 'pos':pos}
params_syn = {'kind':'NMDA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.005, 'std':0.0025} 
params_i2p2 = {'n_stim':80, 'cell':'pyramidal', 'section':'dend', 'params_stim':params_stim, 'params_syn':params_syn, 'params_weight':params_weight}

params_stim = {'kind':'poisson', 'onset':onset, 'tstop':tstop, 'freq': freq, 'start':0, 'noise':1, 'pos':pos}
params_syn = {'kind':'AMPA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.00035, 'std':0.00017} 
params_i3p2 = {'n_stim':80, 'cell':'pyramidal', 'section':'tuft', 'params_stim':params_stim, 'params_syn':params_syn, 'params_weight':params_weight}

params_stim = {'kind':'poisson', 'onset':onset, 'tstop':tstop, 'freq': freq, 'start':0, 'noise':1, 'pos':pos}
params_syn = {'kind':'NMDA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.005, 'std':0.0025} 
params_i4p2 = {'n_stim':80, 'cell':'pyramidal', 'section':'tuft', 'params_stim':params_stim, 'params_syn':params_syn, 'params_weight':params_weight}

params_stim = {'kind':'poisson', 'onset':onset, 'tstop':tstop, 'freq': freq, 'start':0, 'noise':1, 'pos':pos}
params_syn = {'kind':'GABA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.005, 'std':0.0025}
params_i5p2 = {'n_stim':20, 'cell':'pyramidal', 'section':'soma', 'params_stim':params_stim, 'params_syn':params_syn, 'params_weight':params_weight}

params_p2 = [params_i1p2, params_i2p2, params_i3p2, params_i4p2, params_i5p2]

# inputs to m2
params_stim = {'kind':'poisson', 'onset':onset, 'tstop':tstop, 'freq': freq, 'start':0, 'noise':1, 'pos':pos}
params_syn = {'kind':'AMPA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.00035, 'std':0.00017}
params_i1m2 = {'n_stim':20, 'cell':'martinotti', 'section':'soma', 'params_stim':params_stim, 'params_syn':params_syn, 'params_weight':params_weight}

params_stim = {'kind':'poisson', 'onset':onset, 'tstop':tstop, 'freq': freq, 'start':0, 'noise':1, 'pos':pos}
params_syn = {'kind':'NMDA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.005, 'std':0.0025}  
params_i2m2 = {'n_stim':20, 'cell':'martinotti', 'section':'soma', 'params_stim':params_stim, 'params_syn':params_syn, 'params_weight':params_weight}

params_stim = {'kind':'poisson', 'onset':onset, 'tstop':tstop, 'freq': freq, 'start':0, 'noise':1, 'pos':pos}
params_syn = {'kind':'GABA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.005, 'std':0.0025}
params_i3m2 = {'n_stim':50, 'cell':'martinotti', 'section':'soma', 'params_stim':params_stim, 'params_syn':params_syn, 'params_weight':params_weight}

params_m2 = [params_i1m2, params_i2m2, params_i3m2]

# parameters of the connections

# connection probabilities (prob = desired_n_inputs / n_presynaptic_neurons)
prob_p1p1 = 10 / n_p1
prob_p1p2 = 5 / n_p1 
prob_p1m2 = 40 / n_p1
prob_p2p2 = 10 / n_p2 
prob_p2m2 = 10 / n_p2 
prob_m2p2 = 20 / n_m2 

# p1p1
params_p1p1 = [0]*2

params_syn = {'kind':'AMPA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.00035, 'std':0.00017}  
params_p1p1[0] = {'params_syn':params_syn, 'params_weight':params_weight, 'thresh':-20, 'delay':1.1}

params_syn = {'kind':'NMDA' ,'pos':pos} 
params_weight = {'kind':'gaussian', 'mean':0.005, 'std':0.0025} 
params_p1p1[1] = {'params_syn':params_syn, 'params_weight':params_weight, 'thresh':-20, 'delay':1.1}

# p1p2
params_p1p2 = [0]*2

params_syn = {'kind':'AMPA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.00035, 'std':0.00017}  
params_p1p2[0] = {'params_syn':params_syn, 'params_weight':params_weight, 'thresh':-20, 'delay':1.1}

params_syn = {'kind':'NMDA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.005, 'std':0.0025} 
params_p1p2[1] = {'params_syn':params_syn, 'params_weight':params_weight, 'thresh':-20, 'delay':1.1}

# p1m2
params_p1m2 = [0]*2

params_syn = {'kind':'AMPA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.00035, 'std':0.00017}  
params_p1m2[0] = {'params_syn':params_syn, 'params_weight':params_weight, 'thresh':-20, 'delay':1.1}

params_syn = {'kind':'NMDA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.005, 'std':0.0025} 
params_p1m2[1] = {'params_syn':params_syn, 'params_weight':params_weight, 'thresh':-20, 'delay':1.1}

# p2p2
params_p2p2 = [0]*2

params_syn = {'kind':'AMPA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.00035, 'std':0.00017}  
params_p2p2[0] = {'params_syn':params_syn, 'params_weight':params_weight, 'thresh':-20, 'delay':1.1}

params_syn = {'kind':'NMDA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.005, 'std':0.0025} 
params_p2p2[1] = {'params_syn':params_syn, 'params_weight':params_weight, 'thresh':-20, 'delay':1.1}

# p2m2
params_p2m2 = [0]*2

params_syn = {'kind':'AMPA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.00035, 'std':0.00017}  
params_p2m2[0] = {'params_syn':params_syn, 'params_weight':params_weight, 'thresh':-20, 'delay':1.1}

params_syn = {'kind':'NMDA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.005, 'std':0.0025} 
params_p2m2[1] = {'params_syn':params_syn, 'params_weight':params_weight, 'thresh':-20, 'delay':1.1}

# m2p2
params_m2p2 = [0]*1

params_syn = {'kind':'GABA' ,'pos':pos}
params_weight = {'kind':'gaussian', 'mean':0.008, 'std':0.0025}  
params_m2p2[0] = {'params_syn':params_syn, 'params_weight':params_weight, 'thresh':-20, 'delay':1.1}

# <codecell>

# Create neurons with spatial arrangement

x_p, y_p, z_p = get_positions(grid_size, dist)
x_m, y_m, z_m = get_positions(grid_size, dist)

# create first pyramidal cell population
pyrs1 = [0]*n_p1
x_p1 = [0]*np.size(x_p)

for i in np.arange(n_p1):
    x_p1[i] = x_p[i]+dist_areal
    pyrs1[i] = h.Pyramidal() 
    pyrs1[i].position(x_p1[i],y_p[i],z_p[i]) # just shift first pyramidal cell population away

# create second pyramidal cell population
pyrs2 = [0]*n_p2
for i in np.arange(n_p2):
    pyrs2[i] = h.Pyramidal() 
    pyrs2[i].position(x_p[i],y_p[i],z_p[i]) 

# create martinotti cell population
mars2 = [0]*n_m2
for i in np.arange(n_m2): 
    mars2[i] = h.Martinotti() 
    mars2[i].position(x_m[i],y_m[i],z_m[i])

# <codecell>

# save parameters

if not os.path.exists(folder):
    os.makedirs(folder)

# parameters
save_as_txt(folder,'params', 'tstop: '+str(tstop)+'\n'+'dt: '+str(dt)+'\n'+'onset: '+str(onset)
            +'\n'+'n_trials: '+str(n_trials)+'\n'+'frequency: '+str(f)
            +'\n'+'n_p1: '+str(n_p1)+'\n'+'n_p2: '+str(n_p2)+'\n'+'n_m2: '+str(n_m2)
            +'\n'+'dist: '+str(dist)+'\n'+'grid_size: '+str(grid_size)
            +'\n'+'params_p1: '+str(params_p1)+'\n'+'params_p2: '+str(params_p2)+'\n'+'params_m2: '+str(params_m2)
            +'\n'+'params_p1p1: '+str(params_p1p1)+'\n'+'params_p1p2: '+str(params_p1p2)
            +'\n'+'params_p1m2: '+str(params_p1m2)+'\n'+'params_p2p2: '+str(params_p2p2)
            +'\n'+'params_p2m2: '+str(params_p2m2)+'\n'+'params_m2p2: '+str(params_m2p2)
            +'\n'+'prob_con_p1p1: '+str(prob_p1p1)+'\n'+'prob_con_p1p2: '+str(prob_p1p2)
            +'\n'+'prob_con_p1m2: '+str(prob_p1m2)+'\n'+'prob_con_p2p2: '+str(prob_p2p2)
            +'\n'+'prob_con_p2m2: '+str(prob_p2m2)+'\n'+'prob_con_m2p2: '+str(prob_m2p2))

# time
outfile = open(folder+'dt.npy', 'w')
np.save(outfile, dt)
outfile = open(folder+'tstop.npy', 'w')
np.save(outfile, tstop)
outfile = open(folder+'onset.npy', 'w')
np.save(outfile, onset)

# frequency
outfile = open(folder+'f.npy', 'w')
np.save(outfile, f)

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

# spatial arrangement
outfile = open(folder+'positions_p1.npy', 'w')
np.save(outfile, [x_p1, y_p, z_p])        
outfile = open(folder+'positions_p2.npy', 'w')
np.save(outfile, [x_p, y_p, z_p])        
outfile = open(folder+'positions_m2.npy', 'w')
np.save(outfile, [x_m, y_m, z_m])

# connection parameters
outfile = open(folder+'params_p1.npy', 'w')
np.save(outfile, params_p1) 
outfile = open(folder+'params_p2.npy', 'w')
np.save(outfile, params_p2)
outfile = open(folder+'params_m2.npy', 'w')
np.save(outfile, params_m2)
outfile = open(folder+'params_p1p1.npy', 'w')
np.save(outfile, params_p1p1)
outfile = open(folder+'params_p1p2.npy', 'w')
np.save(outfile, params_p1p2)
outfile = open(folder+'params_p1m2.npy', 'w')
np.save(outfile, params_p1m2)
outfile = open(folder+'params_p2p2.npy', 'w')
np.save(outfile, params_p2p2)
outfile = open(folder+'params_p2m2.npy', 'w')
np.save(outfile, params_p2m2)
outfile = open(folder+'params_m2p2.npy', 'w')
np.save(outfile, params_m2p2)

# <codecell>

# create connections

# inputs to p1
syn_ip1 = np.zeros([n_p1, np.size(params_p1)], dtype=object)
stim_ip1 = np.zeros([n_p1, np.size(params_p1)], dtype=object)
con_ip1 = np.zeros([n_p1, np.size(params_p1)], dtype=object)
weights_ip1 = np.zeros([n_p1, np.size(params_p1)], dtype=object)
spiketimes_ip1 = np.zeros([n_p1, np.size(params_p1)], dtype=object)

for i, cell in enumerate(pyrs1):
    for j, params in enumerate(params_p1):
        params['cell'] = cell 
        syn_ip1[i,j], stim_ip1[i,j], con_ip1[i,j], weights_ip1[i,j], spiketimes_ip1[i,j] = synaptic_input(**params) 

# inputs to p2
syn_ip2 = np.zeros([n_p2, np.size(params_p2)], dtype=object)
stim_ip2 = np.zeros([n_p2, np.size(params_p2)], dtype=object)
con_ip2 = np.zeros([n_p2, np.size(params_p2)], dtype=object)
weights_ip2 = np.zeros([n_p2, np.size(params_p2)], dtype=object)

for i, cell in enumerate(pyrs2):
    for j, params in enumerate(params_p2):
        params['cell'] = cell
        syn_ip2[i,j], stim_ip2[i,j], con_ip2[i,j], weights_ip2[i,j], _ = synaptic_input(**params)
    
# inputs to m2
syn_im2 = np.zeros([n_m2, np.size(params_m2)], dtype=object)
stim_im2 = np.zeros([n_m2, np.size(params_m2)], dtype=object)
con_im2 = np.zeros([n_m2, np.size(params_m2)], dtype=object)
weights_im2 = np.zeros([n_m2, np.size(params_m2)], dtype=object)

for i, cell in enumerate(mars2):
    for j, params in enumerate(params_m2):
        params['cell'] = cell
        syn_im2[i,j], stim_im2[i,j], con_im2[i,j], weights_im2[i,j], _ = synaptic_input(**params)
    

# pyramidal 1 --> pyramidal 1 dend
pre = [p.soma for p in pyrs1]
post = [p.dend for p in pyrs1]

for params in params_p1p1: syn_p1p1, con_p1p1, weights_p1p1 = gen_con_rand(prob_p1p1, pre, post, params)

# pyramidal 1 --> pyramidal 2 tuft
pre = [p.soma for p in pyrs1]
post = [p.tuft for p in pyrs2]
    
for params in params_p1p2: syn_p1p2, con_p1p2, weights_p1p2 = gen_con_rand(prob_p1p2, pre, post, params)

# pyramidal 1 --> martinotti 2
pre = [p.soma for p in pyrs1]
post = [m.soma for m in mars2]
    
for params in params_p1m2: syn_p1m2, con_p1m2, weights_p1m2 = gen_con_rand(prob_p1m2, pre, post, params)

# pyramidal 2 --> pyramidal 2
pre = [p.soma for p in pyrs2]
post = [p.dend for p in pyrs2]

for params in params_p2p2: syn_p2p2, con_p2p2, weights_p2p2 = gen_con_rand(prob_p2p2, pre, post, params)

# pyramidal 2 --> martinotti 2
pre = [p.soma for p in pyrs2]
post = [m.soma for m in mars2]

for params in params_p2m2: syn_p2m2, con_p2m2, weights_p2m2 = gen_con_rand(prob_p2m2, pre, post, params)
    
# martinotti 2 --> pyramidal 2
pre = [m.soma for m in mars2]
post = [p.tuft for p in pyrs2]

for params in params_m2p2: syn_m2p2, con_m2p2, weights_m2p2 = gen_con_rand(prob_m2p2, pre, post, params)

# <codecell>

# recordings

# membrane potential p1 
vec_v_p1 = [[]]*len(pyrs1)
vec_v_tuft_p1 = [[]]*len(pyrs1)
for i in np.arange(len(pyrs1)):      
    vec_v_p1[i] = rec(pyrs1[i].soma(0.5)._ref_v)
    vec_v_tuft_p1[i] = rec(pyrs1[i].tuft(0.5)._ref_v)

# membrane potential p2 
vec_v_p2 = [[]]*len(pyrs2)
vec_v_tuft_p2 = [[]]*len(pyrs2)
for i in np.arange(len(pyrs2)): 
    vec_v_p2[i] = rec(pyrs2[i].soma(0.5)._ref_v)
    vec_v_tuft_p2[i] = rec(pyrs2[i].tuft(0.5)._ref_v)

# membrane potential m2
vec_v_m2 = [[]]*len(mars2)
for i in np.arange(len(mars2)): 
    vec_v_m2[i] = rec(mars2[i].soma(0.5)._ref_v)

# spiketimes p1
vec_APs_p1 = [[]]*len(pyrs1)
APcount_p1 = [[]]*len(pyrs1)
for i in np.arange(len(pyrs1)):
    vec_APs_p1[i], APcount_p1[i] = rec_APs(0.5, pyrs1[i].soma)
    
# spiketimes p2
vec_APs_p2 = [[]]*len(pyrs2)
APcount_p2 = [[]]*len(pyrs2)
for i in np.arange(len(pyrs2)):
    vec_APs_p2[i], APcount_p2[i] = rec_APs(0.5, pyrs2[i].soma)

# spiketimes m2
vec_APs_m2 = [[]]*len(mars2)
APcount_m2 = [[]]*len(mars2)
for i in np.arange(len(mars2)):
    vec_APs_m2[i], APcount_m2[i] = rec_APs(0.5, mars2[i].soma)
    
# extracellular recording
h.load_file(1,"../../recording/LFP/extracell_rec.hoc")
h.setelec(grid_size*dist/2, grid_size*dist/2, grid_size*dist/2) # middle of area 2
h.setelec(0,0,0)
vec_vrec = rec(h._ref_vrec)

# <codecell>

for trial in np.arange(n_trials):
 
    # Run
    start_time = time.time() # measure run time
    h.tstop = tstop + onset
    h.steps_per_ms = 1 / dt
    h.dt = dt
    h.v_init = -70
    h.init()
    h.run()
    print "time to run (s): ", time.time() - start_time
    sys.stdout.flush()

    # Convert to arrays and cut off onset    
    vrec = np.array(vec_vrec)[onset/h.dt:-1]
   
    APs_p1 = [[]]*len(pyrs1)
    APs_p2 = [[]]*len(pyrs2)
    APs_m2 = [[]]*len(mars2)
    
    for i,APs in enumerate(vec_APs_p1):
        APs = np.array(APs)
        if APs.size>0:
            APs = APs[APs>onset]
            APs = APs[APs<=tstop+onset]
            APs_p1[i] = APs - onset
    
    for i,APs in enumerate(vec_APs_p2):
        APs = np.array(APs)
        if APs.size>0:
            APs = APs[APs>onset]
            APs = APs[APs<=tstop+onset]
            APs_p2[i] = APs - onset
    
    for i,APs in enumerate(vec_APs_m2):
        APs = np.array(APs)
        if APs.size>0:
            APs = APs[APs>onset]
            APs = APs[APs<=tstop+onset]
            APs_m2[i] = APs - onset
    
    v_p1 = [[]]*len(pyrs1)
    v_tuft_p1 = [[]]*len(pyrs1)
    v_p2 = [[]]*len(pyrs2)
    v_tuft_p2 = [[]]*len(pyrs2)
    v_m2 = [[]]*len(mars2)
    
    for i,v in enumerate(vec_v_p1):
        v_p1[i] = np.array(v)[onset/dt:-1]
    
    for i,v in enumerate(vec_v_tuft_p1):
        v_tuft_p1[i] = np.array(v)[onset/dt:-1]
        
    for i,v in enumerate(vec_v_p2):
        v_p2[i] = np.array(v)[onset/dt:-1]
        
    for i,v in enumerate(vec_v_tuft_p2):
        v_tuft_p2[i] = np.array(v)[onset/dt:-1]
    
    for i,v in enumerate(vec_v_m2):
        v_m2[i] = np.array(v)[onset/dt:-1]
    
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

# <codecell>

v_p1 = np.array(vec_v_p1[3])[onset/h.dt:-1]
v_tuft_p1 = np.array(vec_v_tuft_p1[2])[onset/h.dt:-1]
v_p2 = np.array(vec_v_p2[0])[onset/h.dt:-1]
v_tuft_p2 = np.array(vec_v_tuft_p2[2])[onset/h.dt:-1]
v_m2 = np.array(vec_v_m2[2])[onset/h.dt:-1]

t = np.arange(0,tstop,dt)

# Plot: membrane potential single neurons
pl.figure(1)
pl.plot(t, v_p1, 'k', label='soma')
pl.plot(t, v_tuft_p1, 'r', label='tuft')
pl.legend(loc='upper right',prop={'size':12})
pl.ylabel('Membrane potential (mV)')
pl.xlabel('Time (ms)')
pl.xlim([0,1000])

pl.figure(2)
pl.plot(t, v_p2, 'k', label='soma')
pl.plot(t, v_tuft_p2, 'r', label='tuft')
pl.legend(loc='upper right',prop={'size':12})
pl.ylabel('Membrane potential (mV)')
pl.xlabel('Time (ms)')
pl.xlim([0,1000])

pl.figure(3)
pl.plot(t, v_m2, 'k', label='soma')
pl.legend(loc='upper right',prop={'size':12})
pl.ylabel('Membrane potential (mV)')
pl.xlabel('Time (ms)')
pl.xlim([0,1000])

# <codecell>

# Raster plots
t = np.arange(0,tstop,dt)

# raster plot p1
fig, ax = pl.subplots(1)
for i in np.arange(0,len(APs_p1)):
    pl.scatter(APs_p1[i],i * np.ones(len(APs_p1[i])), s=1, color='k')
pl.ylabel('# Neuron')
pl.xlabel('Time (ms)')
pl.ylim([0,n_p1])
pl.xlim(0,2000)

# raster plot p2
fig, ax = pl.subplots(1)
for i in np.arange(0,len(APs_p2)):
    pl.scatter(APs_p2[i],i * np.ones(len(APs_p2[i])), s=1, color='k')
    pl.ylabel('# Neuron')
pl.xlabel('Time (ms)')
pl.ylim([0,n_p2])
pl.xlim(0,2000)

# raster plot m2
fig, ax = pl.subplots(1)
for i in np.arange(0,len(APs_m2)):
    pl.scatter(APs_m2[i],i * np.ones(len(APs_m2[i])), s=1, color='r')
pl.ylabel('# Neuron')
pl.xlabel('Time (ms)')
pl.ylim([0,n_m2])
pl.xlim(0,1000)

# <codecell>

# oscillatory inhibitory input to p1
fig, ax = pl.subplots(1)
for i in np.arange(0,len(APs_p1)):
    pl.scatter(spiketimes_ip1[i,5][0],i * np.ones(len(spiketimes_ip1[i,5][0])), s=1, color='k')
pl.ylabel('# Neuron')
pl.xlabel('Time (ms)')
pl.ylim([0,n_p1])
pl.xlim(0,1000)

# raster plot p1
fig, ax = pl.subplots(1)
for i in np.arange(0,len(APs_p1)):
    pl.scatter(APs_p1[i],i * np.ones(len(APs_p1[i])), s=1, color='k')
pl.ylabel('# Neuron')
pl.xlabel('Time (ms)')
pl.ylim([0,n_p1])
pl.xlim(0,1000)

