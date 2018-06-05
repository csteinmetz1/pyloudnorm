# pyloudnorm
Implementation of ITU-R BS.1770-4 loudness algorithm in python. 

Based on the standard which can be found [here](https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.1770-4-201510-I!!PDF-E.pdf).

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
Here we use scipy to read a wav file as an ndarray.
```python
import scipy.io.wavfile
import pyloudnorm.loudness
import pyloudnorm.util

# read file 
filename = "test.wav"
rate, data = scipy.io.wavfile.read(filename)

# convert int16 data to float32 data
data = pyloudnorm.util.validate_input_data(data, rate)

# measure and then print the loudness
loudness = pyloudnorm.loudness.measure_gated_loudness(data, rate)
print(loudness)
```

### Loudness normalize and peak normalize audio files
Methods are included to normalize audio files to desired peak values or desired loudness.
Again we use scipy to read a wav file as an ndarray.
```python
import scipy.io.wavfile
import pyloudnorm.loudness
import pyloudnorm.normalize
import pyloudnorm.util

# read file 
filename = "test.wav"
rate, data = scipy.io.wavfile.read(filename)

# convert int16 data to float32 data
data = pyloudnorm.util.validate_input_data(data, rate)

# peak normalize audio to -1 dB
peak_normalized_audio = pyloudnorm.normalize.peak(data, rate, -1.0)

# loudness normalize audio to -12 dB LKFS
loudness_normalized_audio = pyloudnorm.normalize.loudness(data, rate, -12)

# Optionally you can write out the normalized audio with scipy
scipy.io.wavfile.write("peak_normalized_audio.wav", rate, peak_normalized_audio)
scipy.io.wavfile.write("loudness_normalized_audio.wav", rate, loudness_normalized_audio)
```

## Dependancies
- **SciPy** ([https://www.scipy.org/](https://www.scipy.org/))
- **NumPy** ([http://www.numpy.org/](http://www.numpy.org/))
- **Matplotlib** ([https://matplotlib.org/](https://matplotlib.org/))

## Todo
- Think about how to handle inputs with length shorter than 400 ms block size
- Add support for momentary, short term loudness, and loundess range [ref](https://tech.ebu.ch/docs/tech/tech3341.pdf)
- Add true peak measurement 
- Build tests