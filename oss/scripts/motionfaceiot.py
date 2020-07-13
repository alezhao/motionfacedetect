# -*- coding: utf-8 -*-
import cv2,os,sys
import time
import random
import numpy as np
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "{Azure IoT Hub Connection String}"
client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
model = cv2.face.EigenFaceRecognizer_create()
model.read('facemodel')
print('Model load successfully!')
names = ['{Trained Facial Name}']

def motion_detect():
    camera = cv2.VideoCapture(0)   
    if camera is None:
        print('please connect the camera')
        exit()
    
    fps = 30    
    pre_frame = None  
    
    led = False
    icount=0
    
    while True:
        start = time.time()
    
        res, cur_frame = camera.read()
        if res != True:
            break
        end = time.time()
        
        seconds = end - start
        if seconds < 1.0/fps:
            time.sleep(1.0/fps - seconds)
        
        cv2.namedWindow('motiondetect',0);
        cv2.resizeWindow("motiondetect", 640, 480);
        key = cv2.waitKey(30) & 0xff
        if key == 27:
            break

        gray_img = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)
        gray_img = cv2.resize(gray_img, (500, 500))
        gray_img = cv2.GaussianBlur(gray_img, (21, 21), 0)
    
        if pre_frame is None:
            pre_frame = gray_img
        else:
            img_delta = cv2.absdiff(pre_frame, gray_img)
            thresh = cv2.threshold(img_delta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours, hierarchy =   cv2.findContours(thresh.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            for c in contours:
                if cv2.contourArea(c) < 1000:
                    continue
                else:
                    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                    faces = face_cascade.detectMultiScale(cur_frame, 1.3, 5)
                    for (x, y, w, h) in faces:
                        img = cv2.rectangle(cur_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        gray = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)
                        roi = gray[x: x+w, y: y+h]
                        try:
                            icount = icount + 1
                            roi = cv2.resize(roi, (200, 200), interpolation=cv2.INTER_LINEAR)
                            params = model.predict(roi)
                            #print("Label: %s, Confidence: %.2f" % (params[0], params[1]))
                            cv2.putText(cur_frame, names[params[0]], (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            msg = '{} is moving!!! {}'.format(names[params[0]], icount)
                            message = Message(msg)
                            client.send_message(message)
                            print ( "Message {} successfully sent to Azure IOT HUB".format(icount) )  
                        except:
                            continue

            cv2.imshow('motiondetect', cur_frame)	
            pre_frame = gray_img
    
    camera.release()

def read_images(path, sz = None):
    c = 0
    X, y = [], []

    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)#./data/at/*
            for filename in os.listdir(subject_path):
                try:
                    if not filename.endswith('.pgm'):
                        continue
                    filepath = os.path.join(subject_path, filename)
                    im = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                    if sz is not None:
                        im = cv2.resize(im,(200,200))
                    X.append(np.asarray(im, dtype=np.uint8))
                    y.append(c)
                except:
                    print("Unexpected error:",sys.exc_info()[0])
            c = c + 1
    return [X, y]

def face_rec(img_path):
    [X,y] = read_images(img_path)
    y = np.asarray(y, dtype=np.int32)
    model.train(np.asarray(X), np.asarray(y))
    print('train successful')
    
if __name__ == "__main__":
    motion_detect()
