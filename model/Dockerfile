FROM python:3.11
ADD server.py model.py requirements.txt .
RUN pip install flask Flask-Cors numpy pillow requests ultralytics
# RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "./server.py"] 
