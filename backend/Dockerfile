FROM python:3.13-alpine
ADD main.py requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "./main.py"]
