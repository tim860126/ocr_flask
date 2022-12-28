from flask import render_template,Flask, request, abort
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from imutils.perspective import four_point_transform, order_points
import random
import time
import requests
import urllib3
import cv2 as cv
import numpy as np
import os
from urllib.parse import quote
from PIL import Image, ImageDraw, ImageFont

def label_crop(img):
    
    img = cv.resize(img, None, fx=0.9, fy=0.9)

    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    
    yellow_lower = np.array([22, 93, 0])
    yellow_upper = np.array([45, 255, 255])

    yellow_mask = cv.inRange(hsv_img, yellow_lower, yellow_upper)
    yellow = cv.bitwise_and(img, img, mask=yellow_mask)
        
    gray = cv.cvtColor(yellow, cv.COLOR_BGR2GRAY)

    contours, hierarchy = cv.findContours(
        gray, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    c = max(contours, key=cv.contourArea)

    # get contours
    x, y, w, h = cv.boundingRect(c)
    rect = cv.minAreaRect(c)
    box = cv.boxPoints(rect)
    box = np.int0(box)  # corner coordinate

    # draw contours
    im_show = img.copy()
    cv.drawContours(im_show, [box], 0, (0, 0, 255), 5)
  
    # img crop
    img_wraped = four_point_transform(img, box)

    cv.imwrite(("{filepath}{filename}.jpg".format(filepath="./", filename="test")), img_wraped)
    
    return "./test.jpg"
    
def imagePost():
    styleImage = request.files['imageFile'].read() #接收FormData格式
    styleImage = np.fromstring(styleImage, np.uint8) #np.fromstring() 轉成 ndarray 形式
    img = cv.imdecode(styleImage, cv.IMREAD_COLOR) #將 ndarray 轉換成擁有 RGB 3 個 channel 的圖像矩陣格式
    local_save=label_crop(img)
    
    API_KEY=os.getenv('API_KEY')

    ENDPOINT=os.getenv('ENDPOINT')

    computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))
    print("===== Read File - remote =====")

    read_response = computervision_client.read_in_stream(open(local_save,'rb'),raw=True)

    read_operation_location = read_response.headers["Operation-Location"]

    operation_id = read_operation_location.split("/")[-1]

    read_result = computervision_client.get_read_result(operation_id)
    
    
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    msg=""
    image=Image.open(local_save)#讀取與畫出Azure OCR辨識到的文字區域
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                ck=line.text
                msg+=ck  
                x1,y1,x2,y2,x3,y3,x4,y4 = line.bounding_box
                draw = ImageDraw.Draw(image)
                draw.line(
                    ((x1, y1), (x2, y1), (x2, y2), (x3, y2), (x3, y3), (x4, y3), (x4, y4), (x1, y4), (x1, y1)),
                    fill=(255,0,0),
                    width=5
                )
    image.save("result.jpg")
    
    return msg

def hello_world():
    return "123456"

def index():
    title = "Jinja 示範"
    big_word = "SHOW ME JINJA"
    return render_template('index.html', title=title, big_word=big_word)

