from __future__ import division
import numpy as np
from scipy.signal import butter, lfilter
from scipy.stats import binom

# <headingcell level=1>

# identify bursts

# <codecell>

def get_bursts(APs, burst_len):  
    """computes the number of spikes for each burst by counting the number of ISIs smaller than the burst length
    Output
    single_mask  marks all single APs as true
    burst_mask   marks the first AP in a burst as true"""
    
    val_tmp = False
    spikes_per_burst = []
    start_burst = []
    end_burst = []
    start_burst_t = []
    end_burst_t = []
    burst_mask = np.zeros(np.size(APs), dtype=bool)
    single_mask = np.zeros(np.size(APs), dtype=bool)
    
    if np.size(APs) > 1:
        ISI = np.diff(APs)
        ISI = np.append(ISI, ISI[-1]+burst_len+1) # append an ISI longer than burst length to classify the last AP 

        for i,val in enumerate(ISI < burst_len):
            if val_tmp == False and val == True:
                counter = 1
                start_burst.append(i)
                burst_mask[i] = True
            elif val_tmp == True and val == True:
                counter += 1
            elif val_tmp == True and val == False:
                counter += 1
                end_burst.append(i)
                spikes_per_burst.append(counter)
                counter = 0
            else: single_mask[i] = True
            val_tmp = val
        start_burst = start_burst[0:len(end_burst)] # if there is no spike end delete the start

        start_burst_t = APs[start_burst] 
        end_burst_t = APs[end_burst]

    return spikes_per_burst, start_burst_t, end_burst_t, single_mask, burst_mask

# <codecell>

def identify_bursts(APs, v_tuft, burst_len, dt):
    """Finds single spikes and bursts from AP times and divides bursts in BACs, FACs and others
    Outp
    mask  true at the first AP in the corresponding burst
    """
    
    # find the times of burst APs
    (spikes_per_burst, start_burst_t, end_burst_t,  
         single_mask, burst_mask) = get_bursts(APs, burst_len)

    n_bursts = np.size(start_burst_t)

    if n_bursts > 0: # if there are bursts
        start_burst_idx = np.round((start_burst_t)/dt).astype(int)
        end_burst_idx = np.round((end_burst_t)/dt).astype(int)
        start_burst_del_idx = np.round((start_burst_t+5)/dt).astype(int) # time of the first burst +5 ms

        # Plateau potential in the tuft
        burst_plateau = np.zeros(n_bursts, dtype=bool)
        for i in np.arange(n_bursts):
            if np.all(v_tuft[start_burst_del_idx[i]:end_burst_idx[i]] > -40): # -40 is the threshold for a Calcium spike
                burst_plateau[i] = True # value per burst indicating if plateau potential was present
            else: 
                burst_plateau[i] = False
        burst_plateau = burst_plateau[0:len(start_burst_idx)]

        # BP 
        BP = v_tuft[start_burst_idx] <= -20 # -20 is the AP threshold

        # BAC: BP and plateau potential
        BAC = BP & burst_plateau
        BAC_mask = np.zeros(np.size(burst_mask), dtype=bool)
        BAC_mask[burst_mask] = BAC

        # FAC: FP and plateau potential
        FAC = np.logical_not(BP) & burst_plateau
        FAC_mask = np.zeros(np.size(burst_mask), dtype=bool)
        FAC_mask[burst_mask] = FAC

        # Other bursts: not plateau potential
        other_burst = np.logical_not(burst_plateau) 
        other_burst_mask = np.zeros(np.size(burst_mask), dtype=bool)
        other_burst_mask[burst_mask] = other_burst

        return BAC_mask, FAC_mask, other_burst_mask, single_mask, burst_mask
    
    return (np.zeros(np.size(APs), dtype=bool), np.zeros(np.size(APs), dtype=bool), np.zeros(np.size(APs), dtype=bool), 
            np.zeros(np.size(APs), dtype=bool), np.zeros(np.size(APs), dtype=bool))

# <codecell>

