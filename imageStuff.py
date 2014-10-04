#!/usr/bin/python
"""
Program to detect eyes and replace them with googly eyes. Based off of the OpenCV example code facedetect.py
---------
This program is demonstration for face and object detection using haar-like features.
The program finds faces in a camera image or video stream and displays a red box around them.

Original C implementation by:  ?
Python implementation by: Roman Stanchak, James Bowman
"""
import sys
import cv2.cv as cv
import cv2
import time
# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned
# for accurate yet slow object detection. For a faster operation on real video
# images the settings are:
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING,
# min_size=<minimum possible face size

min_size = (2, 2)
image_scale = 1
haar_scale = 1.07
min_neighbors = 5
haar_flags = 0
def greenish(color):
    if color[0] < 60:
        if color[2] < 60:
            if color[1] > 120:
                return True
    return False
    
def detect(img, cascade):
    # allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
                   cv.Round (img.height / image_scale)), 8, 1)

    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    cv.EqualizeHist(small_img, small_img)

    if(cascade):
        objects = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        return objects

    return []

if __name__ == '__main__':
    googlyEye = cv2.imread("eye2.jpg",1)
    for input_name in sys.argv[1:]:
        startTime = time.time()
        image = cv.LoadImage(input_name, 1)
        faces = detect(image, cv.Load("haarcascade_frontalface_default.xml")) # Do facedetection
        leftEyes = []
        rightEyes = []
        for ((x, y, w, h), n) in faces:
            foundLeft = None
            foundRight = None
            tempImage = image[y:y+h, x:x+w]
            #cv.SaveImage("face"+str(n)+".jpg", tempImage)
            leftEye = detect(tempImage, cv.Load("haarcascade_lefteye_2splits.xml")) # Detect left eye --only--
            if len(leftEye) == 1:
                #print "LEFT"
                foundLeft = list(leftEye[0][0])
            
            rightEye = detect(tempImage, cv.Load("haarcascade_righteye_2splits.xml")) # Detect right eye --only--
            if len(rightEye) == 1:
                #print "RIGHT"
                foundRight = list(rightEye[0][0])
                        
            if ((foundLeft == None) or (foundRight == None)):
                # If we have the incorrect number of eyes, find eyes on own
                eyes = detect(tempImage, cv.Load("haarcascade_eye.xml"))
                if len(eyes) == 2: # people should have 2 eyes
                    #print "BOTH"
                    eyes = sorted(eyes, key = lambda x: x[0][0])
                    foundRight = list(eyes[0][0])
                    foundLeft = list(eyes[1][0])
            # Shift the found coordinates to the full size image
            if(foundLeft and foundRight):
                foundLeft[0] += x
                foundLeft[1] += y
                foundRight[0] += x
                foundRight[1] += y
                leftEyes.append(foundLeft)
                rightEyes.append(foundRight)
        for x, y, w, h in leftEyes:
            # the input to cv.HaarDetectObjects was resized, so scale the
            # bounding box of each face and convert it to two CvPoints
            pt1 = (int(x * image_scale), int(y * image_scale))
            pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
            #cv.Rectangle(image, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
            tEye =  cv.CreateImage((w,h), 8, 3)
            resized = cv2.resize(googlyEye, (w,h))
            smallEye = cv.fromarray(resized)
            for i in range(int(x * image_scale), int((x + w) * image_scale)):
                for j in range(int(y * image_scale), int((y + h) * image_scale)):
                    if not greenish(smallEye[j-int(y * image_scale), i - int(x * image_scale)]):
                        image[j,i]=smallEye[j-int(y * image_scale), i - int(x * image_scale)]
            #image[y:y+h, x:x+w] = smallEye[:,:]
        for x, y, w, h in rightEyes:
            # the input to cv.HaarDetectObjects was resized, so scale the
            # bounding box of each face and convert it to two CvPoints
            pt1 = (int(x * image_scale), int(y * image_scale))
            pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
            #cv.Rectangle(image, pt1, pt2, cv.RGB(0, 255, 0), 3, 8, 0)
            tEye =  cv.CreateImage((w,h), 8, 3)
            resized = cv2.resize(googlyEye, (w,h), interpolation = cv2.INTER_AREA)
            smallEye = cv.fromarray(resized)
            for i in range(int(x * image_scale), int((x + w) * image_scale)):
                for j in range(int(y * image_scale), int((y + h) * image_scale)):
                    if not greenish(smallEye[j-int(y * image_scale), i - int(x * image_scale)]):
                        image[j,i]=smallEye[j-int(y * image_scale), i - int(x * image_scale)]
        if (len(leftEyes) > 0):
            cv.SaveImage(input_name+"_result.jpg", image)        
        print "This image took "+str(time.time()-startTime)+" seconds to process."