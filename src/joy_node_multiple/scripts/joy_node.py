#!/usr/bin/python
# -*- coding: utf-8 -*-



# Released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentation/input/joystick-api.txt


import os, struct, array, time
from fcntl import ioctl

# from ackermann_msgs.msg import AckermannDriveStamped
from sensor_msgs.msg import Joy

import numpy as np
import rospy
import sys
import threading
from enum import Enum


class Joystick:
    def initJoystick(self):
        jsdev = self.jsdev
        # We'll store the states here.
        axis_states = {}
        button_states = {}

        # These constants were borrowed from linux/input.h
        axis_names = {
            0x00 : 'x',
            0x01 : 'y',
            0x02 : 'z',
            0x03 : 'rx',
            0x04 : 'ry',
            0x05 : 'rz',
            0x06 : 'trottle',
            0x07 : 'rudder',
            0x08 : 'wheel',
            0x09 : 'gas',
            0x0a : 'brake',
            0x10 : 'hat0x',
            0x11 : 'hat0y',
            0x12 : 'hat1x',
            0x13 : 'hat1y',
            0x14 : 'hat2x',
            0x15 : 'hat2y',
            0x16 : 'hat3x',
            0x17 : 'hat3y',
            0x18 : 'pressure',
            0x19 : 'distance',
            0x1a : 'tilt_x',
            0x1b : 'tilt_y',
            0x1c : 'tool_width',
            0x20 : 'volume',
            0x28 : 'misc',
        }

        button_names = {
            0x120 : 'trigger',
            0x121 : 'thumb',
            0x122 : 'thumb2',
            0x123 : 'top',
            0x124 : 'top2',
            0x125 : 'pinkie',
            0x126 : 'base',
            0x127 : 'base2',
            0x128 : 'base3',
            0x129 : 'base4',
            0x12a : 'base5',
            0x12b : 'base6',
            0x12f : 'dead',
            0x130 : 'a',
            0x131 : 'b',
            0x132 : 'c',
            0x133 : 'x',
            0x134 : 'y',
            0x135 : 'z',
            0x136 : 'tl',
            0x137 : 'tr',
            0x138 : 'tl2',
            0x139 : 'tr2',
            0x13a : 'select',
            0x13b : 'start',
            0x13c : 'mode',
            0x13d : 'thumbl',
            0x13e : 'thumbr',

            0x220 : 'dpad_up',
            0x221 : 'dpad_down',
            0x222 : 'dpad_left',
            0x223 : 'dpad_right',

            # XBox 360 controller uses these codes.
            0x2c0 : 'dpad_left',
            0x2c1 : 'dpad_right',
            0x2c2 : 'dpad_up',
            0x2c3 : 'dpad_down',
        }

        axis_map = []
        button_map = []
        
        # Get the device name.
        #buf = bytearray(63)
        buf = array.array('c', ['\0'] * 64)
        ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
        js_name = buf.tostring()
        print('Device name: %s' % js_name)

        # Get number of axes and buttons.
        buf = array.array('B', [0])
        ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
        num_axes = buf[0]

        buf = array.array('B', [0])
        ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
        num_buttons = buf[0]

        # Get the axis map.
        buf = array.array('B', [0] * 0x40)
        ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP

        for axis in buf[:num_axes]:
            axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
            axis_map.append(axis_name)
            axis_states[axis_name] = 0.0

        # Get the button map.
        buf = array.array('H', [0] * 200)
        ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

        for btn in buf[:num_buttons]:
            btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
            button_map.append(btn_name)
            button_states[btn_name] = 0

        print('%d axes found: %s' % (num_axes, ', '.join(axis_map)))
        print('%d buttons found: %s' % (num_buttons, ', '.join(button_map)))

        self.button_names = button_names
        self.button_map = button_map
        self.button_states = button_states
        self.axis_names = axis_names
        self.axis_map = axis_map
        self.axis_states = axis_states
        
    def __init__(self, jsName, jsdev):
        self.jsName = jsName
        self.jsdev = jsdev
        self.initJoystick()

    jsName = ""     # name of the joystick (js0, js1 etc..)
    jsdev = file    # linux input file for joystick
    
