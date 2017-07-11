from neuron import h


def rec(section, var, pos=0.5):
    """
    Creates a vector recording the given variable at section.
    :param section: Neuron section from which shall be recorded.
    :type section: NEURON section
    :param var: Variable to record.
    :type var: str
    :param pos: Position on the section.
    :type pos: float
    :return: Vector where values will be stored during run.
    :rtype: NEURON vector
    """
    vec = h.Vector()
    vec.record(getattr(section(pos), '_ref_'+var))
    return vec


def rec_APs(section, pos=0.5):
    """
    Creates a vector recording AP times.
    :param section: Neuron section from which shall be recorded.
    :type section: NEURON section
    :param pos: Position on the section.
    :type pos: float
    :return: Vector where the AP times will be stored during run.
    :rtype: NEURON vector
    """
    vec = h.Vector()
    APcount = h.APCount(pos, sec=section)
    APcount.record(vec)
    return vec, APcount
    

