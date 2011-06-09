# -*- coding: utf-8 -*-

from opencv.cv import cvCreateImage, cvCvtColor, cvGet2D, cvInRangeS, cvOr, cvAnd, cvSplit, cvSetZero, cvCopy, cvInitFont, cvPoint, cvSize, IPL_DEPTH_8U, CV_BGR2HLS, CV_FONT_HERSHEY_COMPLEX, cvPutText, CV_RGB, cvZero
from opencv.highgui import cvGrabFrame, cvQueryFrame, cvCreateCameraCapture, cvSetTrackbarPos, cvNamedWindow, cvCreateTrackbar, cvSetMouseCallback, cvShowImage, cvDestroyWindow, cvSetCaptureProperty, CV_CAP_PROP_FRAME_WIDTH, CV_CAP_PROP_FRAME_HEIGHT, CV_CAP_PROP_FPS, CV_EVENT_LBUTTONUP, cvWaitKey, cvReleaseCapture 
from sys import argv
from time import sleep

CAM = cvCreateCameraCapture(0)

delayS = 5
camStartUpTime = 30 # time needed for the webcam to adjust colors and make a correct frame

hlsFilter = {'hmin': 0, 'hmax': 180, 
                 #'lmin': 0, 'lmax': 255,
                 'smin': 0, 'smax': 255} # Accept all

def resetHlsFilter():
    setHlsFilter('hmin', 0)
    setHlsFilter('hmax', 180)
    #setHlsFilter('lmin', 0)
    #setHlsFilter('lmax', 255)
    setHlsFilter('smin', 0)
    setHlsFilter('smax', 255)

def setHlsFilter(key, value):
    hlsFilter[key] = value
    print key
    cvSetTrackbarPos(key, "Filtred", int(value))
    print str(key) + "a"
    print hlsFilter


def getHlsFilter(key):
    return hlsFilter[key]

# Event handlers
def trackBarChangeHmax(pos):
    global hlsFilter
    hlsFilter['hmax'] = int(pos)
    
def trackBarChangeHmin(pos):
    global hlsFilter
    hlsFilter['hmin'] = int(pos)
    
#def trackBarChangeLmax(pos):
    #hlsFilter['lmax'] = pos
    
#def trackBarChangeLmin(pos):
    #hlsFilter['lmin'] = pos
    
def trackBarChangeSmax(pos):
    global hlsFilter
    hlsFilter['smax'] = int(pos)
    
def trackBarChangeSmin(pos):
    global hlsFilter
    hlsFilter['smin'] = int(pos)

def mouseClick(event, x, y, flags, param):
    if event == CV_EVENT_LBUTTONUP:
        frame = cvQueryFrame(CAM)
        hlsFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 3)
        cvCvtColor(frame, hlsFrame, CV_BGR2HLS)

        pixel = cvGet2D(hlsFrame, y, x)
                
        setHlsFilter('hmax', pixel[0])      
        setHlsFilter('hmin', pixel[0])        
        #setHlsFilter('lmax', pixel[1])        
        #setHlsFilter('lmin', pixel[1])        
        setHlsFilter('smax', pixel[2])        
        setHlsFilter('smin', pixel[2])        

def pixelInRange(src, rmin, rmax, floor, roof, dst):
    if rmax > rmin: # normal case
        cvInRangeS(src, rmin, rmax, dst)
    else: # considering range as a cycle
        dst0 = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)
        dst1 = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)
        cvInRangeS(src, floor, rmax, dst0)
        cvInRangeS(src, rmin, roof, dst1)
        cvOr(dst0, dst1, dst)

# Window to get an adjust color to make transparent
def getFilter(frameWidht, frameHeight):    
    cvNamedWindow("Filtred")
    
    cvCreateTrackbar("hmax", "Filtred", getHlsFilter('hmax'), 180, trackBarChangeHmax)
    cvCreateTrackbar("hmin", "Filtred", getHlsFilter('hmin'), 180, trackBarChangeHmin)
    #cvCreateTrackbar("lmax", "Filtred", hlsFilter['lmax'], 255, trackBarChangeLmax)
    #cvCreateTrackbar("lmin", "Filtred", hlsFilter['lmin'], 255, trackBarChangeLmin)
    cvCreateTrackbar("smax", "Filtred", getHlsFilter('smax'), 255, trackBarChangeSmax)
    cvCreateTrackbar("smin", "Filtred", getHlsFilter('smin'), 255, trackBarChangeSmin)

    cvSetMouseCallback("Filtred", mouseClick, None)
    
    frame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 3)
    hlsFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 3)
    filtredFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 3)

    mask = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)

    hFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)
    lFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)
    sFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)
    
    ThHFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)
    ThLFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)
    ThSFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)
    
    key = -1
    while key == -1: # fer que sigui enter
        if not cvGrabFrame(CAM):
            print "Could not grab a frame"
            exit
        frame = cvQueryFrame(CAM)
        
        cvCvtColor(frame, hlsFrame, CV_BGR2HLS)
    
        cvSplit(hlsFrame, hFrame, lFrame, sFrame, None)
        
        pixelInRange(hFrame, getHlsFilter('hmin'), getHlsFilter('hmax'), 0, 180, ThHFrame) 
        #pixelInRange(lFrame, getHlsFilter('lmin'), getHlsFilter('lmax'), 0, 255, ThLFrame)
        pixelInRange(sFrame, getHlsFilter('smin'), getHlsFilter('smax'), 0, 255, ThSFrame)
        
        cvSetZero(mask)        
        cvAnd(ThHFrame, ThSFrame, mask)
        
        cvSetZero(filtredFrame)
        
        cvCopy(frame, filtredFrame, mask)
        
        cvShowImage("Filtred", filtredFrame)

        key = cvWaitKey(10)
        if key == 'r':
            key = -1
            resetHlsFilter()
            
    cvDestroyWindow("Filtred")    