failedDevices = []
def openJoystick(jsName):    
    # don't open already opened joysticks
    for joystick in joysticks:
        if joystick.jsName == jsName:
            return

    # if the device is failing, require re-plugging
    for failedDevName in failedDevices:
        if failedDevName == jsName:
            return
    print('Found joystick on: /dev/input/%s' % (jsName))
    
    jsdev = file
    try:
        fn = '/dev/input/' + jsName
        print('Opening %s...' % fn)
        jsdev = open(fn, 'rb')
        joystick = Joystick(jsName, jsdev)
        joysticks.append(joystick)
        print("✓ Connected to " + jsName)
    except:
        print("✗ Could not open /dev/input/%s\t are you sure it's on?" % jsName)
        failedDevices.append(jsName)


killthreads = False
def killswitch():
    return killthreads

# background process:
def populateJoysticks(openJoystick_callback, killswitch):
    print('Looking for available joysticks:')

    n = 0   # flag
    while True:
        if killswitch():
            return
        # search for joysticks and get names (js0, js1 etc..)
        jsNames = []
        first = True
        for fn in os.listdir('/dev/input'):
            if fn.startswith('js'):
                jsNames.append(fn)

        if n == 1 and len(joysticks) < 1 and len(failedDevices) < 1:
            print("No joysticks found. Will connect when plugged in..")
        if n < 2:
            n += 1

        
        # check if re-plugged
        for failedDevName in failedDevices:
            if failedDevName not in jsNames:
                failedDevices.remove(failedDevName)

        # attempt to open joysticks
        for jsName in jsNames:
            openJoystick_callback(jsName)

        time.sleep(0.5)



class joyControlType:
    initial = 128
    button  = 1
    axis    = 2

def talker():

    joy_msg = Joy()
    joy_msg.axes = [0.0] * 6
    joy_msg.buttons = [0] * 12
    pub = rospy.Publisher('/joy', Joy, queue_size=1)
    rospy.init_node('joy_node_multiple', anonymous=True)
    # rate = rospy.Rate(10)

    newmsg = False  # flag
    while not rospy.is_shutdown():
        try:
                
            # print("NUMBER OF JOYSTICKS: " + str(len(joysticks)))
            newmsg = False
            for joystick in joysticks:
                jsdev = joystick.jsdev
                evbuf = jsdev.read(8) # [-8:]   // will wait until there is data to read
                # print(evbuf)
                if evbuf:
                    newmsg = True
                    time, value, type, number = struct.unpack('IhBB', evbuf)

                    if type == joyControlType.button:
                        button = joystick.button_map[number]
                        # joystick.button_states[button] = value
                        
                        # print(button + " " + str(value))
                        joy_msg.buttons[number] = value
                    if type == joyControlType.axis:
                        axis = joystick.axis_map[number]
                        fvalue = value / 32767.0
                        # joystick.axis_states[axis] = fvalue
                        # print("%s: %.3f" % (axis, fvalue) + "   !!!!!!!!!!!!!!!!!!!  " + str(number))
                        # print(joy_msg.axes)
                        joy_msg.axes[number] = fvalue
                    # if type == 2:
                    #     if len(joystick.axis_map) >= 2:

            if newmsg:
                joy_msg.header.stamp = rospy.Time.now()
                # print(joy_msg)
                pub.publish(joy_msg)
            # rate.sleep()

        except Exception as e:
            print("Error : ",e)
            
# joystick objects:
joysticks = []

if __name__ == '__main__':

    # Start searching for joysticks in background
    thr = threading.Thread(target = populateJoysticks, args=(openJoystick,killswitch))
    thr.deamon = True
    thr.start()
    # Start recording and publishing jostick data
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
