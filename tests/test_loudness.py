import os
import pyloudnorm
import soundfile as sf

def test_integrated():

	data, rate = sf.read("tests/data/sine_1000.wav")
	meter = pyloudnorm.loudness.Meter(rate)
	loudness = meter.integrated_loudness(data)

	assert loudness == -3.0523438444331137