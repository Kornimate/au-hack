import os
from pycocotools.coco import COCO
import tensorflow as tf
import numpy as np
import keras_cv
from tensorflow import keras

class Model():
    def __init__(self,annotation_path, imagedir, path_to_weigths):
        self.annotation_path = annotation_path
        self.image_dir = imagedir
        
        self.coco = COCO(self.annotation_path)

        self.target_classes = [1, 62]  # person and tv/monitor classes
        self.cat_ids = self.coco.getCatIds(catNms=['person', 'tv'])

        # Get all images containing the target classes
        self.img_ids = self.coco.getImgIds(catIds=self.cat_ids)
        self.images = self.coco.loadImgs(self.img_ids)

        self.model = None
        
        if self.TryLoadModelState(path_to_weigths=path_to_weigths):
            return
        
        self.CreateModel()
        self.LoadImageAndBoxes()

        self.test_set=self.CreateDataSet(self.img_ids)
        self.TrainModel()


    def CreateModel(self):
        self.model = keras_cv.models.RetinaNet(
            classes=len(self.target_classes),
            backbone="resnet50",
            bounding_box_format="xywh",
        )

        self.model.compile(
            classification_loss="focal", 
            box_loss="smoothl1", 
            optimizer="adam",
        )

    def TryLoadModelState(self, path_to_weigths):
        if os.path.isfile(path=path_to_weigths):
            self.model.load_weights(filepath=path_to_weigths)
            return True
        else:
            return False
        
    def LoadImageAndBoxes(self,img_id):
        # Load image
        img_info = self.coco.loadImgs(img_id)[0]
        img_path = os.path.join(self.image_dir, img_info['file_name'])
        image = tf.image.decode_jpeg(tf.io.read_file(img_path))
        image = tf.image.resize(image, (640, 640))  # Resize for RetinaNet input

        # Load annotations
        ann_ids = self.coco.getAnnIds(imgIds=img_id, catIds=self.cat_ids, iscrowd=False)
        annotations = self.coco.loadAnns(ann_ids)

        boxes = []
        labels = []
        for ann in annotations:
            bbox = ann['bbox']
            category_id = ann['category_id']
            label = self.target_classes.index(category_id) + 1  # Offset for background class

            boxes.append(bbox)
            labels.append(label)
        
        boxes = np.array(boxes, dtype=np.float32)
        labels = np.array(labels, dtype=np.int32)
        
        return image, {"boxes": boxes, "classes": labels}

    def CocoGenerator(self,img_ids):
        for img_id in img_ids:
            yield self.LoadImageAndBoxes(img_id)

    def CreateDataSet(self, img_ids):
        dataset = tf.data.Dataset.from_generator(  # Create TensorFlow dataset
            lambda: self.CocoGenerator(img_ids),
            output_signature=(
                tf.TensorSpec(shape=(640, 640, 3), dtype=tf.float32),
                {
                    "boxes": tf.TensorSpec(shape=(None, 4), dtype=tf.float32),
                    "classes": tf.TensorSpec(shape=(None,), dtype=tf.int32),
                },
            ),
        )
        dataset = self.dataset.batch(4).prefetch(2)
        return dataset
    
    def TrainModel(self):
        self.model.fit(self.dataset, epochs=10)
        # retinanet.evaluate(val_dataset)

    def PredictFromFile(self,image_path):
        image = tf.image.decode_jpeg(tf.io.read_file(image_path))
        image = tf.image.resize(image, (640, 640))
        image = tf.expand_dims(image, axis=0)

        predictions = self.model.predict(image)
        return predictions

    def PredictFromImgArray(self,image_array):
        image = tf.image.decode_image(image_array, channels=3)
        image = tf.image.resize(image, (640, 640))
        image = tf.expand_dims(image, axis=0)

        predictions = self.model.predict(image)
        return predictions
    
    def SaveModelState(self, path_to_weigths):
        self.model.save_weights(filepath=path_to_weigths)