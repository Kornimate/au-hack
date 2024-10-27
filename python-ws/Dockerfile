FROM python:3.13-alpine
ADD server.py model.py requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "./server.py"] 
