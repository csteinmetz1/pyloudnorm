import warnings
import numpy as np
import scipy.io.wavfile

def peak(data, target):
    """ Peak normalize a signal.
    
    Normalize an input signal to a user specifed peak amplitude.   

    Params
    -------
    data : ndarray
        Input multichannel audio data.
    target : float
        Desired peak amplitude in dB.

    Returns
    -------
    output : ndarray
        Peak normalized output data.
    """
    # find the amplitude of the largest peak
    current_peak = np.max(np.abs(data))

    # calculate the gain needed to scale to the desired peak level
    gain = np.power(10.0, target/20.0) / current_peak
    output = gain * data
    
    # check for potentially clipped samples
    if np.max(np.abs(output)) >= 1.0:
        warnings.warn("Possible clipped samples in output.")

    return output

def loudness(data, input_loudness, target_loudness):
    """ Loudness normalize a signal.
    
    Normalize an input signal to a user loudness in dB LKFS.   

    Params
    -------
    data : ndarray
        Input multichannel audio data.
    input_loudness : float
        Loudness of the input in dB LUFS. 
    target_loudness : float
        Target loudness of the output in dB LUFS.
        
    Returns
    -------
    output : ndarray
        Loudness normalized output data.
    """    
    # calculate the gain needed to scale to the desired loudness level
    delta_loudness = target_loudness - input_loudness
    gain = np.power(10.0, delta_loudness/20.0)

    output = gain * data

    # check for potentially clipped samples
    if np.max(np.abs(output)) >= 1.0:
        warnings.warn("Possible clipped samples in output.")

    return output