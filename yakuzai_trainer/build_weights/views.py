import shutil
from django.shortcuts import render, redirect
from django.conf import settings


import os
import random
import imagehash # pip install imagehash
import numpy as np # pip install numpy
from PIL import Image #pip install pillow
from annoy import AnnoyIndex #pip install annoy

yakuzai_names = ["None","loxonin 10mg" , "loxonin 100mg" , "loxonin 500mg" , "karonaru 100mg" , "antimidipine 100mg" ,"antimidipine 500mg""loxonin 10mg" , "loxonin 100mg" , "loxonin 500mg" , "karonaru 100mg" , "antimidipine 100mg" ,"loxonin 10mg" , "loxonin 100mg" , "loxonin 500mg" , "karonaru 100mg" , "antimidipine 100mg" ,"loxonin 10mg" , "loxonin 100mg" , "loxonin 500mg" , "karonaru 100mg" , "antimidipine 100mg" ,"loxonin 10mg" , "loxonin 100mg" , "loxonin 500mg" , "karonaru 100mg" , "antimidipine 100mg" ,"loxonin 10mg" , "loxonin 100mg" , "loxonin 500mg" , "karonaru 100mg" , "antimidipine 100mg" ,"loxonin 10mg" , "loxonin 100mg" , "loxonin 500mg" , "karonaru 100mg" , "antimidipine 100mg"  ]


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

            shutil.copy(source_image_folder,destination_image_folder)

            only_name_in_name_of_new_file = str(name_of_new_file.split('/')[1])

            print('onlyfile name is ', only_name_in_name_of_new_file)

            src_rename_file = os.path.join(settings.STATIC_DIR, "train_images3\\{}".format(only_name_in_name_of_new_file))
            
            os.rename( src_rename_file , 'joker.jpg')


            
            print('lets train the .ann file with the newly added cropped image file')






    return redirect('https://www.google.com')
