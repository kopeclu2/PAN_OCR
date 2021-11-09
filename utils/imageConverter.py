import cv2
import os
import uuid
from random import randrange
import os
from tqdm import tqdm

folder = 'dataset'
class ImageConverter:
    
    def save_img(self, image, name):
        print("Saving image: ", name)
        path = os.path.join(folder, name+".jpg")
        cv2.imwrite(path, image)
        return

    def load_images_from_folder(self):
        images = []
        for filename in os.listdir(folder):
            if filename.endswith(".png"): 
                old_img_filename = os.path.join(folder,filename)
                new_filename = ImageConverter.my_random_string(10)
                old_xml_filename = os.path.join(folder, filename.replace("png", "xml"))
                assert os.path.exists(old_xml_filename)
                new_xml_filename = os.path.join(folder,new_filename) + '.xml'
                assert os.path.exists(old_img_filename)
                new_img_filename = os.path.join(folder,new_filename) + '.jpg'
                os.rename(old_xml_filename, new_xml_filename)
                os.rename(old_img_filename,new_img_filename)
        return images

    @staticmethod
    def my_random_string(string_length=10):
        """Returns a random string of length string_length."""
        random = str(uuid.uuid4()) # Convert UUID format to a Python string.
        random = random.upper() # Make all characters uppercase.
        random = random.replace("-","") # Remove the UUID '-'.
        return random[0:string_length] # Return the random string.

    
        
