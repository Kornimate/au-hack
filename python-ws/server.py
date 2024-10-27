from flask import Flask,render_template,request, Response, jsonify
from flask_cors import CORS
from model import Model, CreateDataBundle, ConvertB64ToNpArray
import json
import requests
import socket

app = Flask(__name__)
cors = CORS(app)
model = Model()

ws_endpoint = 'http://localhost:8080/update'

@app.route('/home')
def main():
        return Response(json.dumps({"hello": "world"}), status=200, mimetype="application/json")

@app.route("/stream-data", methods=["POST"])
def eval_picture():
    if request.method != 'POST':
        app.logger.warning('invalid request')
        return
    
    jsonData = request.get_json()
    
    print("Value arrived")
    
    converted_img = ConvertB64ToNpArray(jsonData.get("data"))
    
    results = model.Predict(converted_img)
    
    predictions = results[0]  # Get predictions for the first image

    # Extracting information
    jsonObj = CreateDataBundle(predictions,jsonData.get("id", "no id recieved"))
    print(jsonObj)
    
    resp = requests.post(ws_endpoint, json=jsonObj)

    if resp.status_code >= 400:
          print(f"error while sending data: {resp}")
          
    return Response(json.dumps({"response": "ok"}), status=200, mimetype="application/json")

if __name__ == '__main__':
      app.run(host='0.0.0.0',port=5000)