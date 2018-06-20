import os
import pyloudnorm as pyln
import soundfile as sf

def test_integrated_loudness():

	data, rate = sf.read("tests/data/sine_1000.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)

	assert loudness == -3.0523438444331137

def test_peak_normalize():

	data = np.array(0.5)
	norm = pyln.normalize.peak(data, 0.0)

	assert norm == 1.0

def test_loudness_normalize():

	data, rate = sf.read("tests/data/sine_1000.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	norm = pyln.normalize.loudness(data, loudness, -6.0)
	loudness = meter.integrated_loudness(norm)

	assert loudness == -6.0

