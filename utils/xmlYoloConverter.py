import xml.etree.ElementTree as ET
import os
from tqdm import tqdm

class_name_to_id_mapping = {"IS21": 0,
                           "text": 1,
                        }

class XmlYoloConverter():

    def extract_info_from_xml(self, xml_filename):
        root = ET.parse(xml_filename).getroot()

        info_dict = {}
        info_dict['bboxes'] = []

        #Parder VOC_ANOTATTION xml tree

        for element in root:
            #Parse filename
            if element.tag == 'filename':
                info_dict['filename'] = element.text
            
            #Get image <size> 
            elif element.tag == 'size':
                image_size = []
                for subelement in element:
                    image_size.append(int(subelement.text))

                info_dict['image_size'] = tuple(image_size)
            
            #Boudning box <object>
            elif element.tag == 'object':
                bbox = {}
                for subelement in element:
                    if subelement.tag == 'name':
                        bbox["class"] = subelement.text
                    
                    elif subelement.tag == "bndbox":
                        for subsubelement in subelement:
                            bbox[subsubelement.tag] = int(subsubelement.text)
                info_dict['bboxes'].append(bbox)

        return info_dict

    def convert_to_yolov5(self, info_dict):
        print_buffer = []
        # For each bounding box
        for b in info_dict["bboxes"]:
            try:
                class_id = class_name_to_id_mapping[b["class"]]
            except KeyError:
                print("Invalid Class. Must be one from ", class_name_to_id_mapping.keys())
            
            # Transform the bbox co-ordinates as per the format required by YOLO v5
            b_center_x = (b["xmin"] + b["xmax"]) / 2 
            b_center_y = (b["ymin"] + b["ymax"]) / 2
            b_width    = (b["xmax"] - b["xmin"])
            b_height   = (b["ymax"] - b["ymin"])
            
            # Normalise the co-ordinates by the dimensions of the image
            image_w, image_h, image_c = info_dict["image_size"]  
            b_center_x /= image_w 
            b_center_y /= image_h 
            b_width    /= image_w 
            b_height   /= image_h 
            
            #Write the bbox details to the file 
            print_buffer.append("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))
            
        # Name of the file which we have to save 
        save_file_name = os.path.join("dataset", info_dict["filename"].replace("jpg", "txt"))
        print('Try to save new .txt with name: '+ save_file_name)
        # Save the annotation to disk
        print("\n".join(print_buffer), file= open(save_file_name, "w"))

    def convert_all_xml_in_directory_to_yolo5(self, directory):
        # Get the annotations
        annotations = [os.path.join(directory, x) for x in os.listdir(directory) if x[-3:] == "xml"]
        annotations.sort()

        # Convert and save the annotations
        for ann in tqdm(annotations):
            info_dict = self.extract_info_from_xml(ann)
            self.convert_to_yolov5(info_dict)
        annotations = [os.path.join(directory, x) for x in os.listdir(directory) if x[-3:] == "txt"]
