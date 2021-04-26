FROM python:3.8-slim AS builder

MAINTAINER Ikram Hamizi <hamizi.ikram@gmail.com>

WORKDIR /app

COPY . ./
	

RUN chmod +x ./run.sh
RUN ./run.sh

#runs setup.py (installs itself)
RUN pip install .

RUN chmod +x ./print_usage.sh
CMD ["sh", "./print_usage.sh"]


#CMD ["python"] ["blink-counter.py"] ["-p"] ["shape_predictor_68_face_landmarks.dat"] ["-a"] ["True"] ["--video"] ["blink_detection_demo.mp4"] ["--EAR"] ["0.3"] ["--webcam"] ["0"]

