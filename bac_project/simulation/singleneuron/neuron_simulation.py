from __future__ import division
import numpy as np
import pylab as pl
from neuron import h
import os
import json
from connectivity.connection import synaptic_input
from recording.record import rec, rec_APs
from general_functions.saving import save_as_txt
from analyses import functions
from time import time
from random import Random

h.load_file("stdrun.hoc")  # load NEURON libraries
h("""cvode.active(0)""")  # unvariable time step
h.nrn_load_dll("../../connectivity/synapse_models/i686/.libs/libnrnmech.so")  # import synapse models


def run(cell, frequencies, simulation_params, params_syns, params_oscsyns, n_trials, folder, model):

    # make folder 
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    # initialize variables
    v_all = np.zeros([n_trials, np.size(frequencies)], dtype=object)
    v_tuft_all = np.zeros([n_trials, np.size(frequencies)], dtype=object)
    ica_all = np.zeros([n_trials, np.size(frequencies)], dtype=object)
    APs_all = np.zeros([n_trials, np.size(frequencies)], dtype=object)
    spiketimes_list_all = np.zeros([n_trials, np.size(frequencies)], dtype=object)
            
    # save parameters
    with open(folder+'/f.npy', 'w') as f:
        np.save(f, frequencies)
    with open(folder+'/simulation_params.json', 'w') as f:
        json.dump(simulation_params, f)
    with open(folder+'/params_syns.json', 'w') as f:
        json.dump(params_syns, f)
    with open(folder+'/params_oscsyns.json', 'w') as f:
        json.dump(params_oscsyns, f)
    with open(folder+'/n_trials.npy', 'w') as f:
        np.save(f, n_trials)
    save_as_txt(folder, 'model_dir', model)
    
    # insert cell into parameters (needs to be out for saving)
    for params in params_syns:
        params['cell'] = cell
    params_oscsyns['cell'] = cell
      
    # set simulation time
    h.tstop = simulation_params['tstop'] + simulation_params['onset']
    h.steps_per_ms = 1 / simulation_params['dt']
    h.dt = simulation_params['dt']
    
    # initialize recording vectors
    vec_v = rec(p.soma, 'v')
    vec_v_tuft = rec(p.tuft, 'v')
    vec_APs, APcount = rec_APs(p.soma)
    vec_i = rec(p.tuft, 'ica')
    
    # set up stimulation
    syn = np.zeros(np.size(params_syns), dtype=object)
    stim = np.zeros(np.size(params_syns), dtype=object)
    con = np.zeros(np.size(params_syns), dtype=object)
    weights = np.zeros(np.size(params_syns), dtype=object)
    spiketimes_list = np.zeros(np.size(params_syns)+1, dtype=object)

    # simulation for different frequencies of oscillatory inhibition
    for idx in np.arange(np.size(frequencies)):
        for trial in np.arange(n_trials):

            # synaptic input
            for i, params in enumerate(params_syns):
                syn[i], stim[i], con[i], weights[i], spiketimes_list[i] = synaptic_input(**params)
            # oscillatory synapses
            params_oscsyns['params_stim']['freq_osc'] = frequencies[idx]
            syn_osc, stim_osc, con_osc, weights_osc, spiketimes_list[i+1] = synaptic_input(**params_oscsyns)
            
            # run simulation
            h.v_init = simulation_params['v_init']
            h.run()
            
            # convert to array and cut off onset
            start = simulation_params['onset'] / simulation_params['dt']
            v = np.array(vec_v)[start:]
            v_tuft = np.array(vec_v_tuft)[start:]
            ica = np.array(vec_i)[start:]
            APs = np.array(vec_APs)
            APs = APs[APs > simulation_params['onset']]
            APs -= simulation_params['onset']
            
            # store data
            v_all[trial, idx] = v
            v_tuft_all[trial, idx] = v_tuft
            ica_all[trial, idx] = ica
            APs_all[trial, idx] = APs
            spiketimes_list_all[trial, idx] = [[st.to_python() for st in spiketimes] for spiketimes in spiketimes_list]

            # Plot 
            #t = np.arange(0,tstop,dt)
            #pl.plot(t, v, 'k')
            #pl.plot(t, v_tuft, 'r')
            #pl.xlim([0,2000])
            #pl.show()

            # Analyse bursting, firing rate and coherence
            burst_len = 5
            BAC_percent, FAC_percent, other_burst_percent, burst_percent = functions.percentage_burst(APs, v_tuft,
                                                                                    burst_len, simulation_params['dt'])
            print 'percent BAC (5ms): ' + str(BAC_percent) + '  percent burst (5ms): ' + str(burst_percent)
            burst_len = 10
            BAC_percent, FAC_percent, other_burst_percent, burst_percent = functions.percentage_burst(APs, v_tuft,
                                                                                    burst_len, simulation_params['dt'])
            print 'percent BAC (10ms): ' + str(BAC_percent) + '  percent burst (10ms): ' + str(burst_percent)
            burst_len = 20
            BAC_percent, FAC_percent, other_burst_percent, burst_percent = functions.percentage_burst(APs, v_tuft,
                                                                                    burst_len, simulation_params['dt'])
            print 'percent BAC (20ms): ' + str(BAC_percent) + '  percent burst (20ms): ' + str(burst_percent)

            fr = np.size(APs) / (simulation_params['tstop']/1000)
            print 'firing rate: ' + str(fr)

            coherence = functions.get_coherence(APs, frequencies[idx])
            print 'coherence: ' + str(coherence)
            
    # save data
    with open(folder+'/v_all.npy', 'w') as f:
        np.save(f, v_all)
    with open(folder+'/v_tuft_all.npy', 'w') as f:
        np.save(f, v_tuft_all)
    with open(folder+'/ica_all.npy', 'w') as f:
        np.save(f, ica_all)
    with open(folder+'/APs_all.npy', 'w') as f:
        np.save(f, APs_all)
    with open(folder+'/spiketimes_list_all.npy', 'w') as f:
        np.save(f, spiketimes_list_all)


