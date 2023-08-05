import cv2
import numpy as np
import math
import copy

# console
# You can output a message to the console with "console.append(message)".

def init_parameter(console):
    prm = {}
    # Parameters can be set in Dictionary.
    # The set parameters are read into the parameter list.
    # The key and value of the parameter are both strings.
    prm['circle_dp'] = '1'
    prm['circle_min_dist'] = '20'
    prm['circle_param1'] = '100'
    prm['circle_param2'] = '60'
    prm['circle_min_radius'] = '0'
    prm['circle_max_radius'] = '0'
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
    
    # grayscale
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    image_dic['img_gray'] = img_gray
    
    # hough circles
    circle_dp = float(prm['circle_dp'])
    circle_min_dist = float(prm['circle_min_dist'])
    circle_param1 = float(prm['circle_param1'])
    circle_param2 = float(prm['circle_param2'])
    circle_min_radius = int(prm['circle_min_radius'])
    circle_max_radius = int(prm['circle_max_radius'])
    img_circle = copy.deepcopy(img_bgr)
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, dp=circle_dp, minDist=circle_min_dist, \
        param1=circle_param1, param2=circle_param2, minRadius=circle_min_radius, maxRadius=circle_max_radius)
    #circles = np.uint16(np.around(circles))
    for circle in circles[0, :]:
        cv2.circle(img_circle, (circle[0], circle[1]), circle[2], (0, 165, 255), 5)
        cv2.circle(img_circle, (circle[0], circle[1]), 2, (0, 0, 255), 3)
    image_dic['img_circle'] = img_circle
    result['circle_count'] = str(len(circles[0, :]))
    
    # return
    # Return image_dic and result.
    # The image is automatically loaded.
    return(image_dic, result)
    