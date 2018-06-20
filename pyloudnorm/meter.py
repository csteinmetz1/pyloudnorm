from __future__ import division
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from textwrap import dedent
import scipy.signal
import warnings
from . import util

class Meter():
    """ Meter object which defines how the meter operates

    Defaults to the algorithm defined in ITU-R BS.1770-4.

    Parameters
    ----------
    rate : float
        Sampling rate in Hz.
    filter_class : str
        Class of weigthing filter used.
        - 'K-weighting'
        - 'Fenton/Lee 1'
        - 'Fenton/Lee 2'
        - 'Dash et al.'
    block_size : float
        Gating block size in seconds.
    """

    def __init__(self, rate, filter_class="K-weighting", block_size=0.400):

        self.rate = rate
        self.filter_class = filter_class
        self.block_size = block_size
        self.filters = {} # dict to store frequency weighting filters

        if   filter_class == "K-weighting":
            self.filters['high_shelf'] = IIRfilter(4.0, 1/np.sqrt(2), 1500.0, rate, 'high_shelf')
            self.filters['high_pass'] = IIRfilter(0.0, 0.5, 38.0, rate, 'high_pass')
        elif filter_class == "Fenton/Lee 1":
            self.filters['high_shelf'] = IIRfilter(5.0, 1/np.sqrt(2), 1500.0, rate, 'high_shelf')
            self.filters['high_pass'] = IIRfilter(0.0, 0.5, 130.0, rate, 'high_pass')
            self.filters['peaking'] = IIRfilter(0.0, 1/np.sqrt(2), 500.0, rate, 'peaking')
        elif filter_class == "Fenton/Lee 2": # not yet implemented 
            self.stage1_filter = IIRfilter(4.0, 1/np.sqrt(2), 1500.0, rate, 'high_shelf')
            self.stage2_filter = IIRfilter(0.0, 0.5, 38.0, rate, 'high_pass')
        elif filter_class == "Dash et al.":
            self.filters['high_pass'] = IIRfilter(0.0, 0.375, 149.0, rate, 'high_pass')
            self.filters['notch'] = IIRfilter(3.4, 1/np.sqrt(2), 1500.0, rate, 'notch')
        else:
            raise ValueError("Invalid filter class:", filter_class)

    def integrated_loudness(self, data, verbose=False):
        """ Measure the integrated gated loudness of a signal.
        
        Uses the weighting filters and block size defined by the meter
        the integrated loudness is measured based upon the gating algorithm
        defined in the ITU-R BS.1770-4 specification. 

        Params
        -------
        data : ndarray
            Input multichannel audio data.
        verbose : bool
            Print debug information to the terminal 

        Returns
        -------
        LUFS : float
            Integrated gated loudness of the input measured in dB LUFS.
        """
        input_data = data.copy()
        util.valid_audio(input_data, self.rate, self.block_size)

        if input_data.ndim == 1:
            input_data = np.reshape(input_data, (input_data.shape[0], 1))

        numChannels = input_data.shape[1]        
        numSamples  = input_data.shape[0]

        # Apply frequency weighting filter - account for the acoustic respose of the head and auditory system
        for filter_class, filter_stage in self.filters.items():
            for ch in range(numChannels):
                input_data[:,ch] = filter_stage.apply_filter(input_data[:,ch])
            if verbose:
                filter_stage.plot_magnitude()

        G = [1.0, 1.0, 1.0, 1.41, 1.41] # channel gains
        T_g = self.block_size # 400 ms gating block standard
        Gamma_a = -70.0 # -70 LKFS = absolute loudness threshold
        overlap = 0.75 # overlap of 75% of the block duration
        step = 1.0 - overlap # step size by percentage

        z = np.zeros(shape=(numChannels,numSamples)) # instantiate array - trasponse of input
        T = numSamples / self.rate # length of the input in seconds
        numBlocks = int(np.round(((T - T_g) / (T_g * step)))+1) # total number of gated blocks (see end of eq. 3)
        j_range = np.arange(0, numBlocks) # indexed list of total blocks

        for i in range(numChannels): # iterate over input channels
            for j in j_range: # iterate over total frames
                l = int(T_g * (j * step    ) * self.rate) # lower bound of integration (in samples)
                u = int(T_g * (j * step + 1) * self.rate) # upper bound of integration (in samples)
                # caluate mean square of the filtered for each block (see eq. 1)
                z[i,j] = (1.0 / (T_g * self.rate)) * np.sum(np.square(input_data[l:u,i]))
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            # loudness for each jth block (see eq. 4)
            l = [-0.691 + 10.0 * np.log10(np.sum([G[i] * z[i,j] for i in range(numChannels)])) for j in j_range]
        
        # find gating block indices above absolute threshold
        J_g = [j for j,l_j in enumerate(l) if l_j >= Gamma_a]

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            # calculate the average of z[i,j] as show in eq. 5
            z_avg_gated = [np.mean([z[i,j] for j in J_g]) for i in range(numChannels)]
        # calculate the relative threshold value (see eq. 6)
        Gamma_r = -0.691 + 10.0 * np.log10(np.sum([G[i] * z_avg_gated[i] for i in range(numChannels)])) - 10.0

        # find gating block indices above relative and absolute thresholds  (end of eq. 7)
        J_g = [j for j,l_j in enumerate(l) if (l_j > Gamma_r and l_j > Gamma_a)]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            # calculate the average of z[i,j] as show in eq. 7 with blocks above both thresholds
            z_avg_gated = np.nan_to_num([np.mean([z[i,j] for j in J_g]) for i in range(numChannels)])
        
        # calculate final loudness gated loudness (see eq. 7)
        with np.errstate(divide='ignore'):
            LUFS = -0.691 + 10.0 * np.log10(np.sum([G[i] * z_avg_gated[i] for i in range(numChannels)]))

        return LUFS

