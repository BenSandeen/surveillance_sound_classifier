# -*- coding: utf-8 -*-
import soundMngr as sm
import soundFileMngr as sfm

timeForSubSegment = 40 #in milliseconds
samplerate = 44100

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