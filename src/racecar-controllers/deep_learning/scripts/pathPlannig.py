#!/usr/bin/python
# -*- coding: utf-8 -*-
#bu satır rosrunun kodu python olarak gormesini sagladı

import otonomus.network as network
from otonomus.Graph import Graph as Graph
import message_types as mt
from message_types import message_types
from message_types import active_behavior
from sensor_msgs.msg import Joy
from ackermann_msgs.msg import AckermannDriveStamped
from message_types import motor as m

from deep_learning.msg import Burak
import rospy
import math
import time


class St:
    TCP_IP = '192.168.1.100'
    port = 9999
    g = None
    route = None
    current_node = None
    run_time = 0
    reset_time = 0
    

brk = Burak()
brk.type = message_types.PATH_PLANNING
ack = AckermannDriveStamped()
def main():
    passenger_info = network.get_info(St.TCP_IP, St.port)
    print passenger_info
    St.g = Graph(passenger_info)
    St.route = St.g.get_route()
    St.current_node = 1
    print St.route
    
def getAngle(p1, p2):
    dX = p2.x - p1.x
    dY = p2.y - p1.y
    rads = math.atan2(-dY, dX)
    return math.degrees(rads)

def callback(msg):  
    g = St.g
    r = St.route
    c = St.current_node
    if len(r) > c + 1:
        v1 = g.get_vertex(r[c-1])
        v2 = g.get_vertex(r[c])
        v3 = g.get_vertex(r[c+1])
        
        angle = getAngle(v2,v3) - getAngle(v1,v2)
        
        if angle > 180:
            angle = angle - 360
        elif angle < -180 :
            angle = angle + 360 
                    
        path_planning(angle/100)
        St.current_node = c + 1
        print "current node: ",c ,": ",v2," and rotate: ",angle
         
def joy_back(joy_msg):
    if joy_msg.buttons[1] == 1 and St.run_time + 1 < time.time():
        St.run_time = time.time()
        state(-1)
        print "start"
    if joy_msg.buttons[3] == 1  and St.reset_time + 1 < time.time():
        St.reset_time = time.time()
        print "reset"
        main()       

        
def movement(steering = 0.0):
    ack.drive.steering_angle = steering
    ack.drive.speed = m.speed
    pub.publish(ack)


def path_planning(steering):
    state(message_types.PATH_PLANNING)
    wait_sec(0.2, 0)
    wait_sec(abs(steering), steering)
    state(-1)

    
def wait_sec(sec,i):
    timeout = time.time() + sec
    while True:
        movement(i)
        if time.time() > timeout:
            break
            
        
        
brk = Burak()
def state(state):
    brk.steering = state 
    pub2.publish(brk)
        

if __name__ == '__main__':
    rospy.init_node('pathPlannig', anonymous=True)
    pub = rospy.Publisher('/ackermann_cmd_mux/input/navigation', AckermannDriveStamped, queue_size=1)
    rospy.Subscriber('node_update', Burak, callback)
    sub2 = rospy.Subscriber('/active_behavior', Burak, mt.behavior_callback)
    pub2 = rospy.Publisher('/active_behavior', Burak, queue_size=1)
    joy_sub = rospy.Subscriber('/joy', Joy, joy_back)

    main()
    rospy.spin()
