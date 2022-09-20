from django.shortcuts import render, redirect
from django.conf import settings


import os
import random
import imagehash # pip install imagehash
import numpy as np # pip install numpy
from PIL import Image #pip install pillow
from annoy import AnnoyIndex #pip install annoy


# Create your views here.
def build_weights_home_initial(request):

    images_dir = os.path.join(settings.STATIC_DIR, "train_images")
    
    images_list = [img for img in os.listdir(images_dir)]


    vector_length = 0
    id_to_vec = {}

    for count,f in enumerate(images_list):
        img = Image.open(''.join([images_dir,'/',f]))
        img_hash = imagehash.whash(img)
        hash_array = img_hash.hash.astype('int').flatten();
        vector_length = hash_array.shape[0]
        id_to_vec[count] = hash_array
        # instead of count fetch the db to name of yakuzai by compating the filename and add it to the dictionary


    f = vector_length
    dist_function = "hamming"

    t = AnnoyIndex(f, dist_function)
    for key,value in id_to_vec.items():
        t.add_item(key,value)

    num_trees = 200

    t.build(num_trees)
    t.save('test_result_yakuzai.ann')



    print('train over')
    print('image list is ', images_list)
    
    return redirect('train:train_home')



def build_weights_home(request):

    images_dir = os.path.join(settings.STATIC_DIR, "cropped_images")
    initial_tree_path = os.path.join(settings.STATIC_DIR, "test_result_yakuzai.ann")
    
    images_list = [img for img in os.listdir(images_dir)]


    vector_length = 0
    id_to_vec = {}

    for count,f in enumerate(images_list):
        img = Image.open(''.join([images_dir,'/',f]))
        img_hash = imagehash.whash(img)
        hash_array = img_hash.hash.astype('int').flatten();
        vector_length = hash_array.shape[0]
        id_to_vec[count] = hash_array


    f = vector_length
    dist_function = "hamming"

    t = AnnoyIndex(f, dist_function)
    t.load( initial_tree_path )
    
    for key,value in id_to_vec.items():
        t.add_item(key,value)

    num_trees = 200

    t.build(num_trees)

    t.save('test_result_yakuzai.ann')



    print('train over')
    print('image list is ', images_list)
    
    return redirect('train:train_home')



    print('enters build_weights_home with parameters ', request.POST)
    return redirect('https://www.google.com')
    