def getBackground(frameWidht, frameHeight):
    cvNamedWindow("Background")
    
    text = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 3)
    frame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 3)
    background = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 3)


    font = cvInitFont(CV_FONT_HERSHEY_COMPLEX, 1.0, 1.0, 0.0, 2)
    pt1 = cvPoint(50, 100)
    pt2 = cvPoint(50, 150)
    center = cvPoint(frameWidth/2, frameHeight/2)
    cvPutText(text, "Press enter, run away and wait", pt1, font, CV_RGB(150, 100, 150))
    cvPutText(text, str(delayS) + " seconds to capture background", pt2, font, CV_RGB(150, 100, 150))
    cvShowImage("Background", text)
        
    key = -1
    while key == -1:
        key = cvWaitKey(10)    
        
    like = False
    while not like:
        for i in range(delayS):
            cvZero(text)
            cvPutText(text, str(delayS-i), center, font, CV_RGB(150, 100, 150))
            cvShowImage("Background", text)
            cvWaitKey(1000)
    
        csut = camStartUpTime
        while (csut): # Stats capturing frames in order to give time to the cam to auto-adjust colors
            if not cvGrabFrame(CAM):
                print "Could not grab a frame"
                exit
            cvWaitKey(10)
            csut -= 1
        frame = cvQueryFrame(CAM)
        cvCopy(frame, background)
        
        cvCopy(frame, text)
        cvPutText(text, "Is correct? [y/n]", center, font, CV_RGB(150, 100, 150))

        cvShowImage("Background", text)
        
        key = -1
        while key != 'n' and key != 'y':
            key = cvWaitKey(10)
            if key == 'y': # fer que sigui enter
                like = True
                
    return background        
    cvDestroyWindow("Background")


def startChroma(background, frameWidht, frameHeight):
    #cvNamedWindow("Original")
    cvNamedWindow("Chroma")
    
    hlsFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 3)
    transparency = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 3)

    mask = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)

    hFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)
    lFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)
    sFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)
    
    ThHFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)
    ThLFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)
    ThSFrame = cvCreateImage(cvSize(frameWidth, frameHeight), IPL_DEPTH_8U, 1)
    
    key = -1
    while key == -1:
        if not cvGrabFrame(CAM):
            print "Could not grab a frame"
            exit
        frame = cvQueryFrame(CAM)
        
        cvCvtColor(frame, hlsFrame, CV_BGR2HLS)
    
        cvSplit(hlsFrame, hFrame, lFrame, sFrame, None)

        pixelInRange(hFrame, getHlsFilter('hmin'), getHlsFilter('hmax'), 0, 180, ThHFrame) 
        #pixelInRange(lFrame, getHlsFilter('lmin'), getHlsFilter('lmax'), 0, 255, ThLFrame)
        pixelInRange(sFrame, getHlsFilter('smin'), getHlsFilter('smax'), 0, 255, ThSFrame)

        cvAnd(ThHFrame, ThSFrame, mask)
               
        cvCopy(background, frame, mask)
        
        cvShowImage("Chroma", frame)

        key = cvWaitKey(10)
        
    cvDestroyWindow("Chroma")

if __name__ == '__main__':
    
    print "First adjust the zone that you want to make transparent"
    print "then press Enter to next step or 'r' key to reset values."
    
    if len(argv) > 2:
        writeVideo = True
        outputVideoPath = argv[1]
    else:
        writeVideo = False

    frameWidth = 640
    frameHeight = 480

    fps = 15.0

    if writeVideo:
        writer = cvCreateVideoWriter(argv[1], CV_FOURCC('M','J','P','G'), fps, cvSize(640,480))
    
    cvSetCaptureProperty(CAM, CV_CAP_PROP_FRAME_WIDTH, frameWidth)
    cvSetCaptureProperty(CAM, CV_CAP_PROP_FRAME_HEIGHT, frameHeight)
    cvSetCaptureProperty(CAM, CV_CAP_PROP_FPS, fps)
    
    getFilter(frameWidth, frameHeight)

    background = getBackground(frameWidth, frameHeight)

    startChroma(background, frameWidth, frameHeight)

    cvReleaseCapture(CAM)

    if writeVideo:
        cvReleaseVideoWriter(writer)
        

