import cv2
import numpy as np
import math

# console
# You can output a message to the console with "console.append(message)".

def init_parameter(console):
    prm = {}
    # Parameters can be set in Dictionary.
    # The set parameters are read into the parameter list.
    # The key and value of the parameter are both strings.
    return prm

def image_process(image_dic, prm, filename, console):
        
    # result
    # Store the result in Dictionary.
    # The result is read into the result list.
    # The key and value of the result are both strings.
    result = {}
    console.append(filename)
    
    # image dictionary
    # The loaded image is stored in image_dic['original'].
    # The key of image_dic is specified by a string, and this value is automatically registered in Combobox.
    # The value of image_dic is the image, which is the one in the selected Combobox.
    
    # return
    # Return image_dic and result.
    # The image is automatically loaded.
    return(image_dic, result)
    