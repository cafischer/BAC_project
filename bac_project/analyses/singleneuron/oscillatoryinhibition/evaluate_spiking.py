from __future__ import division
from general_functions.plotting import plot_style
from general_functions.saving import save_as_txt
import numpy as np
import pylab as pl
import scipy.stats.stats as st
import os
from neuron import h
from analyses.functions import get_bursts, identify_bursts, get_phases_freq, circ_r, get_coherence, percentage_burst


def compute_firing_rate(folder, f, n_trials, tstop, APs_all):
    
    # initialize
    firing_rate = np.zeros([n_trials,np.size(f)])

    # compute firing rate
    for idx in np.arange(np.size(f)): 
        for trial in np.arange(n_trials): 
            n_APs = np.size(APs_all[trial,idx])
            firing_rate[trial,idx] = n_APs/(tstop/1000)

    # make new folder
    folder = folder + 'firing_rate/'
    if not os.path.exists(folder): os.makedirs(folder)
    
    save_as_txt(folder,'firing_rate','mean: '+str(np.mean(firing_rate,0))+'\n'+'std: '+str(np.std(firing_rate,0))) 
       
    outfile = open(folder+'/firing_rate.npy', 'w') 
    np.save(outfile, firing_rate)  

    # Plot: Firing frequency  
    if len(f)>1: df = np.diff(f)[0]
    else: df = 1
    fig, ax = pl.subplots(1)
    pl.errorbar(f, np.mean(firing_rate,0), np.std(firing_rate,0), fmt='-o', color='k')
    plot_style(ax, 'Frequency of oscillatory inhibition (Hz)', 'Firing rate (Hz)', [f[0]-df,f[-1]+df], [0,pl.ylim()[1]])
    if save: pl.savefig(folder+'/firing_rate.svg')

# <codecell>


