# pyloudnorm  [![Build Status](https://travis-ci.org/csteinmetz1/pyloudnorm.svg?branch=master)](https://travis-ci.org/csteinmetz1/pyloudnorm)
Flexible audio loudness meter in Python. 

Includes implementation of [ITU-R BS.1770-4](https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.1770-4-201510-I!!PDF-E.pdf). <br/>
Momentary, Short-term, and Integrated measurements given by [EBU R128](https://tech.ebu.ch/docs/tech/tech3341.pdf). <br/>
Allows control over gating block size and frequency weighting filters if desired. 

## Installation
```
# get pyloudness source
git clone https://github.com/csteinmetz1/pyloudnorm.git

# run setup from new directory
python setup.py install
```
## Usage

### Find the loudness of an audio file
It's easy to measure the loudness of a wav file. 
Here we use PySoundFile to read a .wav file as an ndarray.
```python
import soundfile as sf
import pyloudnorm

data, rate = sf.read("test.wav") # load audio
meter = pyloudnorm.loudness.Meter(rate) # create BS.1770 meter
loudness = meter.integrated(data) # measure loudness
```

### Loudness normalize and peak normalize audio files
Methods are included to normalize audio files to desired peak values or desired loudness.
Again we use scipy to read a wav file as an ndarray.
```python
import soundfile as sf
import pyloudnorm

# load audio
data, rate = sf.read("test.wav")

# peak normalize audio to -1 dB
peak_normalized_audio = pyloudnorm.normalize.peak(data, rate, -1.0)

# loudness normalize audio to -12 dB LUFS
loudness_normalized_audio = pyloudnorm.normalize.loudness(data, rate, -12.0)
```

## Dependancies
- **SciPy** ([https://www.scipy.org/](https://www.scipy.org/))
- **NumPy** ([http://www.numpy.org/](http://www.numpy.org/))
- **Matplotlib** ([https://matplotlib.org/](https://matplotlib.org/))
- **PySoundFile** ([https://github.com/bastibe/SoundFile](https://github.com/bastibe/SoundFile))

## Todo
- Add support for momentary, short term loudness, and loundess range (see [this spec](https://tech.ebu.ch/docs/tech/tech3341.pdf))
- Add true peak measurement 
- Develop unit tests - include audio files - check potential changes in loudness measurements
- Add additional filters (see [this paper](http://www.aes.org/e-lib/browse.cfm?elib=19215&rndx=851198))
- Include tests from the EBU R128 spec 
- Setup documentation
