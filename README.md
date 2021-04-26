# Eye Blink Detection

## PROGRAM:
Detects the number of blinks of a person in real time and sleeping.
- **INPUT:** `p` a pretrained facial landmarks detectors 
- **Optional Input**: `--video` path of a video file. The default is: a video stream from a webcam.
- **OUTPUT:** A window with the video + the number of blinks

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
##### 1. Build the program locally or Pull it from Docker Hub:
#### METHOD (1): Pull from Docker Hub
On a linux terminal, run this command to run a container:
```bash 
docker run -d --rm --privileged -e DISPLAY=:0 --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix ikramhub/blink-counter  tail -f /dev/null
```
(solution to access the webcam from [LINK: '**Test camera with**'](https://stackoverflow.com/a/64634921/8664083))


#### METHOD (2): Build an image locally from Dockerfile
Clone the repository + run this to build an image:
```bash 
docker build -t blink-counter .
```
```bash 
docker run -d --rm --privileged -e DISPLAY=:0 --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix blink-counter  tail -f /dev/null
```

#### METHOD (3): No building/pulling required
Download the following main files + run the program directly (without pulling or building).

**NOTE**: You may need to donwload dependencies (see file: _run.sh_)

```bash
├── Loud_Alarm_Clock_Buzzer.wav            <- alarm file
├── blink-counter.py                       <- blink detection script
└── shape_predictor_68_face_landmarks.dat  <- pretrained facial landmarks detectors
```


##### 2. Run the program
- **Example (1):** using a video file
You can use a video file that is already in the container (source: [LINK](https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)) 
```bash
docker ps #copy the container ID from IMAGE: ikramhub/blink-counter
docker exec -it <CONTAINER_ID> /bin/bash
python blink-counter.py -p shape_predictor_68_face_landmarks.dat -a True --video blink_detection_demo.mp4 --EAR 0.3
```

Alternatively, you can load your own file before running the previous command:
```bash
docker cp /home/path/hostfile.mp4  <CONTAINER_ID>:/app #copy the file from host to container
```

- **Example (2):** using the built-in webcam
```bash
docker ps #copy the container ID from IMAGE: ikramhub/blink-counter
docker exec -it <CONTAINER_ID> /bin/bash
python blink-counter.py -p shape_predictor_68_face_landmarks.dat -a True --webcam 0 --EAR 0.25
```

3. Quit by hitting the key: "q". To exit the container type `exit`.

#### CMD [OPTIONS]:

Usage:	`python blink-counter.py -p [shape_predictor.dat] [OPTIONS]`
___________________________________________________________________________________________________________
`-p` or `--shape-predictor [file.dat]`:	(required) dlib pre-trained facial landmark detector

`-a [True/False]:`	activates alarm option

`-v or --video [file.mp4]:`	video file path

`-w or --webcam [integer]:`	an integer index of the webcam on the system

`--EAR:`	EAR threshold to count a blink (default=0.25)

(see file: _print_usage.sh_)
