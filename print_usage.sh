printf "
___________________________________________________________________________________________________________
Usage:	python blink-counter.py -p [shape_predictor.dat] [OPTIONS]
___________________________________________________________________________________________________________
-p or --shape-predictor [file.dat]:	(required) dlib pre-trained facial landmark detector

-a [True/False]:	activates alarm option

-v or --video [file.mp4]:	video file path

-w or --webcam [integer]:	an integer index of the webcam on the system

--EAR:	EAR threshold to count a blink (default=0.25)
___________________________________________________________________________________________________________
Example (1): python blink-counter.py -p shape_predictor_68_face_landmarks.dat -a True --video blink_detection_demo.mp4 --EAR 0.3

Example (2): python blink-counter.py -p shape_predictor_68_face_landmarks.dat -a True --webcam 0 --EAR 0.25
___________________________________________________________________________________________________________
NOTE: If the container cannot access the webcam, run this first:

docker run --rm -it --entrypoint=/bin/bash --privileged -e DISPLAY=$IP:0 --device=/dev/video0:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix blink-counter

"
