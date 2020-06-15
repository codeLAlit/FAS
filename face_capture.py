from imutils.video import VideoStream
from imutils import face_utils
import os
import cv2
import time
import imutils
import dlib
import math as mt
import numpy as np
import matplotlib.pyplot as plt
import shutil

DLIB_5_MODEL_PATH="models/shape_predictor_5_face_landmarks.dat"
FACES_PARENT="dataset/faces/"

detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor(DLIB_5_MODEL_PATH)
predictor_align=dlib.shape_predictor(DLIB_5_MODEL_PATH)

def capture_face():
    vs=VideoStream(src=0, framerate=50).start()
    time.sleep(2.0)
    face_found=False
    cropped_face=None
    while True:
        frame=vs.read()
        fram=imutils.resize(frame, width=400)
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects=detector(gray, 0)

        if len(rects)>1:
            text="{} face(s) found. Please be single in the frame.".format(len(rects))
            cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        if len(rects)==1:
            text="Face detected"
            cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            rect=rects[0]
            (bx, by, bw, bh)=face_utils.rect_to_bb(rect)
            cropped_face=frame[by:by+bh+1, bx:bx+bw+1, :]
            face_found=True

            
        cv2.imshow("Frame", frame)
        key=cv2.waitKey(1) & 0xFF
        if key==ord('q') or face_found:
            break
        
    cv2.destroyAllWindows()
    vs.stop()
    return cropped_face


def gen_emp_face(emp_name):
    vs=cv2.VideoCapture(0)
    time.sleep(3.0)
    face_found=False
    cropped_face=None
    correct_image=None
    time_prev=time.time()
    count=0

    if os.path.exists(FACES_PARENT+emp_name):
        shutil.rmtree(FACES_PARENT+emp_name)
    os.mkdir(FACES_PARENT+emp_name)

    while True:
        __, frame=vs.read()
        frame=imutils.resize(frame, width=400)
        frame=cv2.flip(frame, 1)
        frame_orig=frame.copy()
        draw_map(frame, count)
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects=detector(gray, 0)

        if len(rects)==0:
            text="No face found"
            cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        elif len(rects)>1:
            text="{} face(s) found. Please be single in the frame.".format(len(rects))
            cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        elif len(rects)==1:
            text="Face detected"
            cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            rect=rects[0]

            (bx, by, bw, bh)=face_utils.rect_to_bb(rect)
            cv2.rectangle(frame, (bx, by), (bx+bw, by+bh), (0, 255, 0), 1)
            shape=predictor(gray, rect)
            shape=face_utils.shape_to_np(shape)
            face_points=[]
            inside=True
            for(i, (x, y)) in enumerate(shape):
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                face_points.append((x, y))
                if x>270 or x<110 or y<30 or y>135 and i!=4:
                    inside=False
            
            eye1_cen=((face_points[0][0]+face_points[1][0])//2 , (face_points[0][1]+face_points[1][1])//2)
            eye2_cen=((face_points[2][0]+face_points[3][0])//2 , (face_points[2][1]+face_points[3][1])//2)
            angle=slope(eye1_cen, eye2_cen)
            cv2.putText(frame, str(angle), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # print(time_prev-time.time())
            if time.time()-time_prev>1 and count<=25 and inside:
                time_capture=time.time()
                time_prev=time_capture
                adjusted=correct_orientation(frame_orig, rect)
                cv2.imwrite(FACES_PARENT+emp_name+"/"+str(count)+".jpg", adjusted)              
                count+=1
            elif not inside:
                cv2.putText(frame, "Be inside the grid", (150, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        if count>25:
            cv2.putText(frame, "Done, Press q", (200, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.imshow("Frame", frame)
        key=cv2.waitKey(1) & 0xFF
        if key==ord("q"):
            break

    vs.release()
    cv2.destroyAllWindows()
    
    return

def slope(t1, t2):
    diff_x=abs(t2[0]-t1[0])
    diff_y=abs(t2[1]-t1[1])
    if diff_x==0:
        return 90
    elif diff_y==0:
        return 0
    slope=mt.atan(diff_y/diff_x)
    angle=mt.degrees(slope)
    angle=round(angle, 2)
    return angle

def correct_orientation(image, rect):
    gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    shape=predictor_align(gray, rect)
    shape=face_utils.shape_to_np(shape)

    left_eye=shape[0:2]
    right_eye=shape[2:4]

    left_eye_cen=left_eye.mean(axis=0).astype(int)
    right_eye_cen=right_eye.mean(axis=0).astype(int)

    dy=right_eye_cen[1]-left_eye_cen[1]
    dx=right_eye_cen[0]-left_eye_cen[0]
    angle=np.degrees(np.arctan2(dy,dx))-180

    desired_left_eye=(0.35, 0.35)
    desired_face_width=256
    desired_face_height=256

    desired_right_eyex=1.0-desired_left_eye[0]
    dist=np.sqrt((dx**2)+(dy**2))
    desired_dist=(desired_right_eyex-desired_left_eye[0])
    desired_dist*=desired_face_width
    scale=desired_dist/dist

    eyes_cen=((left_eye_cen[0]+right_eye_cen[0])//2, (left_eye_cen[1]+right_eye_cen[1])//2)
    M=cv2.getRotationMatrix2D(eyes_cen, angle, scale)
    tx=desired_face_width*0.5
    ty=desired_face_height*desired_left_eye[1]
    M[0,2]+=(tx-eyes_cen[0])
    M[1, 2]+=(ty-eyes_cen[1])
    
    output=cv2.warpAffine(image, M, (desired_face_width, desired_face_height), flags=cv2.INTER_CUBIC)
    return output

def draw_map(frame, count):
    cv2.ellipse(frame, (200, 135), (90, 120), 0, 0, 360, (255, 255, 255), 1)
    cv2.ellipse(frame, (200, 135), (90, 90), 0, 0, 360, (255, 255, 255), 1)
    cv2.ellipse(frame, (200, 135), (90, 30), 0, 0, 360, (255, 255, 255), 1)
    cv2.ellipse(frame, (200, 135), (60, 120), 0, 0, 360, (255, 255, 255), 1)
    cv2.ellipse(frame, (200, 135), (30, 120), 0, 0, 360, (255, 255, 255), 1)
    
    ### Progress bar
    cv2.putText(frame, "Progress Bar", (10, 285), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.rectangle(frame, (10, 290), (390, 295), (0, 255, 0), 1)
    cv2.rectangle(frame, (10, 290), (10+count*15, 295), (0, 255, 0), -1)
    return 

gen_emp_face("lalit") 
# print(img.shape)
# plt.figure()
# plt.imshow(img)
# plt.show()
# img=capture_face()


