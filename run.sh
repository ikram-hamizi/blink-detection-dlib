#!/bin/bash

echo "1- Downloading OpenCV + Dependencies..." &&\
	apt-get update &&\
	#pip3 install --upgrade pip &&\
	pip3 install opencv-python &&\
	apt-get install -y \
	build-essential cmake pkg-config \
	libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
	libxvidcore-dev libx264-dev \
	libgtk-3-dev\
	libatlas-base-dev gfortran \
	libsm6 libxrender-dev \
	libsdl1.2-dev libsdl-image1.2 libsdl-mixer1.2 libsdl-ttf2.0 \
	python3\
	python3-dev &&\
	echo "" &&\
	echo "************ Python Version **************" &&\
	python -V &&\
	echo &&\
	echo "2- Downloading other blink-counter requirements.txt..." &&\
	echo "export QT_DEBUG_PLUGINS=1"  >> ~/.bashrc  && \ 
	echo "export QT_PLUGIN_PATH=usr/local/lib/python3.8/site-packages/cv2/qt/plugins"  >> ~/.bashrc  && \ 
	pip3 install numpy scipy pygame dlib imutils 
	
	

