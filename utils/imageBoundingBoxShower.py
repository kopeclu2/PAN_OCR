import numpy as np
from utils.xmlYoloConverter import class_name_to_id_mapping
from PIL import Image, ImageDraw
import os
import random
import matplotlib.pyplot as plt

random.seed(0)

class_id_to_name_mapping = dict(zip(class_name_to_id_mapping.values(), class_name_to_id_mapping.keys()))

class ImageBoundingBoxShower:

    def plot_bounding_box(self, image, annotation_list):
        annotations = np.array(annotation_list)
        w, h = image.size
        
        plotted_image = ImageDraw.Draw(image)

        transformed_annotations = np.copy(annotations)
        transformed_annotations[:,[1,3]] = annotations[:,[1,3]] * w
        transformed_annotations[:,[2,4]] = annotations[:,[2,4]] * h 
        
        transformed_annotations[:,1] = transformed_annotations[:,1] - (transformed_annotations[:,3] / 2)
        transformed_annotations[:,2] = transformed_annotations[:,2] - (transformed_annotations[:,4] / 2)
        transformed_annotations[:,3] = transformed_annotations[:,1] + transformed_annotations[:,3]
        transformed_annotations[:,4] = transformed_annotations[:,2] + transformed_annotations[:,4]
        
        for ann in transformed_annotations:
            obj_cls, x0, y0, x1, y1 = ann
            plotted_image.rectangle(((x0,y0), (x1,y1)))
            
            plotted_image.text((x0, y0 - 10), class_id_to_name_mapping[(int(obj_cls))])
        
        plt.imshow(np.array(image))
        plt.show()

    def draw_bounding_box_by_yolo_annotation(self):
        annotations = [os.path.join('dataset', x) for x in os.listdir('dataset') if x[-3:] == "txt"]
        annotations.sort()
        annotation_file = random.choice(annotations)
        with open(annotation_file, "r") as file:
            annotation_list = file.read().split("\n")[:-1]
            annotation_list = [x.split(" ") for x in annotation_list]
            annotation_list = [[float(y) for y in x ] for x in annotation_list]

        #Get the corresponding image file
        image_file = annotation_file.replace("txt", "jpg")
        assert os.path.exists(image_file)

        #Load the image
        image = Image.open(image_file)

        #Plot the Bounding Box
        self.plot_bounding_box(image, annotation_list)