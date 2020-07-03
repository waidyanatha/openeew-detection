# =============================================================================
# This script computes the standard STA/LTA from a given input array x. 
#   The length of the STA is given by nsta in samples, respectively is the length of the
#   LTA given by nlta in samples. 
#
#    x (numpy array) = Signal  
#    nsta (integer) = Length of short time average window in samples
#    nlta (integer) = Length of long time average window in samples
#    return = Function of classic STA/LTA
# =============================================================================

import numpy as np

def sta_lta(x, nsta, nlta):
    """
    Computes the standard STA/LTA from a given input array x. 
    The length of the STA is given by nsta in samples, respectively is the length of the
    LTA given by nlta in samples. 

    x (numpy array) = signal  
    nsta (integer) = length of short time average window in samples
    nlta (integer) = length of long time average window in samples
    return = function of classic STA/LTA
    """
    # Cumulative sum 
    sta = np.cumsum(x ** 2)

    # Convert to float
    sta = np.require(sta, dtype=np.float)

    # Copy for LTA
    lta = sta.copy()

    # Compute the STA and the LTA
    sta[nsta:] = sta[nsta:] - sta[:-nsta]
    sta /= nsta
    lta[nlta:] = lta[nlta:] - lta[:-nlta]
    lta /= nlta
    
    # Pad zeros
    sta[:nlta - 1] = 0

    # Avoid division by zero by setting zero values to tiny float
    dtiny = np.finfo(0.0).tiny
    idx = lta < dtiny
    lta[idx] = dtiny

    return sta / lta

    
def trigger_time(function, t, trig_level):
    '''
    Estimate the time where the function exceeds a given trigger level
    function (numpy array) = classical earthquake detection function (i.e. STA/LTA, PGA)
    t (numpy array) = time of signal
    trig_level (float) = trigger level 
    return = times when the trigger level is exceeded
    '''
    index = np.argwhere(function >= trig_level)
    
    return t[index] 
