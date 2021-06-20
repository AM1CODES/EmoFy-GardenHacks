from django.http import HttpResponse
from django.http.response import StreamingHttpResponse
from django.shortcuts import render
import numpy as np
import cv2
import keras
import tensorflow as tf
import os, urllib.request
from app.camera import VideoCamera

import glob
from PIL import Image as PImage

# Create your views here.

def landing(request):
    return render(request, "app/landing.html")

def index(request):
    return render(request, "app/index.html")

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        
        
def rendervideo(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                        content_type = 'multipart/x-mixed-replace; boundary=frame;')


directory = r'C:/Users/Mihir/Desktop/all folders/Emofy/BackEnd/app/static/images'


def takephoto(request):
    cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
    ret,frame = cap.read() # return a single frame in variable frame
    #os.chdir(directory)
    frame_flip = cv2.flip(frame,1)
    # cv2.imwrite(str(count)+'.jpg',frame_flip)
    cap.release()
    cv2.destroyAllWindows()
    

    #PREDICTING THE IMAGE USING MODEL
    model = keras.models.load_model(os.path.join("C:/Users/Mihir/Desktop/all folders/Emofy/BackEnd/app/"+"model_optimal.h5")) #loading our model that we will use to make predictions of emotions
    #path=(os.path.join(directory)+"/"+str(count)+'.jpg')
    frame = frame_flip
    # isTrue, frame = PImage.imread()
    facecascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml') #using the cascade classifier for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converting whatever we are reading into gray
    faces = facecascade.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)
    
    emotion_dict = {0:'Angry',1:'Disgust',2:'Fear',3:'Happy',4:'Neutral',5:'Sad',6:'Surprise'} #dictionary containing different values
    maxindex=0
    
    for (x, y, w, h) in faces: #drawing rectangles on the faces detected and also adding text
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2) #used to draw our rectangle, we are specifying the start and end point and also color and width of our rectangle
        roi_gray = gray[y:y + h, x:x + w] #ROI - Region of interest, in this we are trying to select the rows starting from y to y+h and then columns from x to x+h - this works like NumPy slicing
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0) #resizing the inputs in order to get  them in the same shape as the images on which our images were trained
        prediction = model.predict(cropped_img) #making predictions on the face detected
        maxindex = int(np.argmax(prediction)) #getting the maximum index out of all the predicted indices
        cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA) #printing the emotion label corresponding to the output index from our emotio dictionary
    
    context = {"img_name": str(count)+'.jpg',"prediction":emotion_dict[maxindex]}
    # count+=1
    return render(request, "app/playlist.html", context)

count=0

def aboutus(request):
    return render(request, "app/about.html")