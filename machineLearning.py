# -*- coding: utf-8 -*-
from sklearn.tree import export_graphviz as eGraph, DecisionTreeClassifier as dTreeClassifier
from sklearn.cross_validation import cross_val_score
import machineLearningHelper as mlh
import numpy as np
import cPickle as p
from joblib import Parallel, delayed

max_depths = [5, 7, 10, 15]
min_weight_fractions_leaf = [0.01, 0.05, 0.1, 0.15]

def modelBuilder(useToySounds=False):
    instances, classifications = mlh.getLearningArrays(useToySounds=useToySounds)
    
    instancesFeatures, featureNames = mlh.getInstancesFeatures(instances)
    classifications = np.array(classifications)
    
    cv = 7
    
    if useToySounds:
        cv = 3

    for max_depth in max_depths:
        for min_weight in min_weight_fractions_leaf:
            yield max_depth, min_weight, classifications, instancesFeatures, featureNames, cv, useToySounds
    
def saveAndAnalyzeTree(treeTuple):
    max_depthIn = treeTuple[0]
    min_weightIn = treeTuple[1]
    classifications = treeTuple[2]
    instancesFeatures = treeTuple[3]
    featureNames = treeTuple[4]
    cvIn = treeTuple[5]
    useToySounds = treeTuple[6]
    
    dTree = dTreeClassifier(max_depth=max_depthIn, 
                            min_weight_fraction_leaf=min_weightIn)
    
    scores = cross_val_score(dTree, instancesFeatures, y=classifications, cv=cvIn)
    dTree = dTree.fit(instancesFeatures, classifications)
    
    dataType = ''
    if useToySounds:
        dataType = 'toy'
    
    saveString = 'models/dTree_' + str(max_depthIn) + '_' + str(min_weightIn) + '_' + dataType
    
    with open(saveString+'.pkl', 'wb') as outModel:
        p.dump(dTree, outModel, protocol=-1)
    
    
    eGraph(dTree, out_file=saveString+'.dot', feature_names=featureNames)
    
    print 'model ' + saveString + ' got average: ', np.average(scores), ' and stdv: ', np.std(scores)
    
    return scores
    
    

def parallelToyForest():
    return Parallel(n_jobs=-1)(delayed(saveAndAnalyzeTree)(treeTuple) for treeTuple in modelBuilder(useToySounds=True))

def parallelBigBoyToyForest():
    return Parallel(n_jobs=-1)(delayed(saveAndAnalyzeTree)(treeTuple) for treeTuple in modelBuilder())

scoresParallel = parallelBigBoyToyForest()
print
print
print
print
print
print scoresParallel