def get_APs_kind(kind, APs_all, n_cells, n_trials, burst_len, dt, folder='', pop=''):
    
    APs_kind = np.zeros([n_cells,n_trials], dtype=object)
    
    for cell in np.arange(n_cells): 
        for trial in np.arange(n_trials):   
            
            if kind == 'burst':
                (spikes_per_burst, APs_burst, end_burst_t,
                    single_mask, burst_mask) = get_bursts(APs_all[cell,trial], burst_len)
                APs_kind[cell,trial] = APs_all[cell,trial][burst_mask]
                
            elif kind == 'single':
                (spikes_per_burst, APs_burst, end_burst_t,
                    single_mask, burst_mask) = get_bursts(APs_all[cell,trial], burst_len)
                APs_kind[cell,trial] = APs_all[cell,trial][single_mask]
                
            elif kind == 'BAC':
                v_tuft = np.load(folder+'trial'+str(trial)+'/v_tuft_'+pop+'.npy') 
                (BAC_mask, FAC_mask, other_burst_mask, single_mask, burst_mask) = identify_bursts(APs_all[cell, trial],
                                                                                v_tuft[cell, :], burst_len, dt)
                APs_kind[cell,trial] = APs_all[cell,trial][BAC_mask]
                
            elif kind == 'FAC':
                v_tuft = np.load(folder+'trial'+str(trial)+'/v_tuft_'+pop+'.npy') 
                (BAC_mask, FAC_mask, other_burst_mask, single_mask, burst_mask) = identify_bursts(APs_all[cell,trial], 
                                                                                v_tuft[cell,:], burst_len, dt)
                APs_kind[cell,trial] = APs_all[cell,trial][FAC_mask]
                
            elif kind == 'other_burst':
                v_tuft = np.load(folder+'trial'+str(trial)+'/v_tuft_'+pop+'.npy') 
                (BAC_mask, FAC_mask, other_burst_mask, single_mask, burst_mask) = identify_bursts(APs_all[cell,trial], 
                                                                                v_tuft[cell,:], burst_len, dt)
                APs_kind[cell,trial] = APs_all[cell,trial][other_burst_mask]
                
            else: raise ValueError("Kind is not available!")

    return APs_kind

# <codecell>

def percentage_burst(APs, v_tuft, burst_len, dt):
    
    BAC_mask, FAC_mask, other_burst_mask, single_mask, burst_mask = identify_bursts(APs, v_tuft, burst_len, dt)
    n_bursts = np.sum(burst_mask)
    n_single = np.sum(single_mask)

    if n_single == 0 and n_bursts == 0:
        return np.nan,np.nan, np.nan, np.nan
    else:
        # Percent BAC, FAC, others
        BAC_percent = np.sum(BAC_mask) / (n_bursts+n_single)*100
        FAC_percent = np.sum(FAC_mask) / (n_bursts+n_single)*100
        other_burst_percent = np.sum(other_burst_mask) / (n_bursts+n_single)*100

        # Percent bursting
        burst_percent = n_bursts/(n_bursts+n_single)*100

        return BAC_percent, FAC_percent, other_burst_percent, burst_percent

# <headingcell level=1>

# Phases

# <codecell>

def get_phases_freq(APs, freq):
    """computes the phase for each AP with respect to the given frequency
    Input:
    APs  time of APs (ms)
    f    frequency with respect to which phases are computed (Hz)"""
    
    phases = APs % (1.0/freq*1000) # bring all spiketimes in one period
    phases = phases * 2*np.pi*freq/1000 # multiplication by the angular frequency puts it in the interval [0,2pi]
        
    return phases

# <codecell>

def get_phases_fft(APs, freq, lfp, window_len, dt):
    """computes the phase of the lfp corresponding to the APs for the given freq
    Input: 
    window_len length of the whole window as idx"""
   
    taper = np.hanning(window_len) # hanning window
    phases = np.zeros(len(APs))

    for i,AP in enumerate(APs):
        AP_idx = np.round(AP/dt)

        # extract lfp around the AP and taper
        if AP_idx+window_len > lfp.size: 
            raise ValueError('AP does not respect window size.')
        else: 
            lfp_window = lfp[AP_idx:AP_idx+window_len] * taper

        # fft
        lfp_fft = np.fft.fft(lfp_window) 
        freqs = np.fft.fftfreq(np.size(lfp_window), d=dt/1000)

        # check that wanted frequency is present
        if not np.any(freqs == freq):
            raise ValueError('Wanted frequency is not contained in the fft transformed signal.')

        # extract the phase
        phases[i] = np.angle(lfp_fft)[freqs == freq]

    return phases

# <codecell>
# circular statistics

def circ_r(phases):
    """Computes mean resultant vector length for circular data.
    Input:
      alpha sample of angles in radians
    Output:
      r mean resultant length """

    # length of the vector containing the weighted sum of cos and sin of angles
    r = np.abs(np.sum(np.exp(1j*phases))) / np.size(phases)

    return r 

def circ_dist(x,y):
    """
    Pairwise difference x_i-y_i around the circle computed efficiently.

    :param x: sample of linear random variable
    :type x:
    :param y: sample of linear random variable or one single angle
    :type y:
    :return: matrix with differences
    :rtype:

    References:
    Biostatistical Analysis, J. H. Zar, p. 651

    Circular Statistics Toolbox for Matlab

    By Philipp Berens, 2009
    berens@tuebingen.mpg.de - www.kyb.mpg.de/~berens/circStat.html
    """

    return np.angle(np.exp(1j*x) / np.exp(1j*y))


