import os
import pyloudnorm as pyln
import soundfile as sf
import numpy as np

def test_integrated_loudness():

	data, rate = sf.read("tests/data/sine_1000.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)

	assert np.isclose(loudness, -3.0523438444331137)

def test_peak_normalize():

	data = np.array(0.5)
	norm = pyln.normalize.peak(data, 0.0)

	assert  np.isclose(norm, 1.0)

def test_loudness_normalize():

	data, rate = sf.read("tests/data/sine_1000.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	norm = pyln.normalize.loudness(data, loudness, -6.0)
	loudness = meter.integrated_loudness(norm)

	assert np.isclose(loudness, -6.0)

def test_rel_gate_test():
	
	data, rate = sf.read("tests/data/1770-2_Comp_RelGateTest.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -10.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_abs_gate_test():
	
	data, rate = sf.read("tests/data/1770-2_Comp_AbsGateTest.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -69.5
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_24LKFS_25Hz_2ch():
	
	data, rate = sf.read("tests/data/1770-2_Comp_24LKFS_25Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)

	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_24LKFS_100Hz_2ch():
	
	data, rate = sf.read("tests/data/1770-2_Comp_24LKFS_100Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_24LKFS_500Hz_2ch():
	
	data, rate = sf.read("tests/data/1770-2_Comp_24LKFS_500Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	

	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_24LKFS_1000Hz_2ch():
	
	data, rate = sf.read("tests/data/1770-2_Comp_24LKFS_1000Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_24LKFS_2000Hz_2ch():
	
	data, rate = sf.read("tests/data/1770-2_Comp_24LKFS_2000Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)

	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_24LKFS_10000Hz_2ch():
	
	data, rate = sf.read("tests/data/1770-2_Comp_24LKFS_10000Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_23LKFS_25Hz_2ch(): 
	
	data, rate = sf.read("tests/data/1770-2_Comp_23LKFS_25Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_23LKFS_100Hz_2ch(): 
	
	data, rate = sf.read("tests/data/1770-2_Comp_23LKFS_100Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_23LKFS_500Hz_2ch(): 
	
	data, rate = sf.read("tests/data/1770-2_Comp_23LKFS_500Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_23LKFS_1000Hz_2ch(): 
	
	data, rate = sf.read("tests/data/1770-2_Comp_23LKFS_1000Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_23LKFS_2000Hz_2ch(): 
	
	data, rate = sf.read("tests/data/1770-2_Comp_23LKFS_2000Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_23LKFS_10000Hz_2ch(): 
	
	data, rate = sf.read("tests/data/1770-2_Comp_23LKFS_10000Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_18LKFS_frequency_sweep(): 
	
	data, rate = sf.read("tests/data/1770-2_Comp_18LKFS_FrequencySweep.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -18.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_conf_stereo_vinL_R_23LKFS(): 
	
	data, rate = sf.read("tests/data/1770-2_Conf_Stereo_VinL+R-23LKFS.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_conf_monovoice_music_24LKFS(): 
	
	data, rate = sf.read("tests/data/1770-2_Conf_Mono_Voice+Music-24LKFS.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def conf_monovoice_music_24LKFS(): 
	
	data, rate = sf.read("tests/data/1770-2_Conf_Mono_Voice+Music-24LKFS.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1

def test_conf_monovoice_music_23LKFS(): 
	
	data, rate = sf.read("tests/data/1770-2_Conf_Mono_Voice+Music-23LKFS.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1