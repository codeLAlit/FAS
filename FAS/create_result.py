import os
import cv2
import imutils
import face_recognition
import dlib
import numpy as np
from .face_capture import capture_face
from .encode_face import encode_image
import matplotlib.pyplot as plt


ENCODINGS_DIR="FAS/dataset/encodings/"

def ismatched(available_encoding, given_encoding, thresh=0.6):
    match=np.linalg.norm(available_encoding-given_encoding, axis=1)
    if match<=0.6:
        return True
    return False

def find_emp():
    image=capture_face()
    encoded_image=encode_image(image)
    if len(encoded_image)==0:
        return "Invalid Image", -1
    match_list=[]
    for encoded_file in os.listdir(ENCODINGS_DIR):
        matches=0
        match_dict={}
        emp_name=encoded_file.split('_')[0]
        encodings=np.load(ENCODINGS_DIR+encoded_file)
        for encoding in encodings:
            if ismatched(encoding, encoded_image):
                matches+=1
        match_dict["name"]=emp_name
        match_dict["votes"]=matches
        match_list.append(match_dict)
    
    max_match=0
    name=None
    for ent in match_list:
        if ent["votes"]>max_match:
            max_match=ent["votes"]
            name=ent["name"]

    return name, max_match

