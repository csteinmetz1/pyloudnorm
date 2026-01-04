"""
Tests for Loudness Range (LRA) measurement.

Reference: EBU Tech 3342 - "Loudness Range: A measure to supplement 
loudness normalisation in accordance with EBU R 128"
https://tech.ebu.ch/docs/tech/tech3342.pdf

The LRA algorithm uses:
- 3-second blocks with 10 Hz refresh rate (~97% overlap)
- Absolute threshold: -70 LUFS
- Relative threshold: -20 LU below ungated integrated loudness
- LRA = 95th percentile - 10th percentile of gated short-term loudness values
"""
import numpy as np
import pyloudnorm as pyln
import soundfile as sf


def test_loudness_range_basic():
    """Test LRA calculation on audio with known dynamic variation.
    
    Per EBU Tech 3342, LRA measures the variation in loudness over time.
    A signal with constant amplitude should have low LRA (near 0),
    while a signal with varying amplitude should have higher LRA.
    """
    rate = 48000
    
    # Create a constant-amplitude signal (should have low LRA)
    duration = 10  # seconds - need enough for 3-second blocks
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    constant_signal = 0.5 * np.sin(2 * np.pi * 1000 * t)
    
    meter = pyln.Meter(rate)
    lra_constant = meter.loudness_range(constant_signal)
    
    # Constant signal should have very low LRA (close to 0)
    assert lra_constant < 3.0, f"Constant signal LRA should be low, got {lra_constant}"


def test_loudness_range_varying_dynamics():
    """Test LRA on a signal with intentionally varying dynamics.
    
    Per EBU Tech 3342, signals with large loudness variation should
    have higher LRA values. This test creates a signal that alternates
    between loud and quiet sections.
    """
    rate = 48000
    block_duration = 3  # seconds per segment to match 3s block size
    
    # Create alternating loud/quiet sections (each 3+ seconds for proper blocking)
    quiet_section = 0.05 * np.sin(2 * np.pi * 440 * np.linspace(0, block_duration, int(rate * block_duration)))
    loud_section = 0.5 * np.sin(2 * np.pi * 440 * np.linspace(0, block_duration, int(rate * block_duration)))
    
    # Alternate: quiet, loud, quiet, loud (12 seconds total)
    varying_signal = np.concatenate([quiet_section, loud_section, quiet_section, loud_section])
    
    meter = pyln.Meter(rate)
    lra_varying = meter.loudness_range(varying_signal)
    
    # Signal with 20 dB amplitude variation should have substantial LRA
    # The amplitude ratio of 0.5/0.05 = 10 corresponds to 20 dB
    assert lra_varying > 5.0, f"Varying dynamics signal should have higher LRA, got {lra_varying}"


def test_loudness_range_preserves_meter_state():
    """Test that loudness_range() restores meter settings after calculation.
    
    This is a regression test for a bug where loudness_range() would
    permanently modify block_size (to 3.0s) and overlap (to 0.97),
    affecting subsequent integrated_loudness() calls.
    """
    rate = 48000
    duration = 10
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    signal = 0.5 * np.sin(2 * np.pi * 440 * t)
    
    meter = pyln.Meter(rate)
    
    # Record original settings
    original_block_size = meter.block_size
    original_overlap = meter.overlap
    
    # Call loudness_range
    meter.loudness_range(signal)
    
    # Verify settings are restored
    assert meter.block_size == original_block_size, \
        f"block_size not restored: expected {original_block_size}, got {meter.block_size}"
    assert meter.overlap == original_overlap, \
        f"overlap not restored: expected {original_overlap}, got {meter.overlap}"


def test_loudness_range_then_integrated_loudness():
    """Test that integrated_loudness() works correctly after loudness_range().
    
    This ensures the meter state restoration is complete and subsequent
    measurements use the correct 400ms block size per ITU-R BS.1770-4.
    """
    rate = 48000
    data, rate = sf.read("tests/data/sine_1000.wav")
    
    meter = pyln.Meter(rate)
    
    # Get baseline integrated loudness
    loudness_before = meter.integrated_loudness(data)
    
    # Call loudness_range on some test signal
    test_signal = 0.5 * np.sin(2 * np.pi * 440 * np.linspace(0, 10, int(rate * 10)))
    meter.loudness_range(test_signal)
    
    # Get integrated loudness again - should match baseline
    loudness_after = meter.integrated_loudness(data)
    
    assert np.isclose(loudness_before, loudness_after), \
        f"Integrated loudness changed after loudness_range(): {loudness_before} vs {loudness_after}"


def test_loudness_range_silent_signal():
    """Test LRA on a near-silent signal (below -70 LUFS absolute threshold).
    
    Per EBU Tech 3342, signals below the absolute threshold of -70 LUFS
    are gated out. If all blocks are below this threshold, LRA cannot
    be computed and should return NaN.
    """
    rate = 48000
    duration = 10
    
    # Create near-silent signal (well below -70 LUFS)
    silent_signal = 1e-10 * np.random.randn(int(rate * duration))
    
    meter = pyln.Meter(rate)
    lra = meter.loudness_range(silent_signal)
    
    # Should return NaN for signals too quiet to measure
    assert np.isnan(lra), f"Expected NaN for silent signal, got {lra}"


def test_loudness_range_stereo():
    """Test LRA calculation on stereo audio.
    
    Per EBU Tech 3342, LRA should work with multichannel audio
    following ITU-R BS.1770-4 channel weighting.
    """
    rate = 48000
    duration = 10
    t = np.linspace(0, duration, int(rate * duration), endpoint=False)
    
    # Create stereo signal
    left = 0.5 * np.sin(2 * np.pi * 440 * t)
    right = 0.5 * np.sin(2 * np.pi * 880 * t)
    stereo_signal = np.column_stack([left, right])
    
    meter = pyln.Meter(rate)
    lra = meter.loudness_range(stereo_signal)
    
    # Should return a valid LRA value
    assert not np.isnan(lra), "LRA should be valid for stereo signal"
    assert lra >= 0, f"LRA should be non-negative, got {lra}"


def test_loudness_range_real_audio():
    """Test LRA on real audio file from test data.
    
    Uses existing test audio to verify LRA works on real-world content.
    """
    data, rate = sf.read("tests/data/piano.wav")
    
    meter = pyln.Meter(rate)
    lra = meter.loudness_range(data)
    
    # Real music should have measurable LRA
    assert not np.isnan(lra), "LRA should be valid for real audio"
    assert lra >= 0, f"LRA should be non-negative, got {lra}"
    # Music typically has LRA between 5-15 LU
    assert lra < 30, f"LRA seems unreasonably high: {lra}"


