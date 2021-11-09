

import albumentations as A
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import uuid
from random import randrange

# Declare an augmentation pipeline


class ImageLoader:
    @staticmethod
    def load_images_from_folder(folder):
        print('Start loading dataset from folder ' + folder)
        images = []
        for filename in os.listdir(folder):
            print("Scanning :" + filename)
            img = cv2.imread(os.path.join(folder,filename))
            if img is not None:
                print("Appending file:" + filename)
                cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                images.append(img)
        print("Loading images has been completed...")
        return images
    
    @staticmethod
    def my_random_string(string_length=10):
        """Returns a random string of length string_length."""
        random = str(uuid.uuid4()) # Convert UUID format to a Python string.
        random = random.upper() # Make all characters uppercase.
        random = random.replace("-","") # Remove the UUID '-'.
        return random[0:string_length] # Return the random string.

    @staticmethod
    def save_image(image):
        path = os.path.join('dataset_agumentioned',ImageLoader.my_random_string(10)+".jpg")
        cv2.imwrite(path, image)
        return

    def do_image_augmention(self, images):
        print("Start doing augmention")
        clach = A.Compose([
                A.CLAHE(),
                A.RandomBrightnessContrast(p=0.2)
        ])
        blur = A.Compose([
            A.CLAHE(),
            A.Blur(p=0.4),
            A.RandomBrightnessContrast(p=0.3)
        ])
        rotate = A.Compose([
            A.CLAHE(),
            A.ElasticTransform(sigma=randrange(100), alpha_affine=randrange(100)),
            A.RandomBrightnessContrast(p=0.2)
        ])
        for i in images:
            print("Aug for image.")
            clached = clach(image=i)
            blured = blur(image=i)
            totated = rotate(image=i)
            transformed_image = clached["image"]
            blured_image = blured["image"]
            totated_image = totated["image"]
            ImageLoader.save_image(transformed_image)
            ImageLoader.save_image(blured_image)
            ImageLoader.save_image(totated_image)
        return


image_loader = ImageLoader()
images_dataset = image_loader.load_images_from_folder('dataset')
image_loader.do_image_augmention(images_dataset)
