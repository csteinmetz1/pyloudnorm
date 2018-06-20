import numpy as np

def valid_audio(data, rate, block_size):
    """ Validate input audio data.
    
    Ensure input is numpy array of floating point data bewteen -1 and 1

    Params
    -------
    data : ndarray
        Input audio data
    rate : int
        Sampling rate of the input audio in Hz
    block_size : int
        Analysis block size in seconds 

    Returns
    -------
    valid : bool
        True if valid audio
        
    """
    if not isinstance(data, np.ndarray):
        raise ValueError("Data must be of type numpy.ndarray")
    
    if not np.issubdtype(data.dtype, np.floating):
        raise ValueError("Data must be floating point")

    if data.ndim == 2 and data.shape[1] > 5:
        raise ValueError("Audio must have five channels or less")

    if data.shape[0] < block_size * rate:
        raise ValueError("Audio must be have length greater than the block size")
    
    return True