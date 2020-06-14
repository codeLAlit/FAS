from imutils.video import VideoStream
from imutils import face_utils
import os
import cv2
import time
import imutils
import dlib

DLIB_5_MODEL_PATH="models/shape_predictor_5_face_landmarks.dat"

detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor(DLIB_5_MODEL_PATH)

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


# img=capture_face()


