# -*- coding: utf-8 -*-
import cv2,os,sys
import time
import random
import numpy as np

model = cv2.face.EigenFaceRecognizer_create()

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
    model.write('facemodel')
    print('train successful')
    
if __name__ == "__main__":
    face_rec(r'./train/')
