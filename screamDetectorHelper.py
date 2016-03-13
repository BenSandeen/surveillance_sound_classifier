# -*- coding: utf-8 -*-
import numpy as np

SILENCE_THRESHOLD = 0.12

def isSilence(segmentOfSong):
    rms = np.sqrt(np.mean(np.square(segmentOfSong)))
    return rms < SILENCE_THRESHOLD