if __name__ == "__main__":
    folder = 'data/test'
    h.nrn_load_dll("../../model/channels/Bahl/i686/.libs/libnrnmech.so")
    model = "/Bahl/Pyramidal.hoc"  #"Pyramidal.hoc"
    h.load_file(1, "../../model/models/"+model)

    # make pyramidal cell
    p = h.Pyramidal()

    f = np.arange(4, 121, 4)  # np.array([12])  #
    simulation_params = {
        'tstop': 500,
        'dt': 0.25,
        'v_init': -70,
        'onset': 200
    }
    n_trials = 10

    # parameters for synapse stimulation
    freq = 10
    pos = 0.5

    params_stim = {'kind': 'poisson_gen', 'onset': simulation_params['onset'], 'tstop': simulation_params['tstop'],
                   'dt': simulation_params['dt'], 'freq': freq, 'pos': pos, 'seed_prng': time()}
    params_syn = {'kind': 'AMPA', 'pos': pos}
    params_weight = {'kind': 'same', 'weight': 0.002}
    params_i1p1 = {'n_stim': 270, 'cell': 'pyramidal', 'section': 'dend', 'params_stim': params_stim,
                   'params_syn': params_syn, 'params_weight': params_weight}

    params_stim = {'kind': 'poisson_gen', 'onset': simulation_params['onset'], 'tstop': simulation_params['tstop'],
                   'dt': simulation_params['dt'], 'freq': freq, 'pos': pos, 'seed_prng': time()}
    params_syn = {'kind': 'NMDA', 'pos': pos}
    params_weight = {'kind': 'same', 'weight': 0.002}
    params_i2p1 = {'n_stim': 0, 'cell': 'pyramidal', 'section': 'dend', 'params_stim': params_stim,
                   'params_syn': params_syn, 'params_weight': params_weight}

    params_stim = {'kind': 'poisson_gen', 'onset': simulation_params['onset'], 'tstop': simulation_params['tstop'],
                   'dt': simulation_params['dt'], 'freq': freq, 'pos': pos, 'seed_prng': time()}
    params_syn = {'kind': 'AMPA', 'pos': pos}
    params_weight = {'kind': 'same', 'weight': 0.002}
    params_i3p1 = {'n_stim': 200, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
                   'params_syn': params_syn, 'params_weight': params_weight}

    params_stim = {'kind': 'poisson_gen', 'onset': simulation_params['onset'], 'tstop': simulation_params['tstop'],
                   'dt': simulation_params['dt'], 'freq': freq, 'pos': pos, 'seed_prng': time()}
    params_syn = {'kind': 'NMDA', 'pos': pos}
    params_weight = {'kind': 'same', 'weight': 0.002}
    params_i4p1 = {'n_stim': 60, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
                   'params_syn': params_syn, 'params_weight': params_weight}

    params_stim = {'kind': 'poisson_gen', 'onset': simulation_params['onset'], 'tstop': simulation_params['tstop'],
                   'dt': simulation_params['dt'], 'freq': freq, 'pos': pos, 'seed_prng': time()}
    params_syn = {'kind': 'GABA', 'pos': pos}
    params_weight = {'kind': 'same', 'weight': 0.002}
    params_i5p1 = {'n_stim': 20, 'cell': 'pyramidal', 'section': 'soma', 'params_stim': params_stim,
                   'params_syn': params_syn, 'params_weight': params_weight}

    params_syns = [params_i1p1, params_i2p1, params_i3p1, params_i4p1, params_i5p1]

    params_stim = {'kind': 'osc', 'freq_osc': [], 'freq': freq, 'onset': simulation_params['onset'],
                   'tstop': simulation_params['tstop'], 'dt': simulation_params['dt'], 'pos': pos, 'seed_prng': time()}
    params_syn = {'kind': 'GABA', 'pos': pos}
    params_weight = {'kind': 'same', 'weight': 0.002}
    params_oscsyns = {'n_stim': 40, 'cell': 'pyramidal', 'section': 'tuft', 'params_stim': params_stim,
                      'params_syn': params_syn, 'params_weight': params_weight}

    # start simulation
    run(p, f, simulation_params, params_syns, params_oscsyns, n_trials, folder, model)

    # lowfr_lowb: 80, 20, 100, 100, 40, 40
    # lowfr_highb: 50, 65, 100, 100, 40, 40
    # highfr_highb: 270, 0, 200, 60, 20, 40