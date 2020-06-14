import imutils
import cv2
import numpy as np
import matplotlib.pyplot as plt
from imutils.video import VideoStream
from imutils import face_utils
import time
import dlib
import math as mt

DLIB_5_MODEL_PATH="models/shape_predictor_5_face_landmarks.dat"

detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor(DLIB_5_MODEL_PATH)

def draw_map(frame):
    cv2.ellipse(frame, (200, 135), (90, 120), 0, 0, 360, (255, 255, 255), 1)
    cv2.ellipse(frame, (200, 135), (90, 90), 0, 0, 360, (255, 255, 255), 1)
    cv2.ellipse(frame, (200, 135), (90, 30), 0, 0, 360, (255, 255, 255), 1)
    cv2.ellipse(frame, (200, 135), (60, 120), 0, 0, 360, (255, 255, 255), 1)
    cv2.ellipse(frame, (200, 135), (30, 120), 0, 0, 360, (255, 255, 255), 1)

    return 

def gen_emp_face(emp_name):
    vs=VideoStream(src=0, framerate=50).start()
    time.sleep(2.0)
    face_found=False
    cropped_face=None
    correct_image=None
    coords_eye_x=[]
    coords_eye_y=[]
    coords_nose_x=[]
    coords_nose_y=[]
    while True:
        frame=vs.read()
        frame=imutils.resize(frame, width=400)
        frame=cv2.flip(frame, 1)
        frame_orig=frame.copy()
        draw_map(frame)
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects=detector(gray, 0)

        if len(rects)==0:
            text="No face found.\n Please adjust lighting and remove spectacles"
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
            for(i, (x, y)) in enumerate(shape):
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                cv2.putText(frame, str(i+1), (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                face_points.append((x, y))
            
            eye1_cen=((face_points[0][0]+face_points[1][0])//2 , (face_points[0][1]+face_points[1][1])//2)
            eye2_cen=((face_points[2][0]+face_points[3][0])//2 , (face_points[2][1]+face_points[3][1])//2)
            
            eye_cen=((eye1_cen[0]+eye2_cen[0])//2, (eye1_cen[1]+eye2_cen[1])//2)
            nose=face_points[4]

            coords_eye_x.append(eye1_cen[0])
            coords_eye_y.append(eye2_cen[0])
            coords_nose_x.append(nose[0])
            coords_nose_y.append(nose[1])

            angle=slope(eye1_cen, eye2_cen)
            cv2.putText(frame, str(angle), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


        cv2.imshow("Frame", frame)
        key=cv2.waitKey(1) & 0xFF
        if key==ord("q"):
            break
    
    cv2.destroyAllWindows()
    vs.stop()
    return [coords_eye_x, coords_eye_y, coords_nose_x, coords_nose_y]

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

coords=gen_emp_face("random")
coords=np.array(coords)
coords=coords.T
print(coords.shape)
plt.figure()
plt.plot(coords[:, 0]-coords[:, 1], color='green', marker='o', linestyle='dashed', linewidth=2, markersize=3)
plt.plot(coords[:, 0], color='red', marker='x', linestyle='solid', linewidth=2, markersize=3)
plt.plot(coords[:, 1], color='blue', marker='x', linestyle='solid', linewidth=2, markersize=3)
plt.show()