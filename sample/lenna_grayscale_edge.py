import cv2
import numpy as np
import math

def init_parameter():
    prm = {}
    # Parameters can be set in Dictionary.
    # The set parameters are read into the parameter list.
    # The key and value of the parameter are both strings.
    prm['canny_th1'] = '0'
    prm['canny_th2'] = '360'
    return prm

def image_process(image_dic, prm, filename):
        
    # result
    # Store the result in Dictionary.
    # The result is read into the result list.
    # The key and value of the result are both strings.
    result = {}
    
    print(filename)
    
    # image dictionary
    # The loaded image is stored in image_dic['original'].
    # The key of image_dic is specified by a string, and this value is automatically registered in Combobox.
    # The value of image_dic is the image, which is the one in the selected Combobox.
    img_bgr = image_dic['original']
    
    # grayscale
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    image_dic['img_gray'] = img_gray
    
    # canny
    canny_th1 = int(prm['canny_th1'])
    canny_th2 = int(prm['canny_th2'])
    img_canny = cv2.Canny(img_gray, canny_th1, canny_th2)
    image_dic['img_canny'] = img_canny
    
    # sobel_x
    img_sobel_x = cv2.Sobel(img_gray, cv2.CV_32F, 1, 0, ksize=3)
    img_sobel_x = cv2.convertScaleAbs(img_sobel_x)
    image_dic['img_sobel_x'] = img_sobel_x
    
    # sobel_y
    img_sobel_y = cv2.Sobel(img_gray, cv2.CV_32F, 0, 1, ksize=3)
    img_sobel_y = cv2.convertScaleAbs(img_sobel_y)
    image_dic['img_sobel_y'] = img_sobel_y
    
    # sobel_xy
    img_sobel_xy = cv2.Sobel(img_gray, cv2.CV_32F, 1, 1, ksize=3)
    img_sobel_xy = cv2.convertScaleAbs(img_sobel_xy)
    image_dic['img_sobel_xy'] = img_sobel_xy
    
    # laplacian
    img_laplacian = cv2.Laplacian(img_gray, cv2.CV_32F)
    img_laplacian = cv2.convertScaleAbs(img_laplacian)
    image_dic['img_laplacian'] = img_laplacian
    
    # return
    # Return image_dic and result.
    # The image is automatically loaded.
    return(image_dic, result)
    