# -*- coding: utf-8 -*-

"""
TODO: implement further psuedocode

soundfile=[eds,df,adfs,adfs,adfs]
#get segments


rmse_segs = librosa.feature.rmse(soundfile,n_fft)

def getScreamProbabilities(sound, samplerate, barTime):
    model = pickle.load("")
    subSegmentTime = 20    
    
    soundSegments = sfm.getSegmentsByTime(sound, samplerate, barTime)
    
    probabilities = []
    for segment in soundSegments:
        probabilities.append(getProbability(segment))
    
    return probabilities


def getProbability(segment):
    pass

def analyzeSoundFile(soundfile):
    samplerate = 44100
    barTimeLength = 500
    sound = librosa.load(soundfile, sr = samplerate)
    
    screamProbabilities = getScreamProbabilities(sound, samplerate, barTimeLength)
    
    plot(screamProbabilities)
"""