from flask import Flask,render_template,request, Response, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from model import Model
import json
import requests
import base64

app = Flask(__name__)
cors = CORS(app)
socketio = SocketIO(app,debug=True,cors_allowed_origins='*')
model = Model()

ws_endpoint = ''


@app.route('/home')
def main():
        return Response(json.dumps({"hello": "world"}), status=200, mimetype="application/json")

@socketio.on("stream-data")
def eval_picture(base64img_and_num):
    img_and_num_arr = base64img_and_num.split('&&')
    # predictions = model.PredictFromImgArray(base64.base64decode(img_and_num_arr[0]))
    # resp = requests.post(ws_endpoint, json=predictions)

    # if resp.status_code >= 400:
    #       print(f"error while sending data: {resp}")

if __name__ == '__main__':
      app.run(port=5000)