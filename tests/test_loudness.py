import os
import pyloudnorm
import soundfile as sf

def test_measure_gated_loudness():

	print(os.getcwd())

	rate, data = sf.read("tests/data/sine_1000.wav")
	meter = pyloudnorm.loudness.Meter(rate)
	loudness = meter.measure_gated_loudness(data)

	assert loudness == -3.0523438444331137