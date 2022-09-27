import shutil
from django.shortcuts import render, redirect
from django.conf import settings


import os
import random
import imagehash # pip install imagehash
import numpy as np # pip install numpy
from PIL import Image #pip install pillow
from annoy import AnnoyIndex #pip install annoy

from static.yakuzai_names import yakuzai_names

from datetime import datetime

import cv2


# Create your views here.
def build_weights_home_initial(request):
    

    # images_dir = r"C:\\Users\\s-sangeeth-k\\Desktop\\YAKUZAI_DB\\test"
    # images_dir = r"C:\\Users\\s-sangeeth-k\\Desktop\\pythonmsaccess\\train_images3"
    images_dir = os.path.join(settings.STATIC_DIR, "train_images3")
    
    
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
    for key,value in id_to_vec.items():
        t.add_item(key,value)

    num_trees = 200

    t.build(num_trees)
    t.save(os.path.join(settings.STATIC_DIR,'ann_file\\test_result_yakuzai.ann'))

    print('train over')

    print('image list is ', images_list)

    print('overrrrrrrrrrrrrrrrrrrrrrrrrswsssssseeseses')

    return redirect('build_weights:similar_images')



def similar_images(request):

    print('enters_similar_images')

    id_to_vec2 = {}

    images_dir = os.path.join(settings.STATIC_DIR, "train_images3")
    
    images_list = [img for img in os.listdir(images_dir)]

    # last_image_path2 = r"C:\\Users\\s-sangeeth-k\\Desktop\\YAKUZAI_DB\\unnamed2-testinput.jpg"
    last_image_path2 = r"C:\Users\s-sangeeth-k\Desktop\yakuzai_trainer\yakuzai_trainer\static\test_image_input\\10_loxonin.jpg"

    #last_image_path2 = r"C:\\Users\\s-sangeeth-k\\Desktop\\YAKUZAI_DB\\loxtestinpdwnload.jpg"

    img2 = Image.open(last_image_path2)

    img_hash2 = imagehash.whash(img2)
    hash_array2 = img_hash2.hash.astype('int').flatten();
    vector_length2 = hash_array2.shape[0]
    id_to_vec2[0] = hash_array2
    dist_function = "hamming"

    f2 = vector_length2
    dist_function2 = "hamming"

    t2 = AnnoyIndex(f2, dist_function)

    t = AnnoyIndex(f2, dist_function)

    try:
        t.load(os.path.join(settings.STATIC_DIR,'ann_file\\test_result_yakuzai.ann'))
        print('succesfully loaded the .ann file from static / annfile / result.ann file')
    except Exception as e:
        print('Failed to load the .ann file from static / annfile / result.ann file')


    for key,value in id_to_vec2.items():
        t2.add_item(key,value)

    num_trees2 = 200
    t2.build(num_trees2)


    print('t2 is ', t2)
    print('vector val of annoy items is ', t2.get_item_vector(0) )

    try:
        print('length of t2 is ', len(t2))
    except Exception as e:
        print('get length of t2 exception occured')

    new_neighbors_vector = t2.get_item_vector(0)


    num_neighbors = 5

    new_neighbors = t.get_nns_by_vector(new_neighbors_vector,num_neighbors,include_distances=True)


    print('new neighbours is ',new_neighbors )

    for items2 in new_neighbors[0]:
        print('the file name is ',images_list[int(items2)])

    return redirect('train:train_home')



def findname(name_text):

    print('entering find')



