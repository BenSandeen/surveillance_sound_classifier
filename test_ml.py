# -*- coding: utf-8 -*-
import machineLearningHelper as mlh

def test_getLearningArrays():
    instances, classifications = mlh.getLearningArrays(useToySounds=True)
    assert len(instances) == len(classifications)

def test_featurify():
    instances, classifications = mlh.getLearningArrays(useToySounds=True)

    instancesFeatures = []
    for instance in instances:
        features, featuresNames = mlh.featurify(instance)
        assert features.dtype == 'float32'
        assert all(not isinstance(feature, list) for feature in features)
        instancesFeatures.append(features)
        lenFeatures = len(features)
        assert lenFeatures == len(featuresNames)
    
def test_getFeatures():
    instances, classifications = mlh.getLearningArrays(useToySounds=True)    
    instancesFeatures, featuresLabels = mlh.getInstancesFeatures(instances)

    assert instancesFeatures.dtype == 'float32'
    
    assert len(instancesFeatures) == len(instances)
    
    lenFeatures = len(instancesFeatures[0])
    for instanceFeatures in instancesFeatures:
        assert lenFeatures == len(instanceFeatures)    
    
