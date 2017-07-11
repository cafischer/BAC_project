from __future__ import division
from general_functions.plotting import plot_style
from general_functions.saving import save_as_txt
import numpy as np
import pylab as pl
import os
from load_variables import load_params, load_pop, load_lfp
from analyses.functions import get_bursts, circ_median, circ_medtest, get_phases_fft


def medianphase(APs_all, lfp, n_cells, trial, freq, burst_len, cycles, df, tstop, dt):
    """computes the median phase for burst and single APs for each cell"""
    
    md_burst = np.zeros(n_cells)
    md_single = np.zeros(n_cells)
    burst_phases = np.array([])
    single_phases = np.array([])
    burst_phases_all = np.array([])
    
    # compute the length of the window for fft
    window_len_t_min = (1/freq) * cycles * 1000  # duration the window for smallest frequency
    window_len_min = int(window_len_t_min / dt)
    window_len = 1 / ((dt/1000) * df)  # window_len = 1 / ((dt/1000) * df)
    window_len_t = window_len * dt
    if window_len < window_len_min:  # window_len should contain at least n cycles of each frequency
        raise ValueError('Window for fft too small.')

    for cell in np.arange(n_cells): 
        # prune APs around which a window cannot be drawn
        APs = np.array(APs_all[cell, trial])
        APs = APs[APs < tstop-window_len_t]

        # divide APs in burst and single spike
        (spikes_per_burst, burst_APs, end_burst_t, single_mask, burst_mask) = get_bursts(APs, burst_len)
        burst_APs_all = APs[~single_mask]  # take all spikes from a burst
        single_APs = APs[single_mask]

        # compute spike-LFP phases
        burst_phases_tmp = get_phases_fft(burst_APs, freq, lfp, window_len, dt)
        single_phases_tmp = get_phases_fft(single_APs, freq, lfp, window_len, dt)
        burst_phases_all_tmp = get_phases_fft(burst_APs_all, freq, lfp, window_len, dt)

        # collect all phases
        burst_phases = np.concatenate((burst_phases, burst_phases_tmp))
        single_phases = np.concatenate((single_phases, single_phases_tmp))
        burst_phases_all = np.concatenate((burst_phases_all, burst_phases_all_tmp))

        # compute the median
        if len(burst_phases_tmp) > 2:
            md_burst[cell] = circ_median(burst_phases_tmp)
        else:
            md_burst[cell] = np.nan
        if len(burst_phases_tmp) > 2:
            md_single[cell] = circ_median(single_phases_tmp)
        else:
            md_single[cell] = np.nan
        
    return md_burst, md_single, burst_phases, single_phases, burst_phases_all

