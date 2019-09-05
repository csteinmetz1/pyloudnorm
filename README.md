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

### Advanced operation
A number of alternate weighting filters are available, as well as the ability to adjust the analysis block size. 
Examples are shown below.
```python
import soundfile as sf
import pyloudnorm as pyln
from pyloudnorm import IIRfilter

data, rate = sf.read("test.wav") # load audio

# block size
meter1 = pyln.Meter(rate)                               # 400ms block size
meter2 = pyln.Meter(rate, block_size=0.200)             # 200ms block size

# filter classes
meter3 = pyln.Meter(rate)                               # BS.1770 meter
meter4 = pyln.Meter(rate, filter_class="DeMan")         # fully compliant filters  
meter5 = pyln.Meter(rate, filter_class="Fenton/Lee 1")  # low complexity improvement by Fenton and Lee
meter6 = pyln.Meter(rate, filter_class="Fenton/Lee 2")  # higher complexity improvement by Fenton and Lee
meter7 = pyln.Meter(rate, filter_class="Dash et al.")   # early modification option

# create your own IIR filters
my_high_pass  = IIRfilter(0.0, 0.5, 20.0, rate, 'high_pass')
my_high_shelf = IIRfilter(2.0, 0.7, 1525.0, rate, 'high_shelf')

# create a meter initialized without filters
meter8 = pyln.Meter(rate, filter_class="custom")

# load your filters into the meter
meter8._filters = {'my_high_pass' : my_high_pass, 'my_high_shelf' : my_high_shelf}

```

## Dependancies
- **SciPy** ([https://www.scipy.org/](https://www.scipy.org/))
- **NumPy** ([http://www.numpy.org/](http://www.numpy.org/))

## References

> Ian Dash, Luis Miranda, and Densil Cabrera, "[Multichannel Loudness Listening Test](http://www.aes.org/e-lib/browse.cfm?elib=14581),"
> 124th International Convention of the Audio Engineering Society, May 2008

> Pedro D. Pestana and Álvaro Barbosa, "[Accuracy of ITU-R BS.1770 Algorithm in Evaluating Multitrack Material](http://www.aes.org/e-lib/online/browse.cfm?elib=16608),"
> 133rd International Convention of the Audio Engineering Society, October 2012

> Pedro D. Pestana, Josh D. Reiss, and Álvaro Barbosa, "[Loudness Measurement of Multitrack Audio Content Using Modifications of ITU-R BS.1770](http://www.aes.org/e-lib/browse.cfm?elib=16714),"
> 134th International Convention of the Audio Engineering Society, May 2013

> Steven Fenton and Hyunkook Lee, "[Alternative Weighting Filters for Multi-Track Program Loudness Measurement](http://www.aes.org/e-lib/browse.cfm?elib=19215),"
> 143rd International Convention of the Audio Engineering Society, October 2017

> Brecht De Man, "[Evaluation of Implementations of the EBU R128 Loudness Measurement](http://www.aes.org/e-lib/browse.cfm?elib=19790)," 
> 145th International Convention of the Audio Engineering Society, October 2018. 

