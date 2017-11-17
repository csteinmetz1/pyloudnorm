from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import test

def generate_high_freq_shelving_filter(G, fc, fs, plot=False):

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
        fig = plt.figure(figsize=(5,5))
        w, h = signal.freqz(b, a, worN=8000)
        plt.semilogx((fs * 0.5 / np.pi) * w, 20 * np.log10(abs(h)))
        plt.title('Pre-filter 1: High Shelving Filter')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Gain [dB]')
        plt.xlim([20, 20000])
        plt.ylim([-10,10])
        plt.grid(True, which='both')
        ax = plt.axes()
        ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
        plt.show()

    return b, a

def generate_high_pass_filter(fc, fs, plot=False):

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
        w, h = signal.freqz(b, a, worN=8000)    
        fig = plt.figure(figsize=(5,5))
        plt.semilogx((fs * 0.5 / np.pi) * w, 20 * np.log10(abs(h)))
        plt.title('Pre-filter 2: Highpass Filter')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Gain [dB]')
        plt.xlim([10, 20000])
        plt.ylim([-30,5])
        plt.grid(True, which='both')
        ax = plt.axes()
        ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
        plt.show()

    return b, a

def apply_K_filter(audio, fs, stage1_filter, stage2_filter):

    stage1_audio = signal.lfilter(stage1_filter[0], stage1_filter[1], audio)
    stage2_audio = signal.lfilter(stage2_filter[0], stage2_filter[1], stage1_audio)

    return stage2_audio

def loudness(audio, fs):
    """ Compute the loudness for a signal."""

    if len(audio.shape) == 1: # for mono input standardize shape
        audio = audio.reshape((audio.shape[0],1))

    numSamples  = audio.shape[0] # length of input in samples
    numChannels = audio.shape[1] # number of input channels

    # generate the two stages of filters
    stage1_filter = generate_high_freq_shelving_filter(4, 1680.0, fs)
    stage2_filter = generate_high_pass_filter(38.0, fs)

    # "K" Frequency Weighting - account for the acoustic respose of the head and auditory system
    for ch in range(numChannels):
        audio[:,ch] = apply_K_filter(audio[:,ch], fs, stage1_filter, stage2_filter)

    # Gating - ensures sections of silence or ambience do not skew the measurement

    G = [1.0, 1.0, 1.0, 1.41, 1.41] # channel gains
    T_g = 0.4 # 400 ms gating block
    Gamma_a = -70.0 # -70 LKFS = absolute loudness threshold
    overlap = 0.75 # overlap of 75% of the block duration
    step = 1 - overlap

    z = np.ndarray(shape=(numChannels,numSamples)) # instantiate array - trasponse of input
    T = numSamples / fs # length of the input in seconds
    j_range = np.arange(0, int(np.round((T - T_g) / (T_g * step))))

    for i in range(numChannels):
        for j in j_range:
            l = int(np.round(T_g * (j * step    ) * fs)) # lower bound of integration (in samples)
            u = int(np.round(T_g * (j * step + 1) * fs)) # upper bound of integration (in samples)
            z[i,j] = (1 / (T_g * fs)) * np.sum(np.square(audio[l:u,i])) # mean square and integrate
           
    l = [-0.691 + 10.0 * np.log10(np.sum([G[i] * z[i,j] for i in range(numChannels)])) for j in j_range]
    
    J_g = [j for j,l_j in enumerate(l) if l_j > Gamma_a]
    z_avg_gated = [np.mean([z[i,j] for j in J_g]) for i in range(numChannels)]
    Gamma_r = -0.691 + 10.0 * np.log10(np.sum([G[i] * z_avg_gated[i] for i in range(numChannels)])) - 10.0

    J_g = [j for j,l_j in enumerate(l) if (l_j > Gamma_a and l_j > Gamma_r)]
    z_avg_gated = [np.mean([z[i,j] for j in J_g]) for i in range(numChannels)]
    L_KG = -0.691 + 10.0 * np.log10(np.sum([G[i] * z_avg_gated[i] for i in range(numChannels)]))

    return L_KG
