# -*- coding: utf-8 -*-
import machineLearningHelper as mlh

def test_getLearningArrays():
    instances, classifications = mlh.getLearningArrays(useToySounds=True)
    assert len(instances) == len(classifications)

def test_featurify():
    instances, classifications = mlh.getLearningArrays(useToySounds=True)

    instancesFeatures = []
    for instance in instances:
        features = mlh.featurify(instance)
        assert features.dtype == 'float32'
        assert all(not isinstance(feature, list) for feature in features)
        instancesFeatures.append(features)
    
def test_getFeatures():
    instances, classifications = mlh.getLearningArrays(useToySounds=True)    
    instancesFeatures = mlh.getInstancesFeatures(instances)

    assert instancesFeatures.dtype == 'float32'    
    
    lenFeatures = len(instancesFeatures[0])
    
    assert len(instancesFeatures) == len(instances)
    for instanceFeatures in instancesFeatures:
        assert lenFeatures == len(instanceFeatures)    
    