def compute_coherence(folder, f, n_trials, dt, burst_len, APs_all, v_tuft_all):
    
    # Initialize arrays
    coherence = np.zeros([n_trials,np.size(f)])
    coherence_BAC = np.zeros([n_trials,np.size(f)])
    coherence_FAC = np.zeros([n_trials,np.size(f)])
    coherence_other_burst = np.zeros([n_trials,np.size(f)])
    coherence_single = np.zeros([n_trials,np.size(f)])
    coherence_burst = np.zeros([n_trials,np.size(f)])

    for idx, freq in enumerate(f): 
        for trial in np.arange(n_trials): 
            v_tuft = v_tuft_all[trial,idx]
            APs = APs_all[trial,idx]
   
            BAC_mask, FAC_mask, other_burst_mask, single_mask, burst_mask = identify_bursts(APs, v_tuft, burst_len, dt)
            
            # Phase coherence
            coherence[trial,idx] = get_coherence(APs, freq)            
            coherence_BAC[trial,idx] = get_coherence(APs[BAC_mask], freq)
            coherence_FAC[trial,idx] = get_coherence(APs[FAC_mask], freq) 
            coherence_other_burst[trial,idx] = get_coherence(APs[other_burst_mask], freq)
            coherence_single[trial,idx] = get_coherence(APs[single_mask], f[idx]) 
            coherence_burst[trial,idx] = get_coherence(APs[burst_mask], f[idx])


    # make new folder
    folder = folder + 'coherence/'
    if not os.path.exists(folder): os.makedirs(folder)
        
    # save
    save_as_txt(folder,'coherence','mean: '+str(st.nanmean(coherence,0))+'\n'+'std: '+str(st.nanstd(coherence,0))) 
    save_as_txt(folder,'coherence_BAC','mean: '+str(st.nanmean(coherence_BAC,0))+'\n'+'std: '+str(st.nanstd(coherence_BAC,0))) 
    save_as_txt(folder,'coherence_FAC','mean: '+str(st.nanmean(coherence_FAC,0))+'\n'+'std: '+str(st.nanstd(coherence_FAC,0))) 
    save_as_txt(folder,'coherence_other_burst','mean: '+str(st.nanmean(coherence_other_burst,0))+'\n'+'std: '+str(st.nanstd(coherence_other_burst,0))) 
    save_as_txt(folder,'coherence_single','mean: '+str(st.nanmean(coherence_single,0))+'\n'+'std: '+str(st.nanstd(coherence_single,0))) 
    save_as_txt(folder,'coherence_burst','mean: '+str(st.nanmean(coherence_burst,0))+'\n'+'std: '+str(st.nanstd(coherence_burst,0)))

    outfile = open(folder+'/coherence.npy', 'w') 
    np.save(outfile, coherence)  
    outfile = open(folder+'/coherence_BAC.npy', 'w') 
    np.save(outfile, coherence_BAC)  
    outfile = open(folder+'/coherence_FAC.npy', 'w') 
    np.save(outfile, coherence_FAC)  
    outfile = open(folder+'/coherence_other_burst.npy', 'w') 
    np.save(outfile, coherence_other_burst)  
    outfile = open(folder+'/coherence_single.npy', 'w') 
    np.save(outfile, coherence_single)  
    outfile = open(folder+'/coherence_burst.npy', 'w') 
    np.save(outfile, coherence_burst)  
    
    # Plot: Coherence      
    if len(f) > 1: df = np.diff(f)[0]
    else: df = 1
    fig, ax = pl.subplots(1)
    pl.errorbar(f, st.nanmean(coherence,0), st.nanstd(coherence,0), fmt='-o', color='k')
    plot_style(ax, 'Frequency of oscillatory inhibition (Hz)', 'Vector Strength', [f[0]-df,f[-1]+df], [-0.1,1.1])
    if save: pl.savefig(folder+'/coherence.svg')

    # Plot: Coherence BAC, FAC, others   
    fig, ax = pl.subplots(1)
    pl.errorbar(f, st.nanmean(coherence_BAC,0), st.nanstd(coherence_BAC,0), fmt='-o', color='k', markerfacecolor='#998ec3', label='BAC')
    pl.errorbar(f, st.nanmean(coherence_FAC,0), st.nanstd(coherence_FAC,0), fmt='-o', color='k', markerfacecolor='#f1a340', label='FAC')
    pl.errorbar(f, st.nanmean(coherence_other_burst,0), st.nanstd(coherence_other_burst,0), fmt='-o', color='k', markerfacecolor='#f7f7f7', label='Others')
    plot_style(ax, 'Frequency of oscillatory inhibition (Hz)', 'Vector Strength', [f[0]-df,f[-1]+df], [-0.1,1.1], True)
    if save: pl.savefig(folder+'/coherence_BACFACothers.svg')

    # Plot: Coherence from single and burst events
    fig, ax = pl.subplots(1)
    pl.errorbar(f, st.nanmean(coherence_single,0), st.nanstd(coherence_single,0), fmt='-o', color='k', markerfacecolor='1.0', label='single-spike event')
    pl.errorbar(f, st.nanmean(coherence_burst,0), st.nanstd(coherence_burst,0), fmt='-o', color='k', markerfacecolor='0.0', label='burst event')
    plot_style(ax, 'Frequency of oscillatory inhibition (Hz)', 'Vector Strength', [f[0]-df,f[-1]+df], [-0.1,1.1], True)
    if save: pl.savefig(folder+'/coherence_singleburst.svg')

# <codecell>


