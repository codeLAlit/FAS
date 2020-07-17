# FAS
FAS is Face based Attendance System. It can be used to mark attendance by capturing an image.

## How to use
- First download the dlib-5 point face detection model from [link](http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2) and paste in FAS/models/
- Run the Django server using `python3 manage.py runserver`
- For adding employee click on **Add Employee**, it will open a page where you enter information for unique identification of an employee.
- After filling information a pop will appear and will capture your images, make sure you complete this process. This is one time process required when a new user is 
  registerd.
- Now click on **Start/Stop** to capture the image for marking attendance.
- Check attendance record in **Check Attendance Record**.

## To Dos
- [ ] Add employee based attendance record searching (easy)
- [ ] Make better UI (easy)
- [ ] Give functionality of live image capture, require making some queue kind of a thing. Whenever system captures an image it store it in a queue performing detection
    and clearing it. (hard)
