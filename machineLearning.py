# -*- coding: utf-8 -*-
from sklearn.tree import export_graphviz as eGraph, DecisionTreeClassifier as dTreeClassifier
import machineLearningHelper as mlh
import numpy as np

instances, classifications = mlh.getLearningArrays(useToySounds=True)



instancesFeatures = mlh.getInstancesFeatures(instances)
classifications = np.array(classifications)

print "Instance features type ", instancesFeatures.dtype
print "classifications type ", classifications.dtype

dTree = dTreeClassifier()
dTree = dTree.fit(instancesFeatures, classifications)
eGraph(dTree, out_file='dTree.dot')