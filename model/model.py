from ultralytics import YOLO
from PIL import Image
from io import BytesIO
import tensorflow as tf
import base64
import numpy as np


class Model():
    def __init__(self):
        self.model = YOLO("yolo11l.pt")
    
    def Predict(self,image):
        return self.model.predict(image, classes=[0,62])
        

def CreateDataBundle(data, id):
    classes = data.boxes.cls.tolist()  # Bounding box coordinates (x1, y1, x2, y2)
    boxes = data.boxes.xyxy.tolist()
    
    return {
        "cam_id":id,
        "locations": boxes,
        "types":list(map(lambda x : int(x), classes))
    }
    
def ConvertB64ToNpArray(b64image):
    decoded_img = base64.b64decode(b64image)
    pil_image = Image.open(BytesIO(decoded_img)).convert("RGB") 
    return np.array(pil_image)