#!/usr/bin/python

import numpy as np
import cv2
import time
import subprocess

# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
print("Using OpenCV version: %s.%s.%s" %(major_ver, minor_ver, subminor_ver))

# Exit if not OpenCv version 3 or higher
if int(major_ver)  < 3 :
    exit(1)

'''
# Example of setting camera parameters using Subprocess and v4l2-ctl
cam_props = {'brightness': 128, 'contrast': 128, 'saturation': 180,
             'gain': 0, 'sharpness': 128, 'exposure_auto': 1,
             'exposure_absolute': 150, 'exposure_auto_priority': 0,
             'focus_auto': 0, 'focus_absolute': 30, 'zoom_absolute': 250,
             'white_balance_temperature_auto': 0, 'white_balance_temperature': 3300}

for key in cam_props:
    subprocess.call(['v4l2-ctl -d /dev/video0 -c {}={}'.format(key, str(cam_props[key]))],
                    shell=True)
'''  

# Another example of using subprocess and v4l2-ctl                
# subprocess.call('v4l2-ctl -d /dev/video0 --set-fmt-video=width=640,height=480,pixelformat=1 && v4l2-ctl --set-parm=32', shell=True)
# time.sleep(3)

cap = cv2.VideoCapture(0)
    
'''
# example of ver < 3 function calls
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    print(str(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),str(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
'''

cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
cap.set(cv2.CAP_PROP_FPS,30)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE,0.25) # Disables auto focus
cap.set(cv2.CAP_PROP_EXPOSURE, 0.03) # Slightly faster than 30hz to support 30FPS

fps = cap.get(cv2.CAP_PROP_FPS)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
print("The camera is set to FPS: %s, Frame width: %s, Frame height: %s, Fixed Exposure: %s" %(fps,width,height,exposure))

num_frames =0
timer0 = 0
timer1 = 0
timer2 = 0
timer3 = 0

last_time = time.time()
while(True):
    timer0 += time.time()
    # Capture frame-by-frame
    ret, frame = cap.read() # The time it takes to execute this line of code is limited by the camera
    timer1 += time.time()
    #print(timer1 - timer0)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    timer2 += time.time()
    
    fps_txt = "FPS: " + str(fps)
    cv2.putText(img = frame, text = fps_txt, org = (20,20), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = .7, 
                    color = (0, 255, 0))

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    timer3 += time.time()
        
    # Counting and display frames per minute    
    elapsed_time = time.time() - last_time
    if (elapsed_time > 1 and num_frames > 0):
        last_time = time.time()
        e1 = (timer1 - timer0)/float(num_frames)
        e2 = (timer2 - timer1)/float(num_frames)
        e3 = (timer3 - timer2)/float(num_frames)
        fps = num_frames
        print("Frames: %i   Time: %f   Timer1: %f   Timer2: %f   Timer3: %f" %(fps, elapsed_time, e1, e2, e3))
        num_frames = 0
        timer0 = 0
        timer1 = 0
        timer2 = 0
        timer3 = 0
    num_frames += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
