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
    img_bgr = image_dic['original']
    img_bgr_split = cv2.split(img_bgr)
    image_dic['b'] = img_bgr_split[0]
    image_dic['g'] = img_bgr_split[1]
    image_dic['r'] = img_bgr_split[2]
    # hsv
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    image_dic['img_hsv'] = img_hsv
    # hsv split
    img_hsv_split = cv2.split(img_hsv)
    image_dic['h'] = img_hsv_split[0]
    image_dic['s'] = img_hsv_split[1]
    image_dic['v'] = img_hsv_split[2]
    
    # return
    # Return image_dic and result.
    # The image is automatically loaded.
    return(image_dic, result)
    