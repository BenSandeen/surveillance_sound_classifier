# -*- coding: utf-8 -*-
import soundFileMngr as sfm
import pytest
import collections
import numpy as np

listsEqual = lambda l0, l1: collections.Counter(l0) == collections.Counter(l1)

def test_getSegments():
    musicArray0 = [1, 1, 2, 2, 3, 3, 4, 4]
    
    musictestSegment0 = [[1, 1], [1, 2], [2, 2], [2, 3], [3, 3], [3, 4], [4, 4]]
    musictestSegment1 = [[1, 1, 2, 2], [2, 2, 3, 3], [3, 3, 4, 4]]
    musictestSegment2 = [[1, 1, 2, 2, 3, 3, 4, 4], [3, 3, 4, 4]]
    
    musicSegment0 = sfm.getSegments(musicArray0, 2)
    musicSegment1 = sfm.getSegments(musicArray0, 4)
    musicSegment2 = sfm.getSegments(musicArray0, 8)
    
    for segment1, segment2 in zip(musictestSegment0, musicSegment0):
        assert listsEqual(segment1, segment2)
        
    for segment1, segment2 in zip(musictestSegment1, musicSegment1):
        assert listsEqual(segment1, segment2)
    
    for segment1, segment2 in zip(musictestSegment2, musicSegment2):
        assert listsEqual(segment1, segment2)
    
    with pytest.raises(ArithmeticError):
        sfm.getSegments(musicArray0, 1) #if window size is odd
        sfm.getSegments(musicArray0, 10) #if too large

def test_milliseconds2samples():
    numMilli = 500
    samplerate = 1000
    numSamples = 500
    assert sfm.milliseconds2samples(numMilli, samplerate) == numSamples

def test_getSegmentsByTime():
    lengthOfSongInSecs = np.random.randint(11, 16)
    samplerate = 44100
    lengthOfSegsInMilli = 500
    expectedSampleLength = samplerate / (1000 / lengthOfSegsInMilli)
    
    song = [0] * lengthOfSongInSecs * samplerate
    
    segmentedSong = sfm.getSegmentsByTime(song, samplerate, lengthOfSegsInMilli)
    
    entered = False
    
    for segment in segmentedSong[:-1]:
        entered = True
        assert len(segment) == expectedSampleLength
    else:
        assert entered
