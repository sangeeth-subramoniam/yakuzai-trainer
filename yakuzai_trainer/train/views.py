from msilib.schema import Directory
from multiprocessing import context
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.templatetags.static import static
from django.conf import settings

import os

# Create your views here.
def train_home(request):

    folder='static/image'

    file_path = folder + '/train_medicine.jpg'

    image_exist = os.path.exists(file_path)

    print('image exist is ', image_exist)



    print('check_cropped_files')
    directory = os.path.join(settings.STATIC_DIR, "cropped_images")
    cropped_file_count = 0
    cropped_file_names = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            cropped_file_count += 1
            cropped_file_names.append('cropped_images/yakuzai' + str(cropped_file_count) + str('.jpg'))
    print('There are ', cropped_file_count,' files in cropped folder ... List is ' , cropped_file_names)


    yakuzai_names = ["None","loxonin 10mg" , "loxonin 100mg" , "loxonin 500mg" , "karonaru 100mg" , "antimidipine 100mg" ,"antimidipine 500mg""loxonin 10mg" , "loxonin 100mg" , "loxonin 500mg" , "karonaru 100mg" , "antimidipine 100mg" ,"loxonin 10mg" , "loxonin 100mg" , "loxonin 500mg" , "karonaru 100mg" , "antimidipine 100mg" ,"loxonin 10mg" , "loxonin 100mg" , "loxonin 500mg" , "karonaru 100mg" , "antimidipine 100mg" ,"loxonin 10mg" , "loxonin 100mg" , "loxonin 500mg" , "karonaru 100mg" , "antimidipine 100mg" ,"loxonin 10mg" , "loxonin 100mg" , "loxonin 500mg" , "karonaru 100mg" , "antimidipine 100mg" ,"loxonin 10mg" , "loxonin 100mg" , "loxonin 500mg" , "karonaru 100mg" , "antimidipine 100mg"  ]


    context = {
        'image_exist' : image_exist,
        'cropped_file_names':cropped_file_names,
        'yakuzai_names' : yakuzai_names
    }

    return render(request, 'train/home.html', context)

def image_post(request):
    print('entering image post with paramerters', request.POST)
    print('entering image post with files', request.FILES)
    
    folder='static/image'

    file_path = folder + '/train_medicine.jpg'

    print('does file exist ? ', os.path.exists(file_path) )

    #DELETE FILE IF ALREADY EXIST 
    if os.path.exists(file_path):
        print('file with same name is present ! Removing File ...')
        os.remove(file_path)
        print('file remved successfully !')
    else:
        print('file with same name not present ! ')

    myfile = request.FILES.get('input-image',None)

    fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT  
    
    filename = fs.save('train_medicine.jpg', myfile)
    
    file_url = fs.url(filename)

    print('file url is ', file_url)





    print(' X ---------------------- START YAKUZAI CROP ------------------------ X')



    crop_images = count_yakuzai()

    print('images cropped ! ' , crop_images)

    return redirect('train:train_home')



def remove_image(request):
    print('removing image ')

    folder='static/image'

    file_path = folder + '/train_medicine.jpg'

    #DELETE FILE IF ALREADY EXIST 
    if os.path.exists(file_path):
        print('file with same name is present ! Removing File ...')
        os.remove(file_path)
        print('file remved successfully !')
    else:
        print('file with same name not present ! ')


    print('removing all cropped images')
    
    cropped_image_folder='static/cropped_images'

    for filename in os.listdir(cropped_image_folder):
        print('filename is ', filename)
        print('filename is ', os.path.join(cropped_image_folder,filename))
        os.remove(os.path.join(cropped_image_folder,filename))
        print('removed!')
    
    print('removed all cropped images successfully ! ')


    return redirect('train:train_home')




def count_yakuzai():

    import random

    #COMPUTER VISION OCR

    # print('imagefile tagname is  ' , tagname)

    print('overriding image_path ')

    image_path = 'static/image/train_medicine.jpg'

    from azure.cognitiveservices.vision.computervision import ComputerVisionClient
    from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
    from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
    from msrest.authentication import CognitiveServicesCredentials


    #AZURE CV 
    from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
    from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
    from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
    from msrest.authentication import ApiKeyCredentials
    
    from dotenv import load_dotenv
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np

    #print('1')

    load_dotenv()
    prediction_endpoint = "https://yakuzai-proto1-cg.cognitiveservices.azure.com/"
    prediction_key = "383bb86f8f11463a8b2b0b0ad09fa713"
    project_id = "d14e2039-1ab7-428a-94f6-b9c2ae15fd79"
    iterationid = "ff92599b-41a9-4394-9ee3-59913617b465"
    model_name = "Iteration4" 

    #print('2')

    credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
    preiction_client = CustomVisionPredictionClient(endpoint=prediction_endpoint, credentials=credentials)

    #print('3')

    #DETECT OBJECTS IN TEST IMAGE
    #img_file = "./static/photo/input/test.jpg"
    img_file = image_path
    with open(img_file, mode="rb") as image_data:
        #print('image data is ' , image_data , type(image_data))
        results = preiction_client.detect_image(project_id, model_name , image_data)

    #LOAF IMAGE AND GET HEIGHT WIDTH CHANNELS
    try:
        #image_file = "./static/photo/input/test.jpg"
        image_file = image_path
        #print('Detecting objects in ', img_file,type(img_file))
        img = Image.open(img_file)
        #print('img type is ', img, type(img))

        img_height, img_width, img_ch = np.array(img).shape

        rotatedimage = img.rotate(0)
        draw = ImageDraw.Draw(rotatedimage)
        

        #lineWidth = int(img_width/150)
        lineWidth = 1
        color = 'red'
    
    except:
        print('IMAGE FILE OPENING ERROR ... EXITING..')


    #print('7')

    #print('result is ', results)

    count = 0

    for count,prediction in enumerate(results.predictions):

        if(prediction.probability*100) >= 99:
            count += 1

        #print('prediction probability are ' ,prediction )

        #set threshold > 50%
        if(prediction.probability*100) >= 99:

            #Box coordinates and dimensions are proportioinal... convert to 
            left = prediction.bounding_box.left * img_width
            top = prediction.bounding_box.top * img_height
            height = prediction.bounding_box.height * img_height
            width = prediction.bounding_box.width * img_width

            # DRAW THE BOX
            draw.rectangle((left, top, left+width, top+height), outline=color, width=lineWidth)
            a = str(prediction.tag_name).encode().decode('utf8')
            print('a is ', a)
            
            print('does it exist ???????????????????? ' , os.path.exists(os.path.join(settings.STATIC_DIR, "fonts/MSMINCHO.TTF")))
            
            print(os.path.join(settings.STATIC_DIR, 'fonts/MSMINCHO.TTF') )
            
            font = ImageFont.truetype(os.path.join(settings.STATIC_DIR, "fonts/MSMINCHO.TTF"), 50)
            draw.text((left, top-40), str(a) + ' ' +  str(f"{prediction.probability * 100 :.2f}%"), fill='white' , font=font)
            #ADDING TAGNAME
            #plt.annotate(prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))

            try:
                cropped_tablets = img.crop((left, top, left+width, top+height))

                # if str(tagname) == "karonaru":
                #     path = "tooooooooo_cropped_tablets"+str(tagname)+str(random.randint(1,100))+str(count)+".jpg"
                # else:
                #     path = "tooooooooo_cropped_tablets"+str(tagname)+str(count)+".jpg"

                path = 'static/cropped_images/yakuzai'+str(count)+'.jpg'
                cropped_tablets.save(path)

            except Exception as e:
                print('Cropping seperate tablets failed !!' , e)


