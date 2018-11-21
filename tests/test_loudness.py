import os
import pyloudnorm as pyln
import soundfile as sf
import numpy as np

def test_integrated_loudness():

	data, rate = sf.read("tests/data/sine_1000.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)

	assert loudness == -3.0523438444331137
test_integrated_loudness()

def test_peak_normalize():

	data = np.array(0.5)
	norm = pyln.normalize.peak(data, 0.0)

	assert norm == 1.0
test_peak_normalize()

def test_loudness_normalize():

	data, rate = sf.read("tests/data/sine_1000.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	norm = pyln.normalize.loudness(data, loudness, -6.0)
	loudness = meter.integrated_loudness(norm)

	assert loudness == -6.0
test_loudness_normalize()

def RelGateTest():
	
	data, rate = sf.read("tests/data/1770-2_Comp_RelGateTest.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -10.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
RelGateTest()

def AbsGateTest():
	
	data, rate = sf.read("tests/data/1770-2_Comp_AbsGateTest.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -69.5
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
AbsGateTest()

def _24LKFS_25Hz_2ch():
	
	data, rate = sf.read("tests/data/1770-2_Comp_24LKFS_25Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)

	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
_24LKFS_25Hz_2ch()

def _24LKFS_100Hz_2ch():
	
	data, rate = sf.read("tests/data/1770-2_Comp_24LKFS_100Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
_24LKFS_100Hz_2ch()

def _24LKFS_500Hz_2ch():
	
	data, rate = sf.read("tests/data/1770-2_Comp_24LKFS_500Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	

	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
_24LKFS_500Hz_2ch()

def _24LKFS_1000Hz_2ch():
	
	data, rate = sf.read("tests/data/1770-2_Comp_24LKFS_1000Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
_24LKFS_1000Hz_2ch()

def _24LKFS_2000Hz_2ch():
	
	data, rate = sf.read("tests/data/1770-2_Comp_24LKFS_2000Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)

	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
_24LKFS_2000Hz_2ch()

def _24LKFS_10000Hz_2ch():
	
	data, rate = sf.read("tests/data/1770-2_Comp_24LKFS_10000Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
_24LKFS_10000Hz_2ch()

def _23LKFS_25Hz_2ch(): 
	
	data, rate = sf.read("tests/data/1770-2_Comp_23LKFS_25Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
_23LKFS_25Hz_2ch()

def _23LKFS_100Hz_2ch(): 
	
	data, rate = sf.read("tests/data/1770-2_Comp_23LKFS_100Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
_23LKFS_100Hz_2ch()

def _23LKFS_500Hz_2ch(): 
	
	data, rate = sf.read("tests/data/1770-2_Comp_23LKFS_500Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
_23LKFS_500Hz_2ch()

def _23LKFS_1000Hz_2ch(): 
	
	data, rate = sf.read("tests/data/1770-2_Comp_23LKFS_1000Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
_23LKFS_1000Hz_2ch()

def _23LKFS_2000Hz_2ch(): 
	
	data, rate = sf.read("tests/data/1770-2_Comp_23LKFS_2000Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
_23LKFS_2000Hz_2ch()

def _23LKFS_10000Hz_2ch(): 
	
	data, rate = sf.read("tests/data/1770-2_Comp_23LKFS_10000Hz_2ch.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
_23LKFS_10000Hz_2ch()

def _18LKFS_FrequencySweep(): 
	
	data, rate = sf.read("tests/data/1770-2_Comp_18LKFS_FrequencySweep.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -18.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
_18LKFS_FrequencySweep()

def _Conf_Stereo_VinL_R_23LKFS(): 
	
	data, rate = sf.read("tests/data/1770-2_Conf_Stereo_VinL+R-23LKFS.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
_Conf_Stereo_VinL_R_23LKFS()

def Conf_MonoVoice_Music_24LKFS(): 
	
	data, rate = sf.read("tests/data/1770-2_Conf_Mono_Voice+Music-24LKFS.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
Conf_MonoVoice_Music_24LKFS()

def Conf_MonoVoice_Music_24LKFS(): 
	
	data, rate = sf.read("tests/data/1770-2_Conf_Mono_Voice+Music-24LKFS.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -24.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
Conf_MonoVoice_Music_24LKFS()

def Conf_MonoVoice_Music_23LKFS(): 
	
	data, rate = sf.read("tests/data/1770-2_Conf_Mono_Voice+Music-23LKFS.wav")
	meter = pyln.Meter(rate)
	loudness = meter.integrated_loudness(data)
	
	targetLoudness = -23.0
	assert targetLoudness - 0.1 <= loudness <= targetLoudness + 0.1, "\n\nExpected %s +/- 0.1, instead got %s, or %s\n" % (targetLoudness,loudness,round(loudness, 1))
Conf_MonoVoice_Music_23LKFS()

print("\nNo Errors Found\n")

