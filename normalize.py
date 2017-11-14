from scipy import signal
import soundfile as sf
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# load audio data to be processed

def high_freq_shelving_filter(G, fc, fs):

    Q = 0.7071752369554193
    K = math.tan((np.pi * fc)/fs)
    V0 = 10**(G/20.0)
    root2 = 1.0/Q

    b0 = (V0 + root2*math.sqrt(V0)*K + K**2) / (1 + root2*K + K**2)
    b1 =                  ( 2 * (K**2 - V0)) / (1 + root2*K + K**2)
    b2 = (V0 - root2*math.sqrt(V0)*K + K**2) / (1 + root2*K + K**2)
    a1 =                    (2 * (K**2 - 1)) / (1 + root2*K + K**2)
    a2 =                (1 - root2*K + K**2) / (1 + root2*K + K**2)

    print b0
    print b1

    b = [b0, b1, b2]
    a = [1.0, a1, a2]

    return b, a

def high_pass_filter(fs):
    pass

# create high shelving filter with fc = 1650 Hz

#b = [1.53512485958697, -2.69169618940638, 1.19839281085285]
#a = [0.0, -1.69065929318241, 0.73248077421585]

# apply the filter
#zi = singal.lfilter_zi(b, a)
#z, _ = signal.lfilter(b, a, xn, zi=zi*xn[0])

def loudness(input, fs, plot=False):
    """ Compute the loudness for a signal."""
    
    b, a = high_freq_shelving_filter(4, 1680, fs)
    
    #stage1 = signal.lfilter(b, a, signal)

    #b = [1.53512485958697, -2.69169618940638, 1.19839281085285]
    #a = [1.0, -1.69065929318241, 0.73248077421585]

    if plot == True:
        fig = plt.figure(figsize=(9,9))
        ax1 = fig.add_subplot(111)
        w, h1 = signal.freqz(b, a, worN=8000)#np.logspace(-4, 3, 2000))
        plt.semilogx((fs * 0.5 / np.pi) * w, 20*np.log10(abs(h1)))
        plt.title('Pre-filter 1')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Gain [dB]')
        plt.xlim([20, 20000])
        plt.ylim([-10,10])
        plt.grid(True, which='both')
        ax = plt.axes()
        ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
        plt.show()

    b, a = high_pass_filter()

loudness(None, 48000, True)