def similar_images_from_parameter(filepath = None):

    if not filepath:
        return None


    print('enters_similar_images from param with path ', filepath)

    id_to_vec2 = {}

    images_dir = os.path.join(settings.STATIC_DIR, "train_images3")
    
    images_list = [img for img in os.listdir(images_dir)]

    # last_image_path2 = r"C:\\Users\\s-sangeeth-k\\Desktop\\YAKUZAI_DB\\unnamed2-testinput.jpg"
    # last_image_path2 = r"C:\Users\s-sangeeth-k\Desktop\yakuzai_trainer\yakuzai_trainer\static\test_image_input\\10_loxonin.jpg"
    last_image_path2 = filepath

    #last_image_path2 = r"C:\\Users\\s-sangeeth-k\\Desktop\\YAKUZAI_DB\\loxtestinpdwnload.jpg"

    img2 = Image.open(last_image_path2)

    img_hash2 = imagehash.whash(img2)
    hash_array2 = img_hash2.hash.astype('int').flatten();
    vector_length2 = hash_array2.shape[0]
    id_to_vec2[0] = hash_array2
    dist_function = "hamming"

    f2 = vector_length2
    dist_function2 = "hamming"

    t2 = AnnoyIndex(f2, dist_function)

    t = AnnoyIndex(f2, dist_function)

    try:
        t.load(os.path.join(settings.STATIC_DIR,'ann_file\\test_result_yakuzai.ann'))
        print('succesfully loaded the .ann file from static / annfile / result.ann file')
    except Exception as e:
        print('Failed to load the .ann file from static / annfile / result.ann file')


    for key,value in id_to_vec2.items():
        t2.add_item(key,value)

    num_trees2 = 200
    t2.build(num_trees2)


    print('t2 is ', t2)
    print('vector val of annoy items is ', t2.get_item_vector(0) )

    try:
        print('length of t2 is ', len(t2))
    except Exception as e:
        print('get length of t2 exception occured')

    new_neighbors_vector = t2.get_item_vector(0)


    num_neighbors = 5

    new_neighbors = t.get_nns_by_vector(new_neighbors_vector,num_neighbors,include_distances=True)


    print('new neighbours is ',new_neighbors )

    for items2 in new_neighbors[0]:
        print('the file name is ',images_list[int(items2)])

    print('returning newarest neighbour name', new_neighbors)
    return images_list[int(new_neighbors[0][0])]



def add_single_image(request):

    now = datetime.now()

    import os
    print('entering add_single_image')

    print('form post contents in add_single_image are ', request.POST)

    yakuzai_select_option_list = request.POST.getlist('yakuzai_name',None)
    yakuzai_changed_name_list = request.POST.getlist('changed_yakuzai_name',None)

    print('yakuzai_select_option_list is ' , yakuzai_select_option_list)

    print(' -------------------  ')

    print('yakuzai_changed_name_list is ' , yakuzai_changed_name_list)


    for counter,items in enumerate(yakuzai_select_option_list):
        if items != '1':
            selected_option = int(items) - 1 # - 1 for te none option which is not used
            selected_option_value = yakuzai_names[selected_option]

            print('selected option val of select element ',counter,' is ' , selected_option + 1 ,' and its value is ' , selected_option_value)
            
            

            name_of_new_file = yakuzai_changed_name_list[counter]

            print('filename val of select element ',counter,' is ' , name_of_new_file)


            source_image_folder = os.path.join(settings.STATIC_DIR,name_of_new_file)
            destination_image_folder = os.path.join(settings.STATIC_DIR, "train_images3")

            import base64

            with open(source_image_folder, "rb") as image_file:
                print('the image fikle is sorce is ' , image_file)
                encoded_string = base64.b64encode(image_file.read())
                print('the base 64 data of image is ' , encoded_string)
                print('base 64 over' , type(encoded_string))


            print('tseeee etttt ')

            month = str(now.strftime("%B"))
            day = str(now.strftime("%d"))
            seconds = str(now.strftime("%S"))
            microseconds = str(now.strftime("%f"))

            print('the month + day + seconds +  microseconds are ', month , day,  seconds , microseconds)


            destination_file_image_unique_name = str(str(selected_option_value) + "_YAKUZAI" + "_sangeeth_" + month + day + '_' + seconds + '_' + microseconds + '.jpg')

            destination_file = os.path.join(destination_image_folder,destination_file_image_unique_name)
            
            with open(destination_file, "wb") as fh:
                fh.write(base64.decodebytes(encoded_string))

            print('base64 file save succesful')


            print('lets train the .ann file with the newly added cropped image file')


            return redirect('build_weights:build_weights_home_initial')

