from neuron import h
import numpy as np
from stimuli import make_stim
from synapse import make_syn
import copy
from random import Random
from time import time


# Single Connection


def connect(stim, syn, weight, section):
    """
    Connects the synapse receiving the given stimulus into the given section of a cell. 
    
    Input:
    stim: neuron stimulus
    syn: neuron synapse
    weight: weight 
    
    Output:
    con: neuron connection
    """
                   
    con = h.NetCon(stim, syn, sec=section)
    con.weight[0] = weight
    
    return con


def connect_cells(pre, params_syn, params_weight, thresh, delay):
    """
    Connects two cells (pre and post) with each other.
    
    Input:
    pre: neuron section of the presynaptic cell
    post: neuron section of the postsynaptic cell
    kind: kind of the synapse (e.g. 'AMPA')
    pos: position of the synapse on the section 
    weight: weight 
    thresh: AP threshold of the membrane potential
    delay: time between the elicitation of the AP and the arrival at the postsynaptic cell
    
    Output:
    syn: neuron synapse
    con: neuron connection
    """
    
    # make weight
    weight = make_weight(params_weight)
            
    # make synapse
    syn = make_syn(**params_syn) 
    
    # make connection
    con = h.NetCon(pre(params_syn['pos'])._ref_v, syn, thresh, delay, weight, sec=pre)
    return syn, con, weight


def make_weight(params_weight):
    """
    Creates a weight from the specified parameters. 
    
    Input:
    params_weight: for same weights {'weight':weight} and for gaussian distributed weights {'mean':mean, 'std':std} 
    
    Output:
    w: weight 
    """
    
    if params_weight['kind'] == 'same':
        w = params_weight['weight']
    elif params_weight['kind'] == 'gaussian':
        w = np.random.normal(params_weight['mean'], params_weight['std'])
        if w < 0: w = 0  # prevent negative weights
    else: 
        raise ValueError('Unknown type of weighting!')
    return w


# Complex Connectivity


def synaptic_input(n_stim, cell, section, params_stim, params_syn, params_weight):
    """
    Creates and connects n_stim synapses. 
    
    Input:
    n_stim: number of stimuli
    cell: cell that receives the stimuli
    section: target section of the cell
    params_stim: parameter for the stimuli (see make_stim)
    params_syn: parameter for the synapses (see make_syn)
    params_weight: parameter for the weight (see make_weight)
    
    Output:
    syns: synapses
    stims: stimuli
    cons: connections 
    weights: weights
    """
    
    syns = np.zeros(n_stim, dtype=object)
    stims = np.zeros(n_stim, dtype=object)
    cons = np.zeros(n_stim, dtype=object)
    weights = np.zeros(n_stim, dtype=object)
    spiketimes_vecs = np.zeros(n_stim, dtype=object)
    
    # select section on the neuron
    if section == 'soma':
        sec = cell.soma
    elif section == 'dend':
        sec = cell.dend
    elif section == 'tuft':
        sec = cell.tuft
    else: 
        raise ValueError('Section not known!')
    params_syn['section'] = sec
    params_stim['section'] = sec
    
    for i in np.arange(n_stim):
        # make stimulus
        stims[i], spiketimes_vecs[i] = make_stim(**params_stim) 
                    
        # make synapse
        syns[i] = make_syn(**params_syn)
        
        # make weight
        weights[i] = make_weight(params_weight) 
    
        # make connection
        cons[i] = connect(stims[i], syns[i], weights[i], params_syn['section'])

    return syns, stims, cons, weights, spiketimes_vecs

def synaptic_input_fromfile(n_stim, cell, section, params_stim, params_syn, params_weight, spiketimes):
    """
    Creates and connects n_stim synapses.

    Input:
    n_stim: number of stimuli
    cell: cell that receives the stimuli
    section: target section of the cell
    params_stim: parameter for the stimuli (see make_stim)
    params_syn: parameter for the synapses (see make_syn)
    params_weight: parameter for the weight (see make_weight)

    Output:
    syns: synapses
    stims: stimuli
    cons: connections
    weights: weights
    """

    syns = np.zeros(n_stim, dtype=object)
    stims = np.zeros(n_stim, dtype=object)
    cons = np.zeros(n_stim, dtype=object)
    weights = np.zeros(n_stim, dtype=object)

    # select section on the neuron
    if section == 'soma':
        sec = cell.soma
    elif section == 'dend':
        sec = cell.dend
    elif section == 'tuft':
        sec = cell.tuft
    else:
        raise ValueError('Section not known!')
    params_syn['section'] = sec
    params_stim['section'] = sec

    spiketimes_vec = [0] * np.size(spiketimes)
    for i, st in enumerate(spiketimes):
        spiketimes_vec[i] = h.Vector()
        spiketimes_vec[i].from_python(st)

    for i in np.arange(n_stim):
        # make stimulus
        stims[i] = h.VecStim(params_stim['pos'], sec=params_stim['section'])
        stims[i].play(spiketimes_vec[i])

        # make synapse
        syns[i] = make_syn(**params_syn)

        # make weight
        weights[i] = make_weight(params_weight)

        # make connection
        cons[i] = connect(stims[i], syns[i], weights[i], params_syn['section'])

    return syns, stims, cons, weights, spiketimes_vec


# Generate Connectivity


def gen_con_rand(pres, posts, params):
    """
    Generates random connections according to the given probability.
    
    Input:
    prob: probability of a connection (0<=prob<=1)
    pres: neuron sections of the presynaptic cells
    posts: neuron sections of the postsynaptic cells
    params: parameter of the connection (see connect_cells)
    
    Output:
    syn: neuron synapses
    con: neuron connections
    weights: weights
    """

    if 'seed_prng' not in params:
        seed_prng = time()
    prng = Random()
    prng.seed(params['seed_prng'])
    
    syn = []
    con = []
    weights = []

    params_connect = copy.deepcopy(params)
    del params_connect['prob']
    del params_connect['seed_prng']
    
    for pre in pres: 
        # make connections randomly according to prob
        connections = np.array([prng.random() for i in range(len(posts))]) <= params['prob']
        posts_sel = np.array(posts)[connections]
        for post in posts_sel:
            params_connect['pre'] = pre
            params_connect['params_syn']['section'] = post
            
            # connect cells
            syn_tmp, con_tmp, weight_tmp = connect_cells(**params_connect)
            
            # save connection
            syn.append(syn_tmp)
            con.append(con_tmp)
            weights.append(weight_tmp)
        
    return syn, con, weights, connections

