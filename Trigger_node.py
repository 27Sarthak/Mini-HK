#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge 

from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from std_msgs.msg import String,Int16
from sensor_msgs.msg import CompressedImage
import time
from sensor_msgs.msg import LaserScan
# Callback function called whenever
# x-y coordinate received



def callback(data):
    global msg
    ball_x 	= data.x
    ball_y 	= data.y
    width  	= data.z
    #print(width)
    #print(ball_x)
    #print(ball_y)
    #print("callback")
    if ball_x != -100 or ball_y != -100 or width != 640: ## intended object is there

        msg = 1
        #return msg
    else:
        msg = 0
        #print(msg)
        #return msg
    #print(msg)
    triggerit = msg
    #print(triggerit)
    pub_trigger.publish(triggerit)
    

if __name__ == '__main__':
    global msg, pub_trigger, triggerit
	# Initialize the node
	#rospy.init_node('find_ball', anonymous=True)
    rospy.init_node('MainNode', anonymous=True)

    #rospy.init_node('follow_colour', anonymous=True)

    # subscribe to /ball_location topic to receive coordinates
    img_sub = rospy.Subscriber("/ball_location",Point, callback)
    
	# Publish x-y coordinates over trigger_msg topic
    pub_trigger = rospy.Publisher('trigger_msg', Int16 ,queue_size=10)
    rospy.spin()
