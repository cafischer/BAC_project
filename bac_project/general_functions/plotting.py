import matplotlib
#matplotlib.use('Agg')
import matplotlib.pylab as pl
import matplotlib.font_manager as font_manager

def plot_style(ax, xlabel, ylabel, xlim, ylim, legend=False):
    
    # Set the fontsize of title, lables and ticks 
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(20) # for server 30

    # Set linewidth and markersize
    matplotlib.rc('lines', linewidth=2.0, markersize=10) # for server 2.5 and 15
    
    # Set labels and limits
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if len(xlim)>0: ax.set_xlim(xlim)
    if len(ylim)>0: ax.set_ylim(ylim)
        
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    # Set legend size
    if legend: legend = ax.legend(loc='upper right', fontsize=20) # for server 30


