# -*- coding: utf-8 -*-
import soundMngr as sm
import soundFileMngr as sfm
import librosa
import numpy as np

timeForSubSegment = 40 #in milliseconds
samplerate = 44100
segmentSize = (samplerate * timeForSubSegment / 1000) + 1

def make_extender(n):
    return lambda x: n.extend(x.flatten())
def list_extender(n):
    return lambda x: n.extend(x)

def getLabels(name, mat):
    return [name + " - " + str(i) for i in range(len(mat.flatten()))]

def featurify(soundSegment):
    # should be vector of dimensions 20x1
    sgram = librosa.feature.melspectrogram(y=soundSegment,sr=samplerate,n_fft=segmentSize,
                                           hop_length=segmentSize)
    mfcc = librosa.feature.mfcc(S=librosa.logamplitude(sgram), sr=samplerate)
    
    # hop_length and window_size are the width of the segment
    pre_attack = librosa.feature.rmse(y=soundSegment,n_fft=segmentSize,hop_length=segmentSize)
    pre_attack = pre_attack.flatten() # may need to return the element inside this: eg: [[a]]

    # look at median of:
        # spectral_centroid = librosa.feature.delta(spectral_centroid)
        # spectral_centroid = np.square(spectral_centroid)
    spectral_centroid = librosa.feature.spectral_centroid(y=soundSegment,
                                                          sr=samplerate,
                                                          n_fft=segmentSize,
                                                          hop_length=segmentSize)
    
    chroma = librosa.feature.chroma_stft(y=soundSegment, sr=samplerate,
                                            n_fft=segmentSize,hop_length=segmentSize)
    chroma_std = np.std(chroma,axis=0) # may not need axis=0 arg
    chroma_avg = np.mean(chroma,axis=0)    
    
    attack = librosa.feature.delta(soundSegment)#,order=2)
    
    features = []
    featuresNames = []
    extend_features = make_extender(features)
    extend_names = list_extender(featuresNames)
    
    extend_features(mfcc)
    extend_names(getLabels('mfcc', mfcc))
    extend_features(pre_attack)
    extend_names(getLabels('pre_attack', pre_attack ))
    extend_features(spectral_centroid)
    extend_names(getLabels('spectral_centroid', spectral_centroid))
    extend_features(chroma)
    extend_names(getLabels('chroma',chroma ))
    extend_features(chroma_avg)
    extend_names(getLabels('chroma_avg', chroma_avg))
    extend_features(chroma_std)
    extend_names(getLabels('chroma_std', chroma_std))
    
    return np.array(features, dtype=np.float32), featuresNames

def getInstancesFeatures(instances):
    instancesFeatures = []
    for instance in instances:
        features, featureNames = featurify(instance)
        instancesFeatures.append(features)
    return np.array(instancesFeatures, dtype=np.float32), featureNames

def getSoundsFromTupleList(sound_sr_tuple_list):
    return list(zip(*sound_sr_tuple_list)[0])

def getLearningArrays(useToySounds=False):
    if useToySounds:
        soundsDict = sfm.getToySounds()
    else:
        soundsDict = sfm.getSounds()
    
    sound_sr_tuple_list = soundsDict["Screams"]
    soundScreams = getSoundsFromTupleList(sound_sr_tuple_list)
    inArray = segmentAndFilterSilenceOut(soundScreams)
    numOfScreams = len(inArray)
    outArray = [1] * numOfScreams
    
    print "Done with screams. We have ", numOfScreams, "instances of screams."
    
    inArrayNotScreams = []
    
    limit = numOfScreams/3
    
    for soundKey in soundsDict:
        if soundKey != "Screams":
            print "Doing soundKey = ", soundKey
            sound_sr_tuple_list = soundsDict[soundKey]
            soundsNotScreams = getSoundsFromTupleList(sound_sr_tuple_list)
            inArrayNotScreams.extend(
                segmentAndFilterSilenceOut(soundsNotScreams, 
                                           limit = limit))
    
    inArray.extend(inArrayNotScreams)
    outArray.extend([0] * len(inArrayNotScreams))
    
    print "Done with non screams. We have ", len(inArrayNotScreams), "instances of no screams."
            
    
    return inArray, outArray
    

def segmentAndFilterSilenceOut(arrayOfSounds, limit=None):
    segmentedSounds = []
    for sound in arrayOfSounds:
        segmentedSounds.extend(sm.getSegmentsByTime(sound, samplerate, timeForSubSegment))
    segmentedFilteredSounds = sm.filterSilenceOut(segmentedSounds)
    
    l = len(segmentedFilteredSounds)
    if limit and limit < l:
        print "There are more sounds than the limit"
        segmentedFilteredSounds = segmentedFilteredSounds[:limit]
    elif limit and limit > l:
        print "There are less sounds than the limit!"
        print "limit = ", limit, " ; we have: ", l
    
    return segmentedFilteredSounds