from __future__ import division
from neuron import h
import numpy as np
from time import time
from random import Random


def make_stim(**params_stim):
    """
    Creates a stimulus of the specified kind.
    
    Input:
    params_stim: for poisson stimulus {'kind':'poisson', 'freq':freq, 'start':start, 'noise':noise, 'pos':pos, 'section':section} 
                 (see poisson_stim) 
                 and for oscillatory stimulus {'kind':'osc', 'freq_osc':freq_osc, 'freq':freq, 'tstop':tstop, 'dt':dt, 'pos':pos, 
                 'section':section} (see spiketimes2stim)
    
    Output: 
    stim: stimulus
    """
    
    if params_stim['kind'] == 'poisson':
        del params_stim['kind']
        stim = poisson_stim(**params_stim)
        return stim, []
    elif params_stim['kind'] == 'poisson_gen':
        del params_stim['kind']
        stim, spiketimes_vec = poisson_stim_gen(**params_stim)
        return stim, spiketimes_vec
    elif params_stim['kind'] == 'osc':
        del params_stim['kind']
        stim, spiketimes_vec = osc_stim(**params_stim)
        return stim, spiketimes_vec
    elif params_stim['kind'] == 'transient_osc':
        del params_stim['kind']
        stim, spiketimes_vec = transient_osc_stim(**params_stim)
        return stim, spiketimes_vec
    else:
        raise ValueError('Unknown type of stimulation.')


def poisson_stim(freq, onset, tstop, start, noise, pos, section):
    """
    Creates a Poisson distributed stimulus.
    
    Input:
    freq: firing rate
    start: time of the most likely first spike
    noise: the interval between spikes consists of a fixed interval of duration (1 - noise)*interval plus a negexp 
           interval of mean duration noise*interval (0 <= noise <= 1) 
    pos: position of the stimulus on the section
    section: section on which the stimulus is placed (has to refer to a section in neuron)
    
    Output: 
    stim: Poisson distributed stimulus
    """
    n_spikes = (onset+tstop)*(freq/1000) + 10  # some more to prevent shortcomings due to random variation
    
    stim = h.NetStim(pos, sec=section)
    stim.interval = 1/(freq/1000) # time between spikes
    stim.start = start # start of 1. spike
    stim.noise = noise # noise in the ISIs
    stim.number = n_spikes # number of spikes
    
    return stim

def poisson_stim_gen(freq, onset, tstop, dt, pos, section, seed_prng=None):
    """
    Creates a Poisson distributed stimulus.

    Input:
    freq: firing rate
    start: time of the most likely first spike
    noise: the interval between spikes consists of a fixed interval of duration (1 - noise)*interval plus a negexp
           interval of mean duration noise*interval (0 <= noise <= 1)
    pos: position of the stimulus on the section
    section: section on which the stimulus is placed (has to refer to a section in neuron)

    Output:
    stim: Poisson distributed stimulus
    """
    r = make_constfun(freq, onset+tstop, dt)
    spiketimes = fun2spiketimes(r, onset+tstop, dt, seed_prng)
    stim, spiketimes_vec = spiketimes2stim(pos, section, spiketimes)

    return stim, spiketimes_vec


def osc_stim(freq_osc, freq, onset, tstop, dt, pos, section, seed_prng=None):
    """
    Creates an oscillatory stimulus.
    
    Input:
    freq_osc: frequency of the oscillation underlying the spike generation
    freq: firing frequency
    tstop: simulation time
    dt: time step
    pos: position of the stimulus on the section
    section: section on which the stimulus is placed (has to refer to a section in neuron)
    
    Output:
    stim: Oscillatory stimulus
    """ 
    
    r = make_oscfun(freq_osc, freq, onset+tstop, dt)
    spiketimes = fun2spiketimes(r, onset+tstop, dt, seed_prng)
    stim, spiketimes_vec = spiketimes2stim(pos, section, spiketimes)
    
    return stim, spiketimes_vec


def transient_osc_stim(freq_osc, freq, transient, onset, tstop, dt, pos, section, seed_prng=None):
    """
    Creates an oscillatory stimulus with a transient in the beginning i.e. noise in the spike timing reduces during the transient to 0
    so that the underlying oscillation is revealed.
    
    Input:
    freq_osc: frequency of the oscillation underlying the spike generation
    freq: firing frequency
    tstop: simulation time
    dt: time step
    pos: position of the stimulus on the section
    section: section on which the stimulus is placed (has to refer to a section in neuron)
    
    Output:
    stim: Oscillatory stimulus
    """ 
    
    r = make_oscfun(freq_osc, freq, onset+tstop, dt)
    spiketimes = fun2spiketimes(r, onset+tstop, dt, seed_prng)
    spiketimes_new = make_transient_spiketimes(spiketimes, freq_osc, onset, transient, tstop, seed_prng)
    stim, spiketimes_vec = spiketimes2stim(pos, section, spiketimes_new)
    
    return stim, spiketimes_vec