class IIRfilter():
    """ IIR Filter object to pre-filtering
    
    This class allows for the generation of various IIR filters
	in order to apply different frequency weighting to audio data
	before measuring the loudness. 

    Parameters
    ----------
    G : float
        Gain of the filter in dB.
    Q : float
        Q of the filter.
    fc : float
        Center frequency of the shelf in Hz.
    rate : float
        Sampling rate in Hz.
    filter_type: str
        Shape of the filter.
    """

    def __init__(self, G, Q, fc, rate, filter_type):
        self.G  = G
        self.Q  = Q
        self.fc = fc
        self.rate = rate
        self.filter_type = filter_type
        self.b, self.a = self.generate_filter_coefficients()

    def __str__(self):
        info = ("""
        {type}
        ----------------------
        Gain         = {G} dB
        Q factor     = {Q} 
        Center freq. = {fc} Hz
        Sample rate  = {rate} Hz
        ----------------------
        b0 = {_b0}
        b1 = {_b1}
        b2 = {_b2}
        a0 = {_a0}
        a1 = {_a1}
        a2 = {_a2}
        ----------------------
        """).format(type=self.valid_types[self.filter_type], 
        G=self.G, Q=self.Q, fc=self.fc, rate=self.rate, 
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
        A  = 10**(self.G/40.0)
        w0 = 2.0 * np.pi * (self.fc / self.rate)
        alpha = np.sin(w0) / (2.0 * self.Q)

        if self.filter_type == 'high_shelf':
            b0 =      A * ( (A+1) + (A-1) * np.cos(w0) + 2 * np.sqrt(A) * alpha )
            b1 = -2 * A * ( (A-1) + (A+1) * np.cos(w0)                          )
            b2 =      A * ( (A+1) + (A-1) * np.cos(w0) - 2 * np.sqrt(A) * alpha )
            a0 =            (A+1) - (A-1) * np.cos(w0) + 2 * np.sqrt(A) * alpha
            a1 =      2 * ( (A-1) - (A+1) * np.cos(w0)                          )
            a2 =            (A+1) - (A-1) * np.cos(w0) - 2 * np.sqrt(A) * alpha
        elif self.filter_type == "peaking":
            b0 =   1 + alpha * A
            b1 =  -2 * np.cos(w0)
            b2 =   1 - alpha * A
            a0 =   1 + alpha / A
            a1 =  -2 * np.cos(w0)
            a2 =   1 - alpha / A
        elif self.filter_type == 'high_pass':
            b0 =  (1 + np.cos(w0))/2
            b1 = -(1 + np.cos(w0))
            b2 =  (1 + np.cos(w0))/2
            a0 =   1 + alpha
            a1 =  -2 * np.cos(w0)
            a2 =   1 - alpha
        else:
            raise ValueError("Invalid filter typer", self.filter_type)

        return np.array([b0, b1, b2])/a0, np.array([a0, a1, a2])/a0

    def plot_magnitude(self):
        """ Plot the magnitude response of the filter.

        This method is provided for debuging and validation of the 
        generated filter coefficients. These plots should match those
        as outlined in the ITU-R 1770-4 standard. 

        """
        fig = plt.figure(figsize=(9,9))
        w, h = scipy.signal.freqz(self.b, self.a, worN=8000)
        plt.semilogx((self.rate * 0.5 / np.pi) * w, 20 * np.log10(abs(h)))
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

    def apply_filter(self, data):
        """ Apply the IIR filter to an input signal.

        Params
        -------
        data : ndarrary
            Input audio data.

        Returns
        -------
        filtered_signal : ndarray
            Filtered input audio.
        """
        return scipy.signal.lfilter(self.b, self.a, data)
      