def compute_percentage(folder, burst_len, f, n_trials, dt, APs_all, v_tuft_all):

    # Initialize arrays
    BAC_percent = np.zeros([n_trials,np.size(f)])
    FAC_percent = np.zeros([n_trials,np.size(f)])
    other_burst_percent = np.zeros([n_trials,np.size(f)])
    burst_percent = np.zeros([n_trials,np.size(f)])
    
    for idx, freq in enumerate(f): 
        for trial in np.arange(n_trials):
            v_tuft = v_tuft_all[trial,idx]
            APs = APs_all[trial,idx]
            
            # compute percentage of bursts
            (BAC_percent[trial,idx], FAC_percent[trial,idx], other_burst_percent[trial,idx], 
             burst_percent[trial,idx]) = percentage_burst(APs, v_tuft, burst_len, dt)
       
    # make new folder
    folder = folder + 'percentage/'
    if not os.path.exists(folder): os.makedirs(folder)
    
    # save  
    save_as_txt(folder,'burst_percent','mean: '+str(np.mean(burst_percent,0))+'\n'+'std: '+str(np.std(burst_percent,0)))
    save_as_txt(folder,'BAC_percent','mean: '+str(np.mean(BAC_percent,0))+'\n'+'std: '+str(np.std(BAC_percent,0)))
    save_as_txt(folder,'FAC_percent','mean: '+str(np.mean(FAC_percent,0))+'\n'+'std: '+str(np.std(FAC_percent,0)))
    save_as_txt(folder,'other_burst_percent','mean: '+str(np.mean(other_burst_percent,0))+'\n'+'std: '+str(np.std(other_burst_percent,0)))
    
    outfile = open(folder+'/BAC_percent.npy', 'w') 
    np.save(outfile, FAC_percent)
    outfile = open(folder+'/FAC_percent.npy', 'w') 
    np.save(outfile, BAC_percent)
    outfile = open(folder+'/other_burst_percent.npy', 'w') 
    np.save(outfile, other_burst_percent)
    outfile = open(folder+'/burst_percent.npy', 'w') 
    np.save(outfile, burst_percent)

    # Plot: Percent_bursting 
    if len(f)>1: df = np.diff(f)[0]
    else: df = 1
    fig, ax = pl.subplots(1)
    pl.errorbar(f, np.mean(burst_percent,0), np.std(burst_percent,0), fmt='-o', color='k')
    plot_style(ax, 'Frequency of oscillatory inhibition (Hz)', 'Percentage of burst events(%)', [f[0]-df,f[-1]+df], [0,105])
    if save: pl.savefig(folder+'/burst_percent.svg')

    # Plot: Percentage of BAC, FAC, others
    fig, ax = pl.subplots(1)
    pl.errorbar(f, np.mean(BAC_percent,0), np.std(BAC_percent,0), fmt='-o', color='k', markerfacecolor='#998ec3', label='BAC')
    pl.errorbar(f, np.mean(FAC_percent,0), np.std(FAC_percent,0), fmt='-o', color='k', markerfacecolor='#f1a340', label='FAC')
    pl.errorbar(f, np.mean(other_burst_percent,0), np.std(other_burst_percent,0), fmt='-o', color='k', markerfacecolor='#f7f7f7', label='Others')
    plot_style(ax, 'Frequency of oscillatory inhibition (Hz)', 'Percentage of events (%)', [f[0]-df,f[-1]+df], [0,105], True)
    if save: pl.savefig(folder+'/BACFACothers_percent.svg')  

# <codecell>


def compute_spikes_per_period(folder, burst_len, f, n_trials, dt):

    # Initialize arrays
    spikes_per_period = np.zeros([n_trials,np.size(f)])
    bursts_per_period = np.zeros([n_trials,np.size(f)])
    
    for idx in np.arange(np.size(f)): 
        for trial in np.arange(n_trials): 
            APs = APs_all[trial,idx]

            n_periods = tstop/1000 * f[idx]
            spikes_per_period[trial,idx] = np.size(APs)/n_periods
            
            
            (spikes_per_burst_tmp, start_burst_t, end_burst_t, 
                     single_mask, burst_mask) = get_bursts(APs, burst_len)
            n_bursts = np.sum(burst_mask)
            bursts_per_period[trial,idx] = n_bursts/n_periods

    # make new folder
    folder = folder + 'spikes_per_period/'
    if not os.path.exists(folder): os.makedirs(folder)
                       
    save_as_txt(folder,'spikes_per_period','mean: '+str(st.nanmean(spikes_per_period,0))+'\n'+'std: '+str(st.nanstd(spikes_per_period,0))) 
    save_as_txt(folder,'bursts_per_period','mean: '+str(st.nanmean(bursts_per_period,0))+'\n'+'std: '+str(st.nanstd(bursts_per_period,0))) 

    outfile = open(folder+'/spikes_per_period.npy', 'w') 
    np.save(outfile, spikes_per_period) 
    outfile = open(folder+'/bursts_per_period.npy', 'w') 
    np.save(outfile, bursts_per_period) 
    
    # plot stimulation vs burst ISI     
    if len(f)>1: df = np.diff(f)[0]
    else: df = 1
    fig, ax = pl.subplots(1)
    pl.errorbar(f, st.nanmean(spikes_per_period,0), st.nanstd(spikes_per_period,0), fmt='-o', color='k')
    plot_style(ax, 'Frequency of oscillatory inhibition (Hz)', 'Spikes per period (Hz)', [f[0]-df,f[-1]+df], [0,pl.ylim()[1]])
    if save: pl.savefig(folder+'/spikes_per_period.svg')

    # plot stimulation vs spikes per burst     
    fig, ax = pl.subplots(1)
    pl.errorbar(f, st.nanmean(bursts_per_period,0), st.nanstd(bursts_per_period,0), fmt='-o', color='k')
    plot_style(ax, 'Frequency of oscillatory inhibition (Hz)', 'Bursts per period', [f[0]-df,f[-1]+df], [0,pl.ylim()[1]])
    if save: pl.savefig(folder+'/bursts_per_period.svg')

