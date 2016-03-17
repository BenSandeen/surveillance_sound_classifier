# -*- coding: utf-8 -*-
import librosa
import cPickle as pickle
import soundMngr as sm
import machineLearningHelper as mlh
import screamDetectorHelper as sdh
import numpy as np
import matplotlib.pyplot as plt
import sys

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
    
def plotProbabilities(screamProbabilities, soundfile):
    pos_data = screamProbabilities
    neg_data = screamProbabilities - 1
    x = np.arange(len(pos_data)) * barTimeLength
    fig = plt.figure()
    fig.suptitle('Probability of screams for \n' + soundfile, fontsize=14)
    ax = plt.subplot(111)
    ax.set_ylabel('Probability (+Screams, -NotScreams)')
    ax.set_xlabel('Time (ms)')
    ax.set_ylim([-1,1])
    ax.bar(x, neg_data, width=1, color='r')
    ax.bar(x, pos_data, width=1, color='b')

def analyzeSoundFile(soundfile):
    sound, sr = librosa.load(soundfile, sr = samplerate)
    
    screamProbabilities = getScreamProbabilities(sound, samplerate, barTimeLength)
    plotProbabilities(screamProbabilities, soundfile)

def test_sounds():
    analyzeSoundFile('test_sounds/rattle.wav')
    analyzeSoundFile('test_sounds/nature.wav')
    analyzeSoundFile('test_sounds/all_scream.wav')
    analyzeSoundFile('test_sounds/scream_with_silence.wav')

def main(argv):
    if argv: #did give a file
        print 'doing given file'
        analyzeSoundFile(argv[0])
    else:
        print 'doing test sounds'
        test_sounds()

if __name__ == "__main__":
    main(sys.argv[1:])