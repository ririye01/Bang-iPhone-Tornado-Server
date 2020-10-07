#!/usr/bin/python
'''Read from PyMongo, make simple model and export for CoreML'''

# make this work nice when support for python 3 releases
# from __future__ import print_function # python 3 is good to go!!!

# database imports
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# model imports
import turicreate as tc 
import numpy as np

# export 
#import coremltools


dsid = 1
client  = MongoClient(serverSelectionTimeoutMS=50)
db = client.turidatabase

def get_features_and_labels_as_SFrame(dsid):
    # create feature vectors from database
    features=[]
    labels=[]
    for a in db.labeledinstances.find({"dsid":dsid}): 
        features.append([float(val) for val in a['feature']])
        labels.append(a['label'])

    features = np.array(features)

    # convert to dictionary for tc
    data = {'target':labels}
    data['sequence'] = np.array(features)
    # for i in range(0,len(features[0])):
    #     key = '%d'%(i)
    #     data[key] = features[:,i]

    # send back the SFrame of the data
    return tc.SFrame(data=data)
  

data = get_features_and_labels_as_SFrame(dsid)

print("Found",len(data),"labels and feature vectors")
print("Unique classes found:",data['target'].unique())


print("Training Model")

model = tc.classifier.create(data,target='target')# training

print("Exporting to CoreML")
model.export_coreml('../TuriModel.mlmodel')


# close the mongo connection

client.close() 