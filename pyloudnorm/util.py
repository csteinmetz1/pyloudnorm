def validate_input_data(data, fs):
    """ Validate input audio data.
    
    Conform input data to floating point audio data bewteen -1 and 1.
    Call this method before calcuating loudness or performing
    normalization if input data is a non-floating point type. (This is
    the case when using scipy to read .wav files)   

    Params
    -------
    data : ndarray
        Input multichannel audio data.
    fs : int
        Sampling rate of the input audio in Hz. 

    Returns
    -------
    output_data : ndarray
        Floating point audio data.
    """
    # for mono input standardize shape
    if len(data.shape) == 1: 
        data = data.reshape((data.shape[0],1))

    valid_dtypes = ['int8', 'int16', 'int32', 'int64',
                    'float16', 'float32', 'float64']

    if data.dtype not in valid_dtypes:
        raise RuntimeError("Invalid input ndarray dtype. Valid input dtypes are", valid_dtypes)

    if   data.dtype == 'int64': 
        data = data.astype('float64') / 9223372036854775807.0
    elif data.dtype == 'int32': 
        data = data.astype('float32') / 2147483647.0
    elif data.dtype == 'int16': 
        data = data.astype('float32') / 32767.0
    elif data.dtype == 'int8':
        data = data.astype('float32') / 127.0
    elif data.dtype == 'float16':
        data = data.astype('float32')

    return data