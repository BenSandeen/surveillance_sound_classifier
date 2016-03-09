# -*- coding: utf-8 -*-
import numpy as np

def getSegments(musicArray, windowSize):
    if windowSize % 2:
        raise ArithmeticError('windowSize cannot be odd')

    musicLength = len(musicArray)
    hopSize = windowSize/2
    
    # figure out how many hops
    length_to_cover_with_hops = musicLength - windowSize;
    
    if length_to_cover_with_hops < 0:
        raise ArithmeticError("window_size cannot be longer than the signal to be windowed")
        
    num_hops = 1 + length_to_cover_with_hops/hopSize;    
    segments = [0]*num_hops
    # fill the array with values 
    for hop in range(num_hops):
        start = hop*hopSize
        end = start + windowSize
        if end > musicLength:
            end = musicLength
        segments[hop] = musicArray[start:end]
    return np.array(segments)