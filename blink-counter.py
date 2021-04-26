###########################################################################################################
#  ***** blink-counter.py ***** 
###########################################################################################################
#  Author: Ikram Hamizi
#  Objective: EOPA INTERNSHIP TEST (26/04/2020) 
#  Task: Eye Blink Detection 
#  Source: https://docs.google.com/document/d/1OI6eVR09Bgokbnmrb__sYkVJrlXiviv1NyUF4VcfrZA/edit?usp=sharing
###########################################################################################################
''' README.md
###########################################################################################################

PROGRAM: detects the number of blinks of a person in real time. 
- INPUT: video from a file path / video from a webcam.
- OUTPUT: Window with the video + the number of blinks

PROPERTIES:
1- One person should be in the video (+)
2- The face of the person should cover at least 1/3 of the frame (pixels) (+)
3- Minimum resolution should be 480p using the (4:3) Standard (i.e. 480x640p) (+)

4- Increments the number of blinks [upper-left corner]
5- If the eyes are closef for more than 2 seconds, a message "Alert!" appears in red (+ an --alarm sound option) (+)
6- Draws the facial landmarks (eyes + bounding box of the face (+))

SOURCE: the program is written following the guide in [https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/]
- The calculation of the Eye Aspect Ratio 
- Detect the facial landmarks: dlib library
- Drawing of landmarks: cv2 and with the help of imutils libraries
'''

###################################
#     ***** LIBRARIES ***** 
###################################
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream #to access a video file on disk 
from imutils.video import VideoStream #to access built-in webcam module
from imutils import face_utils
import threading
import pygame
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
#from google.colab.patches import cv2_imshow # if on google colab

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor",  required=True,   help="path to facial landmark predictor")
ap.add_argument("-a", "--alarm"           , default=False,   help="usage: -a True (to activate alarm option) or -a False") #flag (no input required)
ap.add_argument("-v", "--video",  type=str, default="",      help="path to input video file")
ap.add_argument("-w", "--webcam", type=int, default=0,       help="index of webcam on system (integer: 0,1,..)")
ap.add_argument("--EAR",        type=float, default=0.25,    help="EAR threshold to count a blink")
args = vars(ap.parse_args())

###################################
#   ***** GLOBAL VARIABLES ***** 
###################################
EYE_AR_THRESH = args["EAR"]        # EAR Threshold to determine a blink (to compare var: ear)
EYE_AR_CONSEC_FRAMES = 3    # FRAMES Threshold of successive frames with ear<0.3 (to compare var: FRAME_COUNTER)
TIME_ALARM_THRESH = 2       # Threshold number of seconds to trigger the alarm (to compare var: closed_eyes_elapsed_time)


FRAME_COUNTER = 0 # Number of successive frames when ear<0.3 
BLINK_COUNTER = 0 # Number of blinks

sound_alarm_path = "Loud_Alarm_Clock_Buzzer.wav" #link: https://soundbible.com/2061-Loud-Alarm-Clock-Buzzer.html
sound_alarm_player = None

ALARM_already_on = False 
closed_eyes_elapsed_time = 0.0
closed_eyes_timer_start = 0.0
closed_eyes_timer_next = 0.0

###################################
#     ***** FUNCTIONS ***** 
###################################
''' func1:   eye_aspect_ratio(array)
    args:    eye (array of length 6 points)
    return:  EAR metric'''
def eye_aspect_ratio(eye):

    # compute the euclidean distances between the vertical eye landmarks 
    A = dist.euclidean(eye[1], eye[5]) #between (P2(x,y) and P6(x,y))
    B = dist.euclidean(eye[2], eye[4]) #between (P3(x,y) and P5(x,y))

    # compute the euclidean distance between the horizontal eye landmark
    C = dist.euclidean(eye[0], eye[3]) #between (P1(x,y) and P4(x,y))

    # compute the eye aspect ratio (EAR)
    ear = (A + B) / (2.0 * C)
    return ear


''' class: sound_alarm'''     
class sound_alarm:

  ''' func_i __init__
      args: path to sound alarm file''' 
  def __init__(self, path): 
    pygame.init()
    pygame.mixer.music.load(path)

  ''' func2: sound_alarm.play(stop_event)
      args: stop_event 
      behavior: stop playing if stop_event is not set'''
  def play(self, stop_event):
      while True:
        pygame.mixer.music.play()
        time.sleep(2)  
        
        if stop_event.is_set():
          pygame.mixer.music.stop()
          break;
  

###################################
#     ***** SCRIPT ***** 
###################################

# I. initialize dlib's face detector (HOG-based)
detector = dlib.get_frontal_face_detector()
#initialize facial landmark 
print("[INFO] loading facial landmark predictor...")
predictor = dlib.shape_predictor(args["shape_predictor"]) 


# II. grab the indexes of the facial landmarks for the left and right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


# II. Determine the type of input + start the video stream thread
print("[INFO] starting video stream thread...")

