# pyloudness 
Implementation of ITU-R BS.1770-4 loudness algorithm in python. 

Based on the standard which can be found [here](https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.1770-4-201510-I!!PDF-E.pdf).

## Installation
```
# get pyloudness source
git clone https://github.com/csteinmetz1/pyloudness

# run setup
python setup.py install
```
## Usage
It's easy to measure the loudness of a wav file. 
Here we use scipy to read a wav file as an ndarray.
```python
import pyloudness.loudness as pl
import scipy.io.wavfile

# read file 
filename = "test.wav"
rate, data = scipy.io.wavfile.read(filename)

# measure and then print the loudness
loudness = pl.measure_gated_loudness(data, rate)
print(loudness)
```

## Dependancies
Written for Python 2
- **SciPy** ([https://www.scipy.org/](https://www.scipy.org/))
- **NumPy** ([http://www.numpy.org/](http://www.numpy.org/))
- **Matplotlib** ([https://matplotlib.org/](https://matplotlib.org/))

## TODO
- Add Python 3 support
- Add example usage scripts
- Add some methods for optimization
- Fix occassional "invalid value encounterd in log10" warning
- Add methods for audio signal normalization