# -*- coding: utf-8 -*-
import os, os.path
import cPickle
import librosa

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

def getSounds():
    #TODO: Implement
    pass