def circ_dist2(x, y=None):
    """
    All pairwise difference x_i-y_j around the circle computed efficiently.

    :param x: sample of linear random variable
    :type x:
    :param y: sample of linear random variable
    :type y:
    :return: matrix with pairwise differences
    :rtype:

    References:
    Biostatistical Analysis, J. H. Zar, p. 651

    Circular Statistics Toolbox for Matlab

    By Philipp Berens, 2009
    berens@tuebingen.mpg.de - www.kyb.mpg.de/~berens/circStat.html
    """

    if y is None:
        y = x
    x = np.array([x]).T

    return np.angle(np.tile(np.exp(1j*x), (1, len(y))) / np.tile(np.exp(1j*y), (len(x), 1)))


def circ_mean(alpha, w=None):
    """
    Computes the mean direction for circular data.

    :param alpha: sample of angles in radians
    :type alpha: array-like
    :param w: weightings in case of binned angle data
    :type w: array-like
    :return: mean direction
    :rtype: float

    References:
    Statistical analysis of circular data, N. I. Fisher
    Topics in circular statistics, S. R. Jammalamadaka et al.
    Biostatistical Analysis, J. H. Zar

    Circular Statistics Toolbox for Matlab

    By Philipp Berens, 2009
    berens@tuebingen.mpg.de - www.kyb.mpg.de/~berens/circStat.html
    """

    if w is None:
        w = np.ones(np.size(alpha))

    # compute weighted sum of cos and sin of angles
    r = np.sum(w*np.exp(1j*alpha))

    return np.angle(r)

def circ_median(alpha):
    """
    Computes the median direction for circular data.

    :param alpha: sample of angles in radians
    :type alpha: array-like
    :return: mu mean direction
    :rtype: float

    References:
    Biostatistical Analysis, J. H. Zar (26.6)

    Circular Statistics Toolbox for Matlab

    By Philipp Berens, 2009
    berens@tuebingen.mpg.de - www.kyb.mpg.de/~berens/circStat.html
    """

    alpha = np.mod(alpha, 2*np.pi)

    dd = circ_dist2(alpha, alpha)
    dd = np.round(dd, 5)  # important that some values are recognized as zero for comparison operation
    m1 = np.sum(dd >= 0, 0)
    m2 = np.sum(dd <= 0, 0)

    dm = np.abs(m1-m2)
    m = np.min(dm)
    idx = np.where(dm == dm.min())

    if m > 1:
        raise Warning('Ties detected.')

    md = circ_mean(alpha[idx])  # in case of an even number of phases take the mean between the minima

    if abs(circ_dist(circ_mean(alpha), md)) > abs(circ_dist(circ_mean(alpha), md+np.pi)):
        md = np.mod(md+np.pi, 2*np.pi)

    return md

def get_coherence(APs, freq):
    """computes the phase coherence"""
    if APs.size < 5: # if there are less than 10 spikes the measure is unreliable
        return np.nan
    else:
        phases = get_phases_freq(APs, freq)
        coherence = circ_r(phases)
        return coherence 

# <codecell>

def circ_medtest(alpha, md):
    """Tests for significance of the median.
    H0: the population has median angle md
    H1: the population has not median angle md 
    
    Input:
    alpha sample of angles in radians
    md    median to test for

    Output:
    pval  p-value """

    if np.size(md) > 1:
      raise ValueError('Median can only be a single value.')

    n = np.size(alpha)

    # compute deviations from median
    d = np.angle(np.exp(1j*alpha) / np.exp(1j*md))

    n1 = np.sum(d < 0)
    n2 = np.sum(d > 0)

    # compute p-value with binomial test
    x = np.concatenate([np.arange(0, np.min([n1,n2])+1), np.arange(np.max([n1, n2]), n+1)])
    pval = np.sum(binom.pmf(x, n, 0.5))

    return pval

# <headingcell level=1>

# PPC

# <codecell>

def get_PPC(phases):
    """calculates the PPC (pairwise phase consistency) of the APs for the given frequencies
    Input:
    phases  phases should be grouped by trial"""
    
    PPC = 0
    fac = 0

    for m in np.arange(np.shape(phases)[0]):
        for n in np.arange(np.shape(phases)[0]):
            if m!=n:
                for i in np.arange(np.size(phases[m])):
                    for j in np.arange(np.size(phases[n])):
                        PPC = PPC + np.cos(phases[m][i]-phases[n][j])
                fac = fac + np.size(phases[m]) * np.size(phases[n])

    PPC = 1/fac * PPC 
                
    return PPC

# <codecell>

