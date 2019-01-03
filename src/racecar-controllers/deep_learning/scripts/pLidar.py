#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import std_msgs.msg
import time
import rospy
import message_types as mt
from message_types import message_types
from message_types import active_behavior
from sensor_msgs.msg import LaserScan
from deep_learning.msg import Burak
from ackermann_msgs.msg import AckermannDriveStamped
from message_types import motor as m

class St:
	last_send = 0
	right = True
	
brk = Burak()        
brk.type = message_types.LIDAR
ack = AckermannDriveStamped()

def callback(msg):
	if active_behavior.state > brk.type:
	    return
	ranges = msg.ranges
	front_distance=msg.range_max
	ranges_count=len(ranges)
	middle = ranges_count/2
	angle =0
	for i in range(0,10,1):
	    if not np.isinf(ranges[i]):
	        if ranges[i]<front_distance:
	            front_distance=ranges[i]
	            angle=i
	
	#print front_distance  
	if not St.right:
		if  time.time() > St.last_send + 2:
			lidar(False)
	
	elif front_distance < 1:
	    if time.time() > St.last_send + 5:
	        print "engel"
	        St.last_send = time.time()
	        lidar(True)


def lidar(right):
	if right:
		state(message_types.LIDAR)
		wait_sec(0.4,-0.30)
		state(-1) 
		St.right = False
	elif not St.right:
		state(message_types.LIDAR)
		wait_sec(0.4,0.3)
		state(-1)   
		St.right = True
   

def wait_sec(sec,i):
	timeout = time.time() + sec
	while True:
	    movement(i)
	    if time.time() > timeout:
	        break

def movement(steering = 0.0):
	ack.drive.steering_angle = steering
	ack.drive.speed = m.speed
	pub.publish(ack)
	
def pass_obstacle():
	return [-1*m.steering,m.steering,0.0,m.steering,-1 * m.steering]

	        
brk = Burak()
def state(state):
	brk.steering = state 
	pub2.publish(brk)
	    
rospy.init_node('pLidar', anonymous=True)
pub = rospy.Publisher('/ackermann_cmd_mux/input/navigation', AckermannDriveStamped, queue_size=1)
sub = rospy.Subscriber('/scan', LaserScan, callback)
sub2 = rospy.Subscriber('/active_behavior', Burak, mt.behavior_callback)
pub2 = rospy.Publisher('/active_behavior', Burak, queue_size=1)
rospy.spin()



