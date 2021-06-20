from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import imutils
import cv2,os,urllib.request
import numpy as np
from django.conf import settings



class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        facecascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') #using the cascade classifier for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #converting whatever we are reading into gray
        faces = facecascade.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5) #this helps in finding features and location in our images - we are passing in our grayscale input, we are scaling down the image which is done with scaleFactor 
        # min neighbors helps in determining the quality of detection
        #emotion_dict = {0:'Angry',1:'Disgust',2:'Fear',3:'Happy',4:'Neutral',5:'Sad',6:'Surprise'} #dictionary containing different values
        for (x, y, w, h) in faces: #drawing rectangles on the faces detected and also adding text
            cv2.rectangle(image, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2) #used to draw our rectangle, we are specifying the start and end point and also color and width of our rectangle
            #roi_gray = gray[y:y + h, x:x + w] #ROI - Region of interest, in this we are trying to select the rows starting from y to y+h and then columns from x to x+h - this works like NumPy slicing
            #cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0) #resizing the inputs in order to get  them in the same shape as the images on which our images were trained
            #prediction = model.predict(cropped_img) #making predictions on the face detected
            #maxindex = int(np.argmax(prediction)) #getting the maximum index out of all the predicted indices
            #cv2.putText(image, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA) #printing the emotion label corresponding to the output index from our emotio dictionary
        
        frame_flip = cv2.flip(image,1)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()