# Eye Blink Detection

## PROGRAM:
Detects the number of blinks of a person in real time and sleeping.
- **INPUT:** video from a file path / video from a webcam.
- **OUTPUT:** Window with the video + the number of blinks

## PROPERTIES:
1. Only one person should be in the video (+)
2. The face of the person should cover at least 1/3 of the frame (pixels) (+)
3. Minimum resolution should be 480p using the (4:3) Standard (i.e. 480x640p) (+)

4. Increments the number of blinks [upper-left corner]
5. If the eyes are closed for more than 2 seconds, a message "Alert!" appears in red (+ `--alarm` sound option)
6. Draws the facial landmarks (eyes + bounding box of the face (+))

## SOURCE: 
The program is written following the guide by Adrian Rosebrock from PyImageSearch: [LINK](https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)
- Detect blinks with the calculation of the Eye Aspect Ratio (EAR)
- Detect the facial landmarks: dlib’s pre-trained facial landmark detector 
- Drawing of landmarks: cv2 and with the help of imutils libraries

## USAGE: 
#### METHOD (1):
To run the program from a docker image a Linux terminal, run this (solution to access the webcam from [LINK: '**Test camera with**'](https://stackoverflow.com/a/64634921/8664083)):
```bash 
docker run --rm -it --entrypoint=/bin/bash --privileged -e DISPLAY=$IP:0 --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix ikramhub/blink-counter
```
The run the program:
- **Example (1):** using a video file
```bash
python blink-counter.py -p shape_predictor_68_face_landmarks.dat -a True --video blink_detection_demo.mp4 --EAR 0.3
```

- **Example (2):** using the built-in webcam
```bash
python blink-counter.py -p shape_predictor_68_face_landmarks.dat -a True --webcam 0 --EAR 0.25
```

#### METHOD (2):
Clone the repository and run the same commands in METHOD (1) without `ikramhub/` before the image tag `blink-counter`.

#### METHOD (3):
Download the following main files and run the commands in Exampe (1) or (2). You may have to donwload libraries and dependencies (see file: _run.sh_)

```bash
├── Loud_Alarm_Clock_Buzzer.wav            <- alarm file
├── blink-counter.py                       <- blink detection script
└── shape_predictor_68_face_landmarks.dat  <- pretrained facial landmarks detectors
```

#### CMD [OPTIONS]:

Usage:	`python blink-counter.py -p [shape_predictor.dat] [OPTIONS]`
___________________________________________________________________________________________________________
`-p` or `--shape-predictor [file.dat]`:	(required) dlib pre-trained facial landmark detector

`-a [True/False]:`	activates alarm option

`-v or --video [file.mp4]:`	video file path

`-w or --webcam [integer]:`	an integer index of the webcam on the system

`--EAR:`	EAR threshold to count a blink (default=0.25)

(see file: _print_usage.sh_)
