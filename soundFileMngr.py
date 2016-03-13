# -*- coding: utf-8 -*-
import numpy as np
import os, os.path
import cPickle
import librosa

def milliseconds2samples(numMilli, samplerate):
    return int(numMilli * float(samplerate) / 1000)

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
    
def getSegmentsByTime(musicArray, samplerate, segmentLengthMilli):
    windowSize = milliseconds2samples(segmentLengthMilli, samplerate)
    return getSegments(musicArray, windowSize)
    

def loadAndPickleFiles():
    librosa_loader = librosa.load

    directory_names = ['Screams','Bangs and other manmade sounds','Singing','Birds']
    screams,singing,birds,bangs = [],[],[],[]
    my_sounds = {"Screams":screams,"Singing":singing,"Birds":birds,"Bangs and other manmade sounds":bangs}
    
    for folder in directory_names:
        for sound_file in os.listdir("small_set/"+folder):
            print("folder: ",folder," sound_file: ",sound_file)
            sound,sr = librosa_loader(folder+'/'+sound_file,sr=44100)
            my_sounds[folder].append((sound,sr))

    with open('small_set_sounds.pkl','wb') as outfile:
        cPickle.dump(my_sounds,outfile)
    return my_sounds

def getToySounds():
    try:
        with open('small_set_sounds.pkl','rb') as infile:
            my_sounds = cPickle.load(infile)
    except:
        my_sounds = loadAndPickleFiles()
    
    return my_sounds