# <codecell>


def plot_v(folder, f, tstop, dt, v_all, v_tuft_all):
       
    trial = 0
    t = np.arange(0,tstop,dt)
    
    # make new folder
    folder = folder + 'membrane_potential/'
    if not os.path.exists(folder): os.makedirs(folder)
    
    for idx in np.arange(np.size(f)): 
        v = v_all[trial,idx]
        v_tuft = v_tuft_all[trial,idx]
        
        # plot membrane potential soma and tuft
        fig, ax = pl.subplots(1)
        ax.plot(t, v, 'k', label='soma') 
        ax.plot(t, v_tuft, 'r', label='tuft')
        plot_style(ax, 'Time (ms)', 'Membrane potential (mV)', [0,1000], [], True)
        if save: pl.savefig(folder+'/v'+'_'+str(f[idx])+'.svg') 

# <codecell>


def plot_ISI(folder, f, tstop, dt, APs_all):
       
    trial = 0
    t = np.arange(0,tstop,dt)

    # make new folder
    folder = folder + 'ISI/'
    if not os.path.exists(folder): os.makedirs(folder)
    
    for idx in np.arange(np.size(f)): 
        APs = APs_all[trial,idx]

        # plot ISI
        if np.size(APs) > 1:
            ISI = np.diff(APs)
            fig, ax = pl.subplots(1)
            pl.hist(ISI,bins=np.arange(0,500,5),color='0.4')
            plot_style(ax, 'ISI (ms)', 'Number', [0,500], [0, pl.ylim()[1]])
            if save: pl.savefig(folder+'/ISI'+'_'+str(f[idx])+'.svg')

# <codecell>


def plot_ica(folder, f, tstop, dt, ica_all):
       
    trial = 0
    t = np.arange(0,tstop,dt)
    
    # make new folder
    folder = folder + 'calcium_current/'
    if not os.path.exists(folder): os.makedirs(folder)    
    
    for idx in np.arange(np.size(f)): 
        ica = ica_all[trial,idx]

        ## plot Calcium current
        fig, ax = pl.subplots(1)
        pl.plot(t, np.array(ica), 'k')
        plot_style(ax, 'Time (ms)', 'Calcium current in the tuft (nA)', [0, 1000], [])
        if save: pl.savefig(folder+'/ica'+'_'+str(f[idx])+'.svg') 

        pl.show() 

# <codecell>

## Analysis of spike trains
def analyse(folder, f, tstop, dt, n_trials, burst_len, v_all, v_tuft_all, APs_all, ica_all):
    compute_firing_rate(folder, f, n_trials, tstop, APs_all)
    compute_coherence(folder, f, n_trials, dt, burst_len, APs_all, v_tuft_all)  # does not work with f[i] = 0
    compute_percentage(folder, burst_len, f, n_trials, dt, APs_all, v_tuft_all)
    compute_spikes_per_period(folder, burst_len, f, n_trials, dt)  # does not work with f[i] = 0
    
    plot_v(folder, f, tstop, dt, v_all, v_tuft_all)
    plot_ISI(folder, f, tstop, dt, APs_all)
    plot_ica(folder, f, tstop, dt, ica_all)

# <codecell>


if __name__ == "__main__":
    # parameters
    save = True
    folder_data = '../../../simulation/singleneuron/data/'
    folder_name = 'Bahl2_lowfr_lowb'
    folder_data = folder_data + folder_name
    folder = folder_data + '/figures/'
    burst_len = 10 # ms

    # load parameters
    f = np.load(folder_data+'/f.npy')
    tstop = int(np.load(folder_data+'/tstop.npy'))
    dt = np.load(folder_data+'/dt.npy')
    n_trials = int(np.load(folder_data+'/n_trials.npy'))
    v_all = np.load(folder_data+'/v_all.npy')
    v_tuft_all = np.load(folder_data+'/v_tuft_all.npy')
    APs_all = np.load(folder_data+'/APs_all.npy')
    ica_all = np.load(folder_data+'/ica_all.npy')

    # run analysis
    analyse(folder, f, tstop, dt, n_trials, burst_len, v_all, v_tuft_all, APs_all, ica_all)



