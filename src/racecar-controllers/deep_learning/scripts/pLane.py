#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, struct, array, time
from fcntl import ioctl
from simple_pid import PID
from sensor_msgs.msg import Joy

import cv2
import numpy as np
import rospy
import threading
from enum import Enum
import std_msgs.msg
import time

import os.path
from os.path import expanduser
from ackermann_msgs.msg import AckermannDriveStamped
import message_types as mt
from message_types import message_types
from message_types import motor as m
from message_types import active_behavior
from deep_learning.msg import Burak
import re
import imutils

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"
            # if the shape has 4 vertices, it is either a square or
            # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

            # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"

            # otherwise, we assume the shape is a circle
        else:
            shape = "circle"

            # return the name of the shape

        return shape


class St:
    last_send = 0 
    stop_time = 0 

def talk():
    rate = rospy.Rate(20)
    vcap = cv2.VideoCapture(1)
    pid = get_pid()
    brk = Burak()
    brk.type = message_types.LANE
    ack = AckermannDriveStamped()
    counter = 0
    while True:
        counter += 1
        ret,image = vcap.read()
        blur = cv2.GaussianBlur(image,(5,5),0)
        lower_red = np.array([230,230,230])
        upper_red = np.array([255,255,255])
        mask = cv2.inRange(image, lower_red, upper_red)
        #negatif = 255 - frame
        top_sight = mask[270:290,240:440]
        crop_img = mask[440:480, 140:540]
        #negatif = 255 - crop_img
              
            
            
        # stop detection   
        if counter % 5 == 0:

        # Capture frame-by-frame
            #ret, frame = cap.read()
            frame = image[0:240,400:]
            # convert the resized image to grayscale, blur it slightly,
            # and threshold it
            shape = None
            lower_blue = np.array([70,0,0])
            upper_blue = np.array([150,40,30])
            mask = cv2.inRange(frame, lower_blue, upper_blue);
            mavi = cv2.bitwise_and(frame,frame, mask= mask)
            gray = cv2.cvtColor(mavi, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            thresh = cv2.threshold(blurred, 16, 255, cv2.THRESH_BINARY)[1]

            # find contours in the thresholded image and initialize the
            # shape detector
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if imutils.is_cv2() else cnts[1]
            for c in cnts:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
                M = cv2.moments(c)
                cX = int((M["m10"] / (M["m00"]+1e-7)) )
                cY = int((M["m01"] / (M["m00"]+1e-7)) )
                sd = ShapeDetector()
                shape = sd.detect(c)
                #print "SHAPE: " +str(shape)

                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                c = c.astype("int")
                #cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
                #cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)

                # show the output image
            #cv2.imshow("gray",gray)
            #cv2.imshow("mavi",mavi)
            #cv2.imshow("thresh",thresh)
            #cv2.imshow("frame",frame)
            if shape == "square"  and St.stop_time + 13 < time.time():
                St.stop_time = time.time()
                while True:
                    if St.stop_time + 10 < time.time():
                        break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            counter = counter % 5

        # node detection
        countTop = 0
        asilTop = 0
        for i in range(top_sight.shape[0]):
            for j in range(top_sight.shape[1]):
                asilTop += 1
                if top_sight[i][j] == 255:
                    countTop += 1
        print  (countTop / (asilTop*(1.0))*100)
        brk.hasObstacle = False
        if countTop > asilTop*(0.10) and St.last_send + 2 <time.time():
            brk.hasObstacle = True
            node.publish(brk)
            St.last_send = time.time()
            print "yeni nod buldum"

        while active_behavior.state > brk.type:
            rate.sleep()
            continue


        #gray = cv2.cvtColor(negatif, cv2.COLOR_BGR2GRAY)

        # Find the contours of the frame
        try:
            _,contours,hierarchy = cv2.findContours(crop_img.copy(), 1, cv2.CHAIN_APPROX_NONE)

            # Find the biggest contour (if detected)
            if len(contours) > 0:
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)


                cx = int(M['m10']/M['m00'])
                #cy = int(M['m01']/M['m00'])

                control = pid(cx)
                #print("steering: ",control)
                ack.drive.steering_angle = -1 * control
   
                #cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
                #cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
                #cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

            else:
		pass
                #print "I don't see the line"

        except Exception as e: 
            print(e)
            pass
        
        ack.drive.speed = m.speed
        pub.publish(ack)
        rate.sleep()
    vcap.release()

def get_pid():
    print "pid is set"
    pid = PID(0.001, 0.0000005, 0.0000005,setpoint=0.0)
    pid.setpoint = 0.0
    pid.sample_time = 0.01
    pid.auto_mode = True
    pid.output_limits = (-0.7, 0.7)
    pid.proportional_on_measurement  =  True
    return pid

if __name__ == '__main__':
    rospy.init_node('pLane', anonymous=True)
    pub = rospy.Publisher('/ackermann_cmd_mux/input/navigation', AckermannDriveStamped, queue_size=1)
    node = rospy.Publisher('node_update', Burak, queue_size=10)
    sub2 = rospy.Subscriber('/active_behavior', Burak, mt.behavior_callback)
    talk()
    rospy.spin()
