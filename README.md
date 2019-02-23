# pyloudnorm  [![Build Status](https://travis-ci.org/csteinmetz1/pyloudnorm.svg?branch=master)](https://travis-ci.org/csteinmetz1/pyloudnorm)
Flexible audio loudness meter in Python. 

Implementation of [ITU-R BS.1770-4](https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.1770-4-201510-I!!PDF-E.pdf). <br/>
Allows control over gating block size and frequency weighting filters for additional control. 

## Installation
```
pip install git+https://github.com/csteinmetz1/pyloudnorm
```
## Usage

### Find the loudness of an audio file
It's easy to measure the loudness of a wav file. 
Here we use PySoundFile to read a .wav file as an ndarray.
```python
import soundfile as sf
import pyloudnorm as pyln

data, rate = sf.read("test.wav") # load audio (with shape (samples, channels))
meter = pyln.Meter(rate) # create BS.1770 meter
loudness = meter.integrated_loudness(data) # measure loudness
```

### Loudness normalize and peak normalize audio files
Methods are included to normalize audio files to desired peak values or desired loudness.
```python
import soundfile as sf
import pyloudnorm as pyln

data, rate = sf.read("test.wav") # load audio

# peak normalize audio to -1 dB
peak_normalized_audio = pyln.normalize.peak(data, -1.0)

# measure the loudness first 
meter = pyln.Meter(rate) # create BS.1770 meter
loudness = meter.integrated_loudness(data)

# loudness normalize audio to -12 dB LUFS
loudness_normalized_audio = pyln.normalize.loudness(data, loudness, -12.0)
```

## Dependancies
- **SciPy** ([https://www.scipy.org/](https://www.scipy.org/))
- **NumPy** ([http://www.numpy.org/](http://www.numpy.org/))

