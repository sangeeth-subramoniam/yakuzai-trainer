from email.mime import image
from random import randint

def colour_detector(hue_value):

    """ DETECTS THE COLOUR OF THE HUE VALUE THAT IS PASSED """

    print('ENTERED THE COLOR DETECTIN WITH HUE VALUE ', hue_value)

    color = "Undefined"

    if hue_value < 1:
        color = "BLACK"
    elif hue_value < 5:
        color = "RED"
    elif hue_value < 15:
        color = "ORANGE"
    elif hue_value < 28:
        color = "WHITE"
    elif hue_value < 33:
        color = "YELLOW"
    elif hue_value < 78:
        color = "GREEN"
    elif hue_value < 131:
        color = "BLUE"
    elif hue_value < 170:
        color = "VIOLET"
    else:
        color = "RED"

    return color


def count_yakuzai():

    import random

    from flask import session

    #COMPUTER VISION OCR

    # print('imagefile tagname is  ' , tagname)
    print('imagefile path is  ' , image_path)

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
            font = ImageFont.truetype("./fonts/MSMINCHO.TTF", 50)
            draw.text((left, top-40), str(a) + ' ' +  str(f"{prediction.probability * 100 :.2f}%"), fill='white', font=font)
            #ADDING TAGNAME
            #plt.annotate(prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))

            try:
                cropped_tablets = img.crop((left, top, left+width, top+height))

                # if str(tagname) == "karonaru":
                #     path = "tooooooooo_cropped_tablets"+str(tagname)+str(random.randint(1,100))+str(count)+".jpg"
                # else:
                #     path = "tooooooooo_cropped_tablets"+str(tagname)+str(count)+".jpg"

                path = 'static/cropped_images/yakuzai'+count+'.jpg'
                cropped_tablets.save(path)

            except Exception as e:
                print('Cropping seperate tablets failed !!' , e)

