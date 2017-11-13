from scipy import signal
import soundfile as sf
import math
import matplotlib.pyplot as plt
import numpy as np

# load audio data to be processed
xn = 

def high_freq_shelving_filter(G, fc, fs, Q):

    K = math.tan((np.pi * fc)/fs)
    V0 = 10**(G/20)
    root2 = 1.0/Q

    b0 = (V0 + root2*math.sqrt(V0)*K + K**2) / (1 + root2*K + K**2)
    b1 =                  ( 2 * (K**2 - V0)) / (1 + root2*K + K**2)
    b2 = (V0 - root2*math.sqrt(V0)*K + K**2) / (1 + root2*K + K**2)
    a1 =                    (2 * (K**2 - 1)) / (1 + root2*K + K**2)
    a2 =                (1 - root2*K + K**2) / (1 + root2*K + K**2)

    b = [b0, b1, b2]
    a = [0 , a1, a2]

    return b, a

def high_pass_filter(fs):
    pass

# create high shelving filter with fc = 1650 Hz

b = [1.53512485958697, -2.69169618940638, 1.19839281085285]
a = [0.0, -1.69065929318241, 0.73248077421585]

# apply the filter
#zi = singal.lfilter_zi(b, a)
#z, _ = signal.lfilter(b, a, xn, zi=zi*xn[0])

def loudness(signal, fs):
    """ Compute the loudness for a signal."""
    
    b, a = high_freq_shelving_filter(4, 1650, fs, 2.0)

    stage1 = signal.lfilter(b, a, signal)

    b, a = high_pass_filter()