# if --video: input is a video file from disk
if len(args["video"]) != 0: #not none 
  vs = FileVideoStream(args["video"]).start()
  fileStream = True
# else, it's from a webcam
else: 
  src = args["webcam"] #default is -
  vs = VideoStream(src=src).start()
  fileStream = False
time.sleep(1.0)


# IV. Determine if alarm sound is required
if args["alarm"]:
  print("Alarm option is activated")
  sound_alarm_player = sound_alarm(sound_alarm_path) #initalize sound_alarm object

# V. loop over the frames from the video stream
###################################
#  ***** START DETECTING ***** 
###################################

while True:

  # 1. grab the frame
  frame = vs.read()
  
  # xx CHECK check if there are frames in fileStream left in the buffer to process
  if (fileStream and frame is None):
    print("Detection Finished.")
    break;
  
    
  # xx CHECK if the video resolution is above 480p # TASK REQUIREMENT
  if (frame.shape[0] < 480 and frame.shape[1] < 640):
    print("This program supports 480p video resolution and above using the standard 4:3 (i.e. 480x640p)")
    break;


  # 2. get the faces rectangles (coordinates) in the frame
  # resize frame ang convert to gray scale   
  frame = imutils.resize(frame, width=450)
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  
  # detect faces rectangles with dlib
  rects = detector(gray, 0)

  # xx CHECK if only one face was detected in per frame # TASK REQUIREMENT
  number_of_faces = len(rects)

  if number_of_faces == 1:
  
    rect = rects[0]

    # convert dlib's rectangle to OpenCV bounding box 
    (x, y, w, h) = face_utils.rect_to_bb(rect)

    # 3- get the facial landmarks of the face 
    shape = predictor(gray, rect) #
    shape = face_utils.shape_to_np(shape) # convert to NumPy array 
   
    
    # xx CHECK if the face takes 1/3 of the frame # TASK REQUIREMENT
    if (h >= 1/3 * frame.shape[0]):
        
        # draw the face bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 4- extract the left and right eye coordinates#
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # 5- get the average EAR over both eyes
        ear = (leftEAR + rightEAR) / 2.0 #averaged following the suggestion of Soukupová and Čech (2016) paper

        # visualize the eyes in green
        leftEyeHull = cv2.convexHull(leftEye)   #compute the convex hull 
        rightEyeHull = cv2.convexHull(rightEye) #compute the convex hull
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        
        # 6- xx CHECK if EAR is below the threshold and increment FRAME COUNTER
        if ear < EYE_AR_THRESH:
            
            
            FRAME_COUNTER += 1 
            #print(f"{FRAME_COUNTER}: eye closed ._. EAR={ear}") #debug

            if FRAME_COUNTER == 1:
                # get epoch time at the first frame where the eye started closing
                closed_eyes_timer_start = time.time()  
        
            # get epoch time in seconds  
            closed_eyes_timer_next = time.time()  

            # get elapsed time since eye started closing 
            closed_eyes_elapsed_time = closed_eyes_timer_next - closed_eyes_timer_start
	    
            # xx CHECK if eyes are closed above the threshold

            if closed_eyes_elapsed_time > TIME_ALARM_THRESH: 

                # a. write "Alert!" in red #TASK REQUIREMENT
                cv2.putText(frame, "Alert!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # b. play alarm sound
                if (sound_alarm_player is not None):
                    
                    # xx CHECK if the alarm is not on 
                    if not ALARM_already_on:

                       # define a stopping event
                       stop_event = threading.Event()

                       # turn on the alarm
                       ALARM_already_on = True 

                       t = threading.Thread(target=sound_alarm_player.play, args=(stop_event,))
                       t.deamon = True
                       t.start()
         
        else: 
            ''' 7- xx if the eye is opened again, check if the number of frames exceed the threshold of a blink'''  
            if FRAME_COUNTER >= EYE_AR_CONSEC_FRAMES:
                BLINK_COUNTER += 1 
     
                #print("eye opend again @.@") #DEBUG
                #print("YOU BLINKED!") #DEBUG
                
                # stop the alarm sound
                if (sound_alarm_player is not None) and ALARM_already_on:

                  # stop event
                  stop_event.set()
                  # turn off the alarm
                  ALARM_already_on = False
                            
            # reset when eyes are open                
            FRAME_COUNTER = 0
            closed_eyes_elapsed_time = 0
   
        # draw the total number of blinks on the frame
        cv2.putText(frame, "Blinks: {}".format(BLINK_COUNTER), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) 
        #cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) # draw EAR at the current frame
        
        
  # show the frame
  cv2.imshow("Resized Frame",  np.array(frame, dtype = np.uint8 ))
  key = cv2.waitKey(1) & 0xFF
 
  # if the `q` key was pressed, break from the loop
  if key == ord("q"):
    break;   
    
cv2.destroyAllWindows()
vs.stop()
