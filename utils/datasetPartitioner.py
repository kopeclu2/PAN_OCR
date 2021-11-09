import os
import shutil
from sklearn.model_selection import train_test_split

required_directories = ['images/train/', 'images/val/', 'images/test/', 'annotations/train/', 'annotations/val/', 'annotations/test/']

class DatasetPartitioner:
    
    train_test_size = 0.7
    val_test_size = 0.2

    def __init__(self, train_size = 0.7, validation_size = 0.2):
        self.make_required_dirs()
        self.train_test_size = train_size
        self.val_test_size = validation_size
        
    def make_required_dirs(self):
        print("Cheching for required directories...")
        for directory in required_directories:
            if not os.path.exists(directory):
                print("--> Creating directory :", directory)
                os.makedirs(directory)

    #Utility function to move images 
    def move_files_to_folder(list_of_files, destination_folder):
        for f in list_of_files:
            try:
                shutil.move(f, destination_folder)
            except:
                print(f)
                assert False

    def partition_dataset_to_test_and_train_packages(self):
        images = [os.path.join('dataset', x) for x in os.listdir('dataset') if x[-3:] == "jpg"]
        annotations = [os.path.join('dataset', x) for x in os.listdir('dataset') if x[-3:] == "txt"]

        images.sort()
        annotations.sort()
        # Split the dataset into train-valid-test splits 
        train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size = 0.5, random_state = 1)
        val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size = 0.2, random_state = 1)

        move_files_to_folder(train_images, 'images/train')
        move_files_to_folder(val_images, 'images/val/')
        move_files_to_folder(test_images, 'images/test/')
        move_files_to_folder(train_annotations, 'annotations/train/')
        move_files_to_folder(val_annotations, 'annotations/val/')
        move_files_to_folder(test_annotations, 'annotations/test/')