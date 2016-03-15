# -*- coding: utf-8 -*-
from machineLearningHelper import getLearningArrays
from librosa.output import write_wav
import numpy as np

samplerate = 44100

instances, classifications = getLearningArrays(useToySounds=True)

screams = []
notScreams = []

numInstances = len(instances)

for i in xrange(numInstances):
    if classifications[i]:
        screams.extend(instances[i])
    else:
        notScreams.extend(instances[i])

screams = np.array(screams)
notScreams = np.array(notScreams)

write_wav('./test_sounds/concatenated_screams.wav', screams, 44100, norm=False)
write_wav('./test_sounds/concatenated_not_screams.wav', notScreams, 44100, norm=False)