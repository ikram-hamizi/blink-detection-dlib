# Eye Blink Detection

## PROGRAM:
Detects the number of blinks of a person in real time. 
- **INPUT:** video from a file path / video from a webcam.
- **OUTPUT:** Window with the video + the number of blinks

## PROPERTIES:
1. Only one person should be in the video (+)
2. The face of the person should cover at least 1/3 of the frame (pixels) (+)
3. Minimum resolution should be 480p using the (4:3) Standard (i.e. 480x640p) (+)

4. Increments the number of blinks [upper-left corner]
5. If the eyes are closed for more than 2 seconds, a message "Alert!" appears in red (+ --alarm sound option)
6. Draws the facial landmarks (eyes + bounding box of the face (+))

## SOURCE: 
The program is written following the guide by Adrian Rosebrock from PyImageSearch: [LINK](https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)
- Detect blinks with the calculation of the Eye Aspect Ratio (EAR)
- Detect the facial landmarks: dlib library
- Drawing of landmarks: cv2 and with the help of imutils libraries

## USAGE: 
#### METHOD (1):
From a Linux terminal, run:
```bash 
docker run --rm -it --entrypoint=/bin/bash --privileged -e DISPLAY=$IP:0 --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix ikramhub/blink-counter
```
The run the program:
- **Example (1):**
```bash
python blink-counter.py -p shape_predictor_68_face_landmarks.dat -a True --video blink_detection_demo.mp4 --EAR 0.3
```

- **Example (2):**
```bash
python blink-counter.py -p shape_predictor_68_face_landmarks.dat -a True --webcam 0 --EAR 0.25
```

#### METHOD (2):
Clone the repository and run the commands in option (1) withouth `ikramhub/` before `blink-counter`.

#### CMD [OPTIONS]:

Usage:	python blink-counter.py -p [shape_predictor.dat] [OPTIONS]
___________________________________________________________________________________________________________
`-p` or `--shape-predictor [file.dat]`:	(required) dlib pre-trained facial landmark detector

`-a [True/False]:`	activates alarm option

`-v or --video [file.mp4]:`	video file path

`-w or --webcam [integer]:`	an integer index of the webcam on the system

`--EAR:`	EAR threshold to count a blink (default=0.25)

(From: _print_usage.sh_)
