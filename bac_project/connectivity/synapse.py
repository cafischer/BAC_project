from __future__ import division
from neuron import h


def make_syn(kind, pos, section):
    """
    Creates a synapse of the specified kind.
    
    Input:
    kind: type of synapse (AMPA, NMDA, GABA, AMPA_facil, NMDA_facil, GABA_depress)
    pos: position of the synapse on the section 
    section: section on which the synapse is placed (has to refer to a section in neuron)
    
    Output:
    syn: created synapse
    
    Information:
    Parameters are based on: Chapter 6 of Modelling synapses from Roth and Rossum
    """
    
    # create synapse
    if kind == "AMPA":
        syn = h.Exp2Syn(pos, sec=section)
        syn.tau1= 0.2 # ms 
        syn.tau2 = 1.7 # ms 
        syn.e = 0 # mV     
                
    elif kind == "NMDA":
        syn = h.NMDA(pos, sec=section)
        syn.Alpha = 5 # 1/ms/mM
        syn.Beta = 1/30 # 1/ms 
        syn.Cdur = 1 # ms

    elif kind == "NMDA2":
        syn = h.Exp2Syn(pos, sec=section)
        syn.tau1= 2 # ms
        syn.tau2 = 26 # ms
        syn.e = 0 # mV
        
    elif kind == "GABA":
        syn = h.Exp2Syn(pos, sec=section)
        syn.tau1= 0.26 # ms 
        syn.tau2 = 6.5 # ms 
        syn.e = -70 # mV
        
    elif kind == "AMPA_facil":
        syn = h.FDSExp2Syn(pos, sec=section)
        syn.tau1= 0.2 # ms 
        syn.tau2 = 1.7 # ms 
        syn.e = 0 # mV   
        syn.tau_F = 670 # ms time constant facilitation
        syn.tau_D1 = 138 # ms time constant depression
        syn.f = 0.4 # amount of facilitation per presynaptic AP
        syn.d1 = 0.1 # amount of depression per presynaptic AP
        
    elif kind == "NMDA_facil":
        syn = h.FDSExp2Syn(pos, sec=section)
        syn.tau1= 2 # ms 
        syn.tau2 = 26 # ms 
        syn.e = 0 # mV   
        syn.tau_F = 670 # ms time constant facilitation
        syn.tau_D1 = 138 # ms time constant depression
        syn.f = 0.4 # amount of facilitation per presynaptic AP
        syn.d1 = 0.1 # amount of depression per presynaptic AP

    elif kind == "GABA_depress":
        syn = h.FDSExp2Syn(pos, sec=section)
        syn.tau1= 0.26 # ms 
        syn.tau2 = 6.5 # ms 
        syn.e = -70 # mV   
        syn.tau_F = 2 # ms time constant facilitation
        syn.tau_D1 = 1250 # ms time constant depression
        syn.f = 0.1 # amount of facilitation per presynaptic AP
        syn.d1 = 0.4 # amount of depression per presynaptic AP
        
    else:
        raise ValueError('Synapse type not available!')
        
    return syn