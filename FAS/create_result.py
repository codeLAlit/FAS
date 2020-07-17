import os
import cv2
import imutils
import face_recognition
import dlib
import json
import numpy as np
from .face_capture import capture_face
from .encode_face import encode_image
import matplotlib.pyplot as plt


ENCODINGS_DIR="FAS/dataset/encodings/"

def universe_vectors(num_univ, dimension, vec_per_univ):
    ## Run when you initialize
    univ_dict={}
    for i in range(num_univ):
        vecs=np.random.normal(size=(vec_per_univ, dimension))
        univ_dict[i]=vecs.tolist()
    with open("FAS/dataset/univ_data.json", 'w') as f:
        json.dump(univ_dict, f)
    
def get_hash_value(univ_vectors, vec):
    dot=np.dot(univ_vectors, vec)
    signs=np.maximum(np.sign(dot).squeeze(), 0)
    hash_val=0
    for i in range(signs.shape[0]):
        hash_val+=(2**i)*signs[i]
    return hash_val

def get_check_vecs(all_vecs, vec):
    with open("FAS/dataset/univ_data.json", 'r') as fp:
        univs=json.load(fp)

    selected_vecs=[]
    for key in univs.keys():
        univ_vecs=np.array(univs[key])
        hash_req=get_hash_value(univ_vecs, vec)
        for vec_other in all_vecs:
            if(get_hash_value(univ_vecs, vec_other)==hash_req):
                selected_vecs.append(vec_other)
    
    return selected_vecs

def make_universe(num_employees, encoding_dimension):
    num_univs=5
    num_buckets=num_employees/50.0
    num_planes=int(np.log2(num_buckets))+1
    encoding_dimension=128
    universe_vectors(num_univs, encoding_dimension, num_planes)

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
        sel_vecs=get_check_vecs(encodings, encode_image)
        for sel_vec in sel_vecs:
            if ismatched(sel_vec, encoded_image):
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

