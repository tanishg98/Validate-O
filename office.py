
#importing dependencies
import os,sys
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications
from sklearn.metrics import pairwise_distances
import matplotlib.pyplot as plt
import requests
from PIL import Image
import pandas as pd
import pickle
import urllib.request
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=FutureWarning)
    import h5py


#sys.stdout = os.devnull
os.chdir('/Users/tanishgirotra/validate-o-sever/routes/VALIDATE_O')
os.chdir('/Users/tanishgirotra/validate-o-sever/routes/VALIDATE_O/office')
os.chdir('/Users/tanishgirotra/validate-o-sever/routes/VALIDATE_O/office/data')
os.chdir('/Users/tanishgirotra/validate-o-sever/routes/VALIDATE_O/office/data/image1')  
urllib.request.urlretrieve("https://i.pinimg.com/236x/4f/d8/6a/4fd86aa61239d692354ac95e8804b05f.jpg", "local-filename.jpg")
#os.chdir(prevdir)
os.chdir('/Users/tanishgirotra/validate-o-sever/routes/VALIDATE_O/office/data2/image2')
urllib.request.urlretrieve("https://validate-o-server.herokuapp.com/get_image",'local-filename2.jpg')

#initialising weights

img_width, img_height = 224, 224

top_model_weights_path = 'bottleneck_fc_model.h5'
train_data_dir = '/Users/tanishgirotra/validate-o-sever/routes/VALIDATE_O/office/data'
nb_train_samples = 1
epochs = 3
batch_size = 1

#to rectrive final bottleneck function

def save_bottlebeck_features():
    
    #Function to compute VGG-16 CNN for image feature extraction.
    
    datagen = ImageDataGenerator(rescale=1. / 255)
    
    # build the VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')
    generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)

    bottleneck_features_train = model.predict_generator(generator, nb_train_samples // batch_size)
    bottleneck_features_train = bottleneck_features_train.reshape((1,-1))
    
    np.save(open('abc.npy', 'wb'), bottleneck_features_train)
    

save_bottlebeck_features()

s = np.load('abc.npy')
s.shape


#initialising weights

img_width, img_height = 224, 224

top_model_weights_path = 'bottleneck_fc_model.h5'
train_data_dir = '/Users/tanishgirotra/validate-o-sever/routes/VALIDATE_O/office/data2'
nb_train_samples = 1
epochs = 3
batch_size = 1


#to rectrive final bottleneck function

def save_bottlebeck_features():
    
    #Function to compute VGG-16 CNN for image feature extraction.
    
    datagen = ImageDataGenerator(rescale=1. / 255)
    
    # build the VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')
    generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)

    bottleneck_features_train = model.predict_generator(generator, nb_train_samples // batch_size)
    bottleneck_features_train = bottleneck_features_train.reshape((1,-1))
    
    np.save(open('abc2.npy', 'wb'), bottleneck_features_train)
    

save_bottlebeck_features()


s2 = np.load('abc2.npy')
s2.shape


#distance for similarity
distance = pairwise_distances(s,s2)
final_distance=1/(1+np.exp(distance-3))
#sys.stdout = sys.__stdout__
print(distance,final_distance)
