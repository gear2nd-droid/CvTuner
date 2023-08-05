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
    prm['gamma'] = '3.0'
    prm['scurve'] = '0.05'
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
    
    # gamma
    gamma = float(prm['gamma'])
    lut_gamma = np.zeros([256,1], dtype=np.uint8)
    for i in range(256):
        lut_gamma[i][0] = 255 * (float(i) / 255) ** (1.0 / gamma)
    img_gamma = cv2.LUT(img_bgr, lut_gamma)
    image_dic['img_gamma'] = img_gamma
    
    # s_curve
    scurve = float(prm['scurve'])
    lut_scurve = np.zeros([256,1], dtype=np.uint8)
    for i in range(256):
        lut_scurve[i][0] = 255 / (1 + math.exp(scurve * (-1 * i + 127)))
    img_scurve = cv2.LUT(img_bgr, lut_scurve)
    image_dic['img_scurve'] = img_scurve   

    # reverse
    lut_reverse = np.zeros([256,1], dtype=np.uint8)
    for i in range(256):
        lut_reverse[i][0] = 255 - i
    img_reverse = cv2.LUT(img_bgr, lut_reverse)
    image_dic['img_reverse'] = img_reverse
    
    # return
    # Return image_dic and result.
    # The image is automatically loaded.
    return(image_dic, result)
    