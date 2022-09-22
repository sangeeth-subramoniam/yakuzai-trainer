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

    images_dir = os.path.join(settings.STATIC_DIR, "train_images3")
    
    images_list = [img for img in os.listdir(images_dir)]


    vector_length = 0
    id_to_vec = {}

    for count,f in enumerate(images_list):
        print('THE FILENAME IS ' , f)
        filename = str(f[0:len(f)-4])
        print('THE new FILENAME IS ' , filename)
        img = Image.open(''.join([images_dir,'/',f]))
        img_hash = imagehash.whash(img)
        hash_array = img_hash.hash.astype('int').flatten();
        vector_length = hash_array.shape[0]
        id_to_vec[filename] = hash_array
        # instead of count fetch the db to name of yakuzai by compating the filename and add it to the dictionary


    f = vector_length
    dist_function = "hamming"

    t = AnnoyIndex(f, dist_function)
    for key,value in id_to_vec.items():
        print('the keyt and value are ', key , value)
        new_key = key.split('_')[0]
        print('new key value is ', new_key)
        t.add_item(int(new_key),value)

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


def nearest_neighbour(request):

    test_images_dir = os.path.join(settings.STATIC_DIR, "test_image_input")
    initial_tree_path = os.path.join(settings.STATIC_DIR, "test_result_yakuzai.ann")
    
    images_list = [img for img in os.listdir(test_images_dir)]

    print(' test images list is ',images_list)

    query_index = images_list.index('10_loxonin.jpg')
    print('query_index is ', query_index , ' and the type is ', type(query_index))



    num_neighbors = 9

    dist_function = "hammings"

    t = AnnoyIndex(f2, dist_function)
    t.load(initial_tree_path)

    neighbors = t.get_nns_by_item(query_index,num_neighbors,include_distances=True)

    print(neighbors)
    print('printing similar images...')

    for items in neighbors[0]:
        print('the file name is ',images_list[int(items)])



    print('image test last')

    id_to_vec2 = {}

    last_image_path2 = r"C:\\Users\\s-sangeeth-k\\Desktop\\pythonmsaccess\\testimage.jpg"
    img2 = Image.open(last_image_path2)
    img_hash2 = imagehash.whash(img2)
    hash_array2 = img_hash2.hash.astype('int').flatten();
    vector_length2 = hash_array2.shape[0]
    id_to_vec2[0] = hash_array2


    f2 = vector_length2
    dist_function2 = "hamming"

    t2 = AnnoyIndex(f2, dist_function2)


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



    t3 = AnnoyIndex(f2, dist_function)
    t3.load('test_result.ann')

    new_neighbors = t3.get_nns_by_vector(new_neighbors_vector,num_neighbors,include_distances=True)


    print('new neighbours is ',new_neighbors )

    for items2 in new_neighbors[0]:
        print('the file name is ',images_list[int(items2)])


    return redirect('train:train_home')



def finding_similar(request):

    print('entering_finding similar')

    id_to_vec2 = {}

    last_image_path2 = r"C:\\Users\\s-sangeeth-k\\Desktop\\yakuzai_trainer\\yakuzai_trainer\\static\\test_image_input\\10_loxonin.jpg"
    img2 = Image.open(last_image_path2)
    img_hash2 = imagehash.whash(img2)
    
    hash_array2 = img_hash2.hash.astype('int').flatten();
    vector_length2 = hash_array2.shape[0]
    
    id_to_vec2[0] = hash_array2


    f2 = vector_length2
    dist_function = "hamming"
    num_neighbors = 9

    t2 = AnnoyIndex(f2, dist_function)
    


    for key,value in id_to_vec2.items():
        print('the keyS and value of similar search are ', key , value)
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

    print('new neighbour vectors',new_neighbors_vector)


    initial_tree_path = os.path.join(settings.STATIC_DIR, "test_result_yakuzai.ann")
    t3 = AnnoyIndex(f2, dist_function)
    t3.load(initial_tree_path)

    new_neighbors = t3.get_nns_by_vector(new_neighbors_vector,num_neighbors,include_distances=True)


    print('new neighbours is ',new_neighbors )

    print('exiting _finding similar')

    # for items2 in new_neighbors[0]:
    #     print('the file name is ',images_list[int(items2)])
    