if __name__ == "__main__":

    folder = '../../simulation/network/data/Bahl2_testtransient/'
    pop = 'p2'
    folder_sav = folder + 'figures/phasedist/'+pop+'/'
    if not os.path.exists(folder_sav): os.makedirs(folder_sav)
    n_cells = 40
    freq = 12  # frequency at which the phases are determined
    trial = 0
    burst_len = 10

    # load data
    t, tstop, dt, onset, f, n_trials = load_params(folder)
    APs_all = load_pop(folder, pop, n_cells, trial+1)
    lfp = load_lfp(folder, n_trials, dt)
    lfp = lfp[0]
    cycles = 5  # number of cycles which should be enclosed by the window (for phase analysis)
    df = 0.5

    # compute the median phase of burst and single APs
    md_burst, md_single, burst_phases, single_phases, burst_phases_all = medianphase(APs_all, lfp, n_cells, trial,
                                                                                freq, burst_len, cycles, df, tstop, dt)

    np.savetxt(folder_sav+'md_burst_f'+str(freq)+'.txt', md_burst)
    np.savetxt(folder_sav+'md_single_f'+str(freq)+'.txt', md_single)

    # take the difference: burst phase - single phase
    md_diff = md_burst - md_single
    md_diff[md_diff > np.pi] = 2*np.pi - md_diff[md_diff > np.pi]
    md_diff[md_diff < -1*np.pi] += 2*np.pi

    # test for significance using a binomial test for circular data
    pval = circ_medtest(md_diff, 0)
    sig = pval < 0.05
    print 'Median of single and bursts APs significant different: ' + str(sig)
    np.savetxt(folder_sav+'Phasediff_sig_f'+str(freq), np.array([sig]))

    # histogram median phase difference
    fig, ax = pl.subplots(1)
    ax.hist(md_diff, bins=np.arange(-3.25, 3.25 + 0.25, 0.25), color='0.5')
    ax.plot(np.mean(md_diff), pl.ylim()[1]+10, 'vk', ms=20, label=pop)
    ax.axvline(x=0, ymin=0, ymax=1, color='k', linewidth=3)
    plot_style(ax, 'Phase difference of \n burst to single spike events (rad)', 'Number of cells',
               [-1*np.pi-0.25,np.pi+0.25], [0, pl.ylim()[1]])
    pl.xticks([-1*np.pi, -1*np.pi/2, 0, np.pi/2, np.pi], ['-pi', '-pi/2', '0', 'pi/2', 'pi'])
    leg = ax.legend(loc='upper right', numpoints=1, fontsize=20, frameon=False)
    leg.get_lines()[0]._legmarker.set_ms(10)
    pl.show()
    pl.savefig(folder_sav+'phasediff_f'+str(freq)+'.svg')

    # histogram of the median phase distribution burst and single
    fig, ax = pl.subplots(1)
    pl.hist(md_burst, bins=np.arange(-3.25, 3.25 + 0.25, 0.25), color='1.0', label='burst')
    pl.hist(md_single, bins=np.arange(-3.25, 3.25 + 0.25, 0.25), color='0.5', alpha=0.75, label='single \nspike')
    plot_style(ax, 'Distribution of the median phase (rad)', 'Number of cells',
               [-1*np.pi-0.25, np.pi+0.25], [0, pl.ylim()[1]+20], True)
    pl.xticks([-1*np.pi, -1*np.pi/2, 0, np.pi/2, np.pi], ['-pi', '-pi/2', '0', 'pi/2', 'pi'])
    pl.show()
    pl.savefig(folder_sav+'phasedist_f'+str(freq)+'.svg')

    # historgram phase distribution burst (events) and single averaged over all cells
    hist_burst, bins = np.histogram(burst_phases, bins=np.arange(-3.25, 3.25 + 0.25, 0.25),
                                    weights=np.ones(np.size(burst_phases))/n_cells)
    hist_single, bins = np.histogram(single_phases, bins=np.arange(-3.25, 3.25 + 0.25, 0.25),
                                    weights=np.ones(np.size(single_phases))/n_cells)
    hist_burst[0] = hist_burst[0]+hist_burst[-1]  # -pi and pi is the same
    hist_burst[-1] = hist_burst[0]
    hist_single[0] = hist_single[0]+hist_single[-1]  # -pi and pi is the same
    hist_single[-1] = hist_single[0]
    width = (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2

    fig, ax = pl.subplots(1)
    pl.bar(center, hist_burst, align='center', width=width, color='#fc8d59', label='burst')
    pl.bar(center, hist_single, align='center', width=width, color='#99d594', alpha=0.75, label='single \nspike')
    plot_style(ax, 'Distribution of the phase (rad)', 'Number of events',
               [-1*np.pi-0.25, np.pi+0.25], [0, pl.ylim()[1]+5], True)
    pl.xticks([-1*np.pi, -1*np.pi/2, 0, np.pi/2, np.pi], ['-pi', '-pi/2', '0', 'pi/2', 'pi'])
    pl.savefig(folder_sav+'Phases(events)_f'+str(freq)+'.svg')
    pl.show()

    # histogram phase distribution burst (spikes) and single averaged over all cells
    hist_burst_all, bins = np.histogram(burst_phases_all, bins=np.arange(-3.25, 3.25 + 0.25, 0.25),
                                    weights=np.ones(np.size(burst_phases_all))/n_cells)
    hist_burst_all[0] = hist_burst_all[0]+hist_burst_all[-1]  # -pi and pi is the same
    hist_burst_all[-1] = hist_burst_all[0]
    width = (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2

    fig, ax = pl.subplots(1)
    pl.bar(center, hist_burst_all, align='center', width=width, color='#fc8d59', label='burst')
    pl.bar(center, hist_single, align='center', width=width, color='#99d594', alpha=0.75, label='single \nspike')
    plot_style(ax, 'Distribution of the phase (rad)', 'Number of events',
               [-1*np.pi-0.25, np.pi+0.25], [0, pl.ylim()[1]+5], True)
    pl.xticks([-1*np.pi, -1*np.pi/2, 0, np.pi/2, np.pi], ['-pi', '-pi/2', '0', 'pi/2', 'pi'])
    pl.savefig(folder_sav+'Phases(spikes)_f'+str(freq)+'.svg')
    pl.show()