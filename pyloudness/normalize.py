from __future__ import division
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from textwrap import dedent
import scipy.signal

class IIRfilter():
    """ IIR Filter object to perform 2-stage pre-filtering
    
    This class generates a high shelf or high pass filter as described 
    in ITU-R 1770-4 (see pg. 3-4 of the standard). 

    Parameters
    ----------
    G : float
        Gain of the filter in dB.
    Q : float
        Q of the filter.
    fc : float
        Center frequency of the shelf in Hz.
    fs : float
        Sampling rate in Hz.
    filter_type: str
        Shape of the filter.
    """

    def __init__(self, G, Q, fc, fs, filter_type):
        self.G  = G
        self.Q  = Q
        self.fc = fc
        self.fs = fs
        self.filter_type = filter_type
        self.valid_types = {'high_shelf' : 'High Shelf Filter', 'high_pass' : 'High Pass Filter'}
        if self.filter_type not in self.valid_types:
            raise ValueError("Invalid filter type. Valid types: {valid_types}".format(valid_types=self.valid_types.keys()))
        self.b, self.a = self.generate_filter_coefficients()

    def __repr__(self):
        info = ("""
        {type}
        ----------------------
        Gain         = {G} dB
        Q factor     = {Q} 
        Center freq. = {fc} Hz
        Sample rate  = {fs} Hz
        ----------------------
        b0 = {_b0}
        b1 = {_b1}
        b2 = {_b2}
        a0 = {_a0}
        a1 = {_a1}
        a2 = {_a2}
        ----------------------
        """).format(type=self.valid_types[self.filter_type], 
        G=self.G, Q=self.Q, fc=self.fc, fs=self.fs, 
        _b0=self.b[0], _b1=self.b[1], _b2=self.b[2], 
        _a0=self.a[0], _a1=self.a[1], _a2=self.a[2])

        return dedent(info)

    def generate_filter_coefficients(self):
        """ Generates biquad filter coefficients using instance filter parameters. 

        This method is called whenever an IIRFilter is instantiated and then sets
        the coefficients for the filter instance. NOTE: Changing the IIRFilter 
        instance filter paramters will not update the filter coefficents unless
        this method is called after the modification. 

        Returns
        -------
        b : ndarray
            Numerator filter coefficients stored as [b0, b1, b2]
        a : ndarray
            Denominator filter coefficients stored as [a0, a1, a2]
        """
        A  = np.sqrt(10**(self.G/20.0))
        w0 = 2.0 * np.pi * (self.fc / self.fs)
        alpha = np.sin(w0) / (2.0 * self.Q)

        if self.filter_type == 'high_shelf':
            b0 =      A * ( (A+1) + (A-1) * np.cos(w0) + 2 * np.sqrt(A) * alpha )
            b1 = -2 * A * ( (A-1) + (A+1) * np.cos(w0)                          )
            b2 =      A * ( (A+1) + (A-1) * np.cos(w0) - 2 * np.sqrt(A) * alpha )
            a0 =            (A+1) - (A-1) * np.cos(w0) + 2 * np.sqrt(A) * alpha
            a1 =      2 * ( (A-1) - (A+1) * np.cos(w0)                          )
            a2 =            (A+1) - (A-1) * np.cos(w0) - 2 * np.sqrt(A) * alpha
        else: # high pass filter
            b0 =  (1 + np.cos(w0))/2
            b1 = -(1 + np.cos(w0))
            b2 =  (1 + np.cos(w0))/2
            a0 =   1 + alpha
            a1 =  -2 * np.cos(w0)
            a2 =   1 - alpha

        return np.array([b0, b1, b2])/a0, np.array([a0, a1, a2])/a0

    def plot_magnitude(self):
        """ Plot the magnitude response of the filter.

        This method is provided for debuging and validation of the 
        generated filter coefficients. These plots should match those
        as outlined in the ITU-R 1770-4 standard. 

        """
        fig = plt.figure(figsize=(9,9))
        w, h = signal.freqz(self.b, self.a, worN=8000)
        plt.semilogx((self.fs * 0.5 / np.pi) * w, 20 * np.log10(abs(h)))
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Gain [dB]')
        if self.filter_type == 'high_shelf':
            plt.title('Pre-filter 1: High Shelving Filter')
            plt.xlim([20, 20000])
            plt.ylim([-10,10])
            plt.grid(True, which='both')
            ax = plt.axes()
            ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
        else:
            plt.title('Pre-filter 2: Highpass Filter')
            plt.xlim([10, 20000])
            plt.ylim([-30,5])
            plt.grid(True, which='both')
            ax = plt.axes()
            ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
        plt.show()

    def apply_filter(signal):
        """ Apply the IIR filter to an input signal.

        Params
        -------
        signal : ndarrary
            Input audio data.

        Returns
        -------
        filtered_signal : ndarray
            Filtered input audio.
        """
        return scipy.signal.lfilter(self.b, self.a, signal)
    
def measure_gated_loudness(signal, fs):
    """ Measure the gated loudness of a signal.
    
    Following the four stage process outlined in the ITU-R 1770-4 standard,
    this method calculates the gated loundess of a signal in LKFS or the
    K-weighted full-scale loudness.   

    Params
    -------
    signal : ndarray
        Input multichannel audio data.
    fs : int
        Sampling rate of the input audio in Hz. 

    Returns
    -------
    L_KG : float
        Gated loudness of the input measured in LKFS.

    Examples
    --------
    >>> from pyloudnorm import normalize
    """

    if len(signal.shape) == 1: # for mono input standardize shape
        signal = signal.reshape((signal.shape[0],1))

    numSamples  = signal.shape[0] # length of input in samples
    numChannels = signal.shape[1] # number of input channels

    # generate the two stages of filters
    stage1_filter = IIRfilter(1/np.sqrt(2), 1680, fs, 'high_shelf', G=4.0)
    stage2_filter = IIRfilter(0.5, 38, fs, 'high_pass')

    # NOTE: Every call to measure_gated_loudness() results in the creation of 
    # filter objects. This allows for the input 

    # "K" Frequency Weighting - account for the acoustic respose of the head and auditory system
    for ch in range(numChannels):
        signal[:,ch] = stage1_filter.apply_filter(signal[:,ch])
        signal[;,ch] = stage2_filter.apply_filter(signal[:,ch])

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
            z[i,j] = (1 / (T_g * fs)) * np.sum(np.square(signal[l:u,i])) # mean square and integrate
           
    l = [-0.691 + 10.0 * np.log10(np.sum([G[i] * z[i,j] for i in range(numChannels)])) for j in j_range]
    
    J_g = [j for j,l_j in enumerate(l) if l_j > Gamma_a]
    z_avg_gated = [np.mean([z[i,j] for j in J_g]) for i in range(numChannels)]
    Gamma_r = -0.691 + 10.0 * np.log10(np.sum([G[i] * z_avg_gated[i] for i in range(numChannels)])) - 10.0

    J_g = [j for j,l_j in enumerate(l) if (l_j > Gamma_a and l_j > Gamma_r)]
    z_avg_gated = [np.mean([z[i,j] for j in J_g]) for i in range(numChannels)]
    L_KG = -0.691 + 10.0 * np.log10(np.sum([G[i] * z_avg_gated[i] for i in range(numChannels)]))

    return L_KG
