import warnings
import numpy as np
import scipy.io.wavfile
import pyloudnorm.loudness

def peak(data, fs, target_peak):
    """ Peak normalize a signal.
    
    Normalize an input signal to a user specifed peak amplitude.   

    Params
    -------
    data : ndarray
        Input multichannel audio data.
    fs : int
        Sampling rate of the input audio in Hz. 
    peak : float
        Desired peak amplitude in dB.

    Returns
    -------
    output_data : ndarray
        Peak normalized output data.
    """
    # find the amplitude of the largest peak
    current_peak = np.max(np.abs(data))

    # calculate the gain needed to scale to the desired peak level
    gain = np.power(10.0, target_peak/20.0) / current_peak
    output = gain * data
    
    # check for potentially clipped samples
    if np.max(np.abs(output)) >= 1.0:
        warnings.warn("Possible clipped samples in output.")
    return output

def loudness(data, fs, target_loudness):
    """ Loudness normalize a signal.
    
    Normalize an input signal to a user loudness in dB LKFS.   

    Params
    -------
    data : ndarray
        Input multichannel audio data.
    fs : int
        Sampling rate of the input audio in Hz. 
    target_loudness :
        Desired loudness in dB LKFS.
        
    Returns
    -------
    output_data : ndarray
        Loudness normalized output data.
    """
    # measure loudness of input
    input_loudness = pyloudnorm.loudness.measure_gated_loudness(data, fs)
    
    # calculate the gain needed to scale to the desired loudness level
    delta_loudness = target_loudness - input_loudness
    gain = np.power(10.0, delta_loudness/20.0)

    output = gain * data

    # check for potentially clipped samples
    if np.max(np.abs(output)) >= 1.0:
        warnings.warn("Possible clipped samples in output.")
    return output