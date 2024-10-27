FROM python:3.11
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
RUN pip install flask Flask-Cors numpy pillow requests ultralytics
ADD server.py model.py requirements.txt .
RUN pip install tensorflow
# RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "./server.py"] 
