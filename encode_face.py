import face_recognition
import pickle
import cv2
import os
import json
import numpy as np
import codecs

def encode_image(image, emp_name, is_cnn=True, ):
    #####
    #For creating encode for a image to check
    #####
    known_encoding=[]
    try:
        image_rgb=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except:
        image_rgb=image
    
    if(is_cnn):
        model="cnn"
    else:
        model="hog"
    boxes = face_recognition.face_locations(image_rgb, model=model)
    encodings=face_recognition.face_encodings(image_rgb, boxes)

    for encoding in encodings:
        known_encoding.append(encoding)
    
    emp_data={}
    emp_data["name"]=emp_name
    emp_data["encodings"]=np.array(know_encoding)

    return emp_data

def gen_emp_data(image_directory, emp_name, encode_dir, is_cnn=True):
    emp_encodings=[]
    img_files=os.listdir(image_directory)
    for img in img_files:
        known_encoding=[]
        image=cv2.imread(os.path.join(image_directory, img))
        image_rgb=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if(is_cnn):
            model="cnn"
        else:
            model="hog"
        
        boxes = face_recognition.face_locations(image_rgb, model=model)
        encodings=face_recognition.face_encodings(image_rgb, boxes)

        for encoding in encodings:
            known_encoding.append(encoding)
        
        emp_encodings.append(known_encoding)
    
    encodings=np.asarray(emp_encodings)
    file_name=encode_dir+emp_name+"_face_encodings.npy"
    np.save(file_name, encodings)


#### For testing #####
# image=cv2.imread("dataset/face1.jpeg")
# gen_emp_data("dataset/faces/", "ranodm", "dataset/encodings/", True)
# data=encode_image(image,  "Random", True )
# print(data)
