# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from __future__ import division

from general_functions.plotting import plot_style
import numpy as np
import pylab as pl
from matplotlib.collections import LineCollection
from neuron import h
from mpl_toolkits.mplot3d import Axes3D

# <codecell>

def plot_morph(pyr):
    """plot of the position of the soma of the specified cell types"""
    secs = ['soma', 'dend', 'apic', 'tuft', 'hillock', 'iseg', 'axon']
    n_points = 2
    X = [0]*n_points
    Y = [0]*n_points
    Z = [0]*n_points
    d = [0]*n_points
    
    fig = pl.figure()
    ax = fig.add_subplot(111)

    for sec in secs:
        h('access '+pyr+'[0].'+sec)
        for i in np.arange(n_points):
            X[i] = h.x3d(i)
            Y[i] = h.y3d(i)
            Z[i] = h.z3d(i)
            d[i] = h.diam3d(i)
        y = np.linspace(Y[0],Y[1],100)
        z = np.linspace(Z[0],Z[1],100)
        diams = np.linspace(d[0],d[1],100)
        
        for j in range(len(y)-1):
            pl.plot(y[j:j+2], z[j:j+2], linewidth=diams[j], color='k')
        #ax.plot(Y,Z,color='k',linewidth=d[i])
    plot_style(ax,'y (um)','z (um)',[-310,310],[])
    pl.gca().set_aspect('equal', adjustable='box')
    ax.set_xticks([-300,0,300])
    pl.draw()
    pl.show()
    pl.savefig('morph.svg')

# <codecell>
# load channels
#h.nrn_load_dll("../channels/x86_64/.libs/libnrnmech.so")
# load neuron templates
#h.load_file(1, "../models/Pyramidal.hoc")
h.nrn_load_dll("../../model/channels/Bahl/i686/.libs/libnrnmech.so")
model = "/Bahl/Pyramidal.hoc" #"Pyramidal.hoc"
h.load_file(1, "../../model/models/"+model)
pyr = h.Pyramidal()
plot_morph('Pyramidal')

# <codecell>