def APsLFP2PPC(freq, APs_all, lfp, n_trials, min_APs, cycles, tstop, dt):
    """computes the PPC from the given APs and LFPs"""

    phases = np.zeros([n_trials], dtype=object)

    for trial in np.arange(n_trials):

        # compute the length of the window
        window_len_t = (1/freq) * cycles * 1000  # duration of half the window
        window_len = int(window_len_t / dt)

        # prune APs around which a window cannot be drawn
        APs = np.array(APs_all[trial])
        APs = APs[APs<tstop-window_len_t]

        # compute the phases
        if np.size(APs) < min_APs:  # check if the minimal number of APs is fulfilled
            phases[trial] = np.nan
            print 'Not enough APs for analysis!'+' Trial: '+str(trial)
        else: 
            phases[trial] = get_phases_fft(APs, freq, lfp[trial], window_len, dt)

    # PPC
    if np.any(isnan_special(phases)):
        PPC = np.nan
    else:
        PPC = get_PPC(phases)

    return PPC

# <codecell>

def get_PPC_kind(kind, APs_all, lfp, n_cells, n_trials, f, burst_len, min_APs, cycles, tstop, dt, folder='', pop=''):
    """computes the PPC from APs of the specified kind"""

    PPC_kind = np.zeros([n_cells, np.size(f)])

    # get APs of the specified kind
    if kind == 'all':
        APs_kind = APs_all
    else:
        APs_kind = get_APs_kind(kind, APs_all, n_cells, n_trials, burst_len, dt,  folder, pop)
    
    for cell in np.arange(n_cells): 
         for idx, freq in enumerate(f): 
            # compute PPC
            PPC_kind[cell, idx] = APsLFP2PPC(freq, APs_kind[cell, :], lfp, n_trials, min_APs, cycles, tstop, dt)

    return PPC_kind

# <codecell>

def get_PPC_rand(APs_kind, lfp_phases, n_cells, n_trials, f, burst_len, min_APs, cycles, tstop, dt, folder='', pop=''):
    """computes the PPC from APs of the specified kind"""
            
    PPC = np.zeros([n_cells, np.size(f)])    
    
    for cell in np.arange(n_cells): 
         for idx, freq in enumerate(f): 
                phases = np.zeros([n_trials], dtype=object)
                for trial in np.arange(n_trials):
                    # compute the length of the window
                    window_len_t = (1/freq) * cycles * 1000 # duration of half the window
                    window_len = int(window_len_t / dt)
    
                    # prune APs around which a window cannot be drawn (to have later the same number of APs)
                    APs = np.array(APs_kind[cell,trial])
                    APs = APs[APs<tstop-window_len_t]

                    # compute phases
                    if np.size(APs) < min_APs: # check if the minimal number of APs is fulfilled
                        phases[trial] = np.nan
                        print 'Not enough APs for analysis!'+' Trial: '+str(trial)
                    else:
                        phases_tmp = np.zeros(len(APs))
                        for i,AP in enumerate(APs):
                            # give each AP a random lfp window
                            r = np.random.randint(0,np.size(lfp_phases[trial,idx])) # r is a random number that choses a phase from the lfp recording
                            phases_tmp[i] = lfp_phases[trial,idx][r]
                        phases[trial] = phases_tmp

                # PPC
                if np.any(isnan_special(phases)):
                    PPC[cell,idx] = np.nan
                else:
                    PPC[cell,idx] = get_PPC(phases)
                    
    return PPC

# <codecell>

def get_PPC_rand2(n_APs, lfp_phases, n_cells, n_trials, f):
    """computes the PPC from APs of the specified kind"""
            
    PPC = np.zeros([n_cells, np.size(f)])    
    
    for cell in np.arange(n_cells): 
         for idx, freq in enumerate(f): 
                phases = np.zeros([n_trials], dtype=object)
                for trial in np.arange(n_trials):
                    # choose random phases from the lfp
                    rand = np.random.randint(0,np.size(lfp_phases[trial,idx]), n_APs)
                    phases[trial] = lfp_phases[trial,idx][rand]

                # compute PPC
                PPC[cell,idx] = get_PPC(phases)
                    
    return PPC

# <codecell>

def isnan_special(arr):
    for i in arr:
        if np.size(i)==1:
            if np.isnan(i):
                return True
    return False

# <headingcell level=1>

# Filter

# <codecell>

def lowpass(data, samprate, cutoff, order=1):
    """low-pass butterworth filter"""
    
    b,a = butter(order, cutoff/(samprate/2.0), btype='low', analog=0, output='ba')
    data_f = lfilter(b, a, data)
    return data_f

# <codecell>

def bandpass(data, samprate, lowcut, highcut, order=1):
    """band-pass butterworth filter"""
    lowcut = lowcut/(samprate/2.0)
    highcut = highcut/(samprate/2.0)
    
    b,a = butter(order, [lowcut, highcut], btype='band', analog=False, output='ba')
    data_f = lfilter(b, a, data)
    return data_f

