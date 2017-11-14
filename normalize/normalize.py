from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def high_freq_shelving_filter(G, fc, fs, plot=False):

    Q = 1.0 / np.sqrt(2.0)
    A  = np.sqrt(10**(G/20.0))
    w0 = w0 = 2.0 * np.pi * (fc / fs)
    
    alpha = np.sin(w0) / (2 * Q)
    
    b0 =      A * ( (A+1) + (A-1) * np.cos(w0) + 2 * np.sqrt(A) * alpha )
    b1 = -2 * A * ( (A-1) + (A+1) * np.cos(w0)                          )
    b2 =      A * ( (A+1) + (A-1) * np.cos(w0) - 2 * np.sqrt(A) * alpha )
    a0 =            (A+1) - (A-1) * np.cos(w0) + 2 * np.sqrt(A) * alpha
    a1 =      2 * ( (A-1) - (A+1) * np.cos(w0)                          )
    a2 =            (A+1) - (A-1) * np.cos(w0) - 2 * np.sqrt(A) * alpha

    b = [b0, b1, b2]
    a = [a0, a1, a2]

    if plot:
        fig = plt.figure(figsize=(9,9))
        ax1 = fig.add_subplot(111)
        w, h1 = signal.freqz(b, a, worN=8000)
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

    return b, a

def high_pass_filter(fc, fs, plot=False):

    Q  = 0.5
    w0 = 2.0 * np.pi * (fc / fs)

    alpha = np.sin(w0) / (2 * Q)

    b0 =  (1 + np.cos(w0))/2
    b1 = -(1 + np.cos(w0))
    b2 =  (1 + np.cos(w0))/2
    a0 =   1 + alpha
    a1 =  -2 * np.cos(w0)
    a2 =   1 - alpha

    b = [b0, b1, b2]
    a = [a0, a1, a2]

    if plot:
        fig = plt.figure(figsize=(9,9))
        ax1 = fig.add_subplot(111)
        w, h2 = signal.freqz([b0,b1,b2], [a0,a1,a2], worN=8000)
        plt.semilogx((fs * 0.5 / np.pi) * w, 20*np.log10(abs(h2)))
        plt.title('Pre-filter 2')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Gain [dB]')
        plt.xlim([10, 20000])
        plt.ylim([-30,5])
        plt.grid(True, which='both')
        ax = plt.axes()
        ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
        plt.show()

    return b, a

def loudness(audio, fs):
    """ Compute the loudness for a signal."""
    
    # Perform "K" frequency weighting
    b, a = high_freq_shelving_filter(4, 1680.0, fs)
    stage1 = signal.lfilter(b, a, audio)

    b, a = high_pass_filter(38.0, fs)
    stage2 = signal.lfilter(b, a, stage1)