def spiketimes2stim(pos, section, spiketimes):
    """
    Creates a stimulus from the given spiketimes.
    
    Input:
    pos: position of the stimulus on the section
    section: section on which the stimulus is placed (has to refer to a section in neuron)
    spiketimes: array containing the spike times
    
    Output: 
    stim: Stimulus with the given spiketimes
    spiketimes_vec: Neuron representation of spiketimes
    """
    
    spiketimes_vec = h.Vector()
    spiketimes_vec.from_python(spiketimes) # convert spiketimes to neuron vector
    
    # make stimulus
    stim = h.VecStim(pos, sec=section)
    stim.play(spiketimes_vec)
    
    return stim, spiketimes_vec


# Make Spiketimes

def make_oscfun(freq_osc, freq, tstop, dt):
    """
    Computes the y-values of an oscillatory function of the given frequency. The amplitude of the oscillatory function 
    is adjusted so that the expected number of spikes matches the firing frequency.
    
    Input:
    freq_osc: frequency of the oscillation underlying the spike generation
    freq: firing frequency
    tstop: simulation time
    dt: time step
    
    Output:
    r: y-values of the created oscillatory function 
    """ 
     
    t = np.arange(0, tstop, dt)
    r = np.zeros(np.size(t))
    amp = (tstop*freq/1000) / (-1/(2*np.pi*freq_osc/1000) * np.sin(2*np.pi*freq_osc/1000*tstop) + tstop)
    # E_t[n_spikes] = integral_t(r(t)*1) --> solve for the amplitude (n_spikes is given by the period times the frequency)
    
    for i, ts in enumerate(t):
        r[i] = amp + amp*np.cos(2*np.pi*ts*freq_osc/1000) # +amp to get it above 0
    
    return r

def make_constfun(freq, tstop, dt):
    """
    Computes the y-values of a constant function of the given frequency. The amplitude of the function
    is adjusted so that the expected number of spikes matches the firing frequency.

    Input:
    freq: firing frequency
    tstop: simulation time
    dt: time step

    Output:
    r: y-values of the created constant function
    """
    r = np.ones(tstop/dt) * freq / 1000  # 1/ms

    return r


def fun2spiketimes(r, tstop, dt, seed_prng=None):
    """
    Creates Poisson distributed spiketimes given a certain function.
    
    Input: 
    r: y-values of the function that shall be used to create the spiketimes
    tstop: simulation time
    dt: time step
    
    Output:
    spiketimes: array containing the spike times
    """
    if seed_prng is None:
        seed_prng = time()
    prng = Random()
    prng.seed(seed_prng)

    t = np.arange(0, tstop, dt)
    spiketrain = np.zeros(np.size(t), dtype=int)
    
    for i, ts in enumerate(t):
        if r[i]*dt > prng.random():
            spiketrain[i] = 1
        else:
            spiketrain[i] = 0
    spiketimes = sorted(t[np.nonzero(spiketrain)])  # convert spikes to spike times

    #pl.plot(time, spiketrain, '*')
    #pl.show()
    #pl.plot(time, r)
    #pl.show()
    
    return spiketimes


def make_transient_spiketimes(spiketimes, freq_osc, onset, transient, tstop, seed_prng=None):

    if seed_prng is None:
        seed_prng = time()
    prng = Random()
    prng.seed(seed_prng)

    interval = 1000/freq_osc
    spiketimes_new = np.zeros(np.size(spiketimes))
    
    for i, st in enumerate(spiketimes):
        if st < onset: 
            noise = interval # spike can jitter over the whole interval
            shift = prng.uniform(-1 * noise/2, noise/2) # get a random value in the interval determined by noise
            spiketimes_new[i] = st + shift 
        elif st < onset + transient: 
            noise = interval - (st * interval) / (onset+transient) # jitter reduces to 0 towards the end of the transient
            shift = prng.uniform(-1 * noise/2, noise/2) # get a random value in the noise interval determined by noise
            spiketimes_new[i] = st + shift 
        else: 
            spiketimes_new[i] = st

    spiketimes_new = spiketimes_new[spiketimes_new>0]
    spiketimes_new = spiketimes_new[spiketimes_new<tstop+onset]
    spiketimes_new = sorted(spiketimes_new)
    
    return spiketimes_new