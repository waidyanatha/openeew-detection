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


def pga(x,y,z):
    '''
    Estimate the maximum value of acceleration of the three components
    x (numpy array) = signal  
    y (numpy array) = signal  
    z (numpy array) = signal  
    '''
    return (x**2 + y**2 + z**2)**0.5
    

    
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
