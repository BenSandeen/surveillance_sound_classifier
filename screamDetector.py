# -*- coding: utf-8 -*-
import librosa
import cPickle as pickle
import soundMngr as sm
import machineLearningHelper as mlh
import screamDetectorHelper as sdh
import numpy as np
import matplotlib.pyplot as plt

with open("models/pickle_files/dTree_5_0.15_.pkl", 'rb') as inModel:
    model = pickle.load(inModel)

subSegmentTime = 40    
samplerate = 44100
barTimeLength = 120

def getScreamProbabilities(sound, samplerate, barTime):
    soundSegments = sm.getSegmentsByTime(sound, samplerate, barTime)
    
    probabilities = []
    for segment in soundSegments:
        probabilities.append(getProbability(segment))
    
    return np.array(probabilities)


def getProbability(segment):
    subSegments = sm.getSegmentsByTime(segment, samplerate, subSegmentTime)
    subSegmentsFeatures, featureNames = mlh.getInstancesFeatures(subSegments)
    classifications = model.predict(subSegmentsFeatures)
    for i in xrange(len(classifications)):
        if sdh.isSilence(subSegments):
            classifications[i] = 0
    
    return float(sum(classifications))/len(classifications)
    
def plotProbabilities(screamProbabilities):
    pos_data = screamProbabilities
    neg_data = screamProbabilities - 1
    x = len(pos_data)
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.bar(x, neg_data, width=1, color='r')
    ax.bar(x, pos_data, width=1, color='b')
    plt.show()

def analyzeSoundFile(soundfile):
    sound, sr = librosa.load(soundfile, sr = samplerate)
    
    screamProbabilities = getScreamProbabilities(sound, samplerate, barTimeLength)
    print screamProbabilities
    #TODO: plot(screamProbabilities)

def test_sounds():
    analyzeSoundFile('test_sounds/Scream+21_wav_Output_83.wav')
    analyzeSoundFile('test_sounds/125127__thanvannispen__schreeuw1clean_wav_Output_15.wav')
    analyzeSoundFile('test_sounds/31581__dobroide__20070224-swallows_wav_Output_3.wav')
    analyzeSoundFile('test_sounds/243613__patricklieberkind__big-crash_wav_Output_57.wav')
test_sounds()