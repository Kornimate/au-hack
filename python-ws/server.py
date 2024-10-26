from flask import Flask,render_template,request, Response, jsonify
from flask_cors import CORS
from model import Model
import json
import requests
import base64
import socket

app = Flask(__name__)
cors = CORS(app, )
# model = Model()

ws_endpoint = ''


@app.route('/home')
def main():
        return Response(json.dumps({"hello": "world"}), status=200, mimetype="application/json")

@app.route("/stream-data", methods=["POST"])
def eval_picture():
    if request.method != 'POST':
        app.logger.warning('invalid request')
        return
    data = request.get_json()
    
    print(f"got value from: {data.get("id", "no id recieved")}")
    # predictions = model.PredictFromImgArray(base64.base64decode(img_and_num_arr[0]))
    # resp = requests.post(ws_endpoint, json=predictions)

    # if resp.status_code >= 400:
    #       print(f"error while sending data: {resp}")
    return Response(json.dumps({"response": "ok"}), status=200, mimetype="application/json")

if __name__ == '__main__':
      app.run(host=socket.gethostbyname(socket.gethostname()),port=5000)