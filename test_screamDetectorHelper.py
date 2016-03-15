# -*- coding: utf-8 -*-
"""
import screamDetectorHelper as sdh
import soundFileMngr as sfm
import librosa

def test_isSilence():
    samplerate = 44100
    silence, _ = librosa.load("test_sounds/silence.wav", sr=samplerate)
    segmentedSilence = sfm.getSegmentsByTime(silence, samplerate, 1000)
    for segment in segmentedSilence:
        assert sdh.isSilence(segment)
    
    scream, _ = librosa.load("test_sounds/Scream+21_wav_Output_83.wav", sr=samplerate)
    segmentedScream = sfm.getSegmentsByTime(scream, samplerate, 500)

    for segment in segmentedScream:
        assert not sdh.isSilence(segment)
"""