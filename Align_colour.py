#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge 

from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from std_msgs.msg import String, Int16
from sensor_msgs.msg import CompressedImage, LaserScan
import time

# Callback function called whenever
# x-y coordinate received
class stuff:
	def __init__(self):
		self.trig = 0
		self.lds = 0
		self.pub_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
		self.trigger = rospy.Subscriber("/trigger_msg",Int16, self.msg_callback)
		# subscribe to /ball_location topic to receive coordinates
		self.img_sub = rospy.Subscriber("/ball_location",Point, self.drive_callback)
		self.sub = rospy.Subscriber("/scan", LaserScan,self.lds_callback)

	def msg_callback(self,msg):
		self.trig = msg.data
		#print(self.trig)
	
	def lds_callback(self,dt):
		self.lds = dt.ranges[0]

	def drive_callback(self,data):
		if  self.trig == 1:
			#print(trigger_msg)
			#global vel
			ball_x 	= data.x
			ball_y 	= data.y
			width  	= data.z
			print(data)
			# Create Twist() instance
			vel = Twist()

			# 
			if ball_x < 0 and ball_y < 0:
				vel.angular.z = 0
			else:
				# Determine center-x, normalized deviation from center
				mid_x  	= int(width/2)
				delta_x	= ball_x - mid_x
				norm_x 	= delta_x/width

				if norm_x > 0.15:
					print ("delX: {:.3f}. Turn right".format(norm_x))
					vel.angular.z = -0.5
				elif norm_x < -0.15:
					print ("delX: {:.3f}. Turn left".format(norm_x))
					vel.angular.z = 0.5
				if abs(norm_x) < 0.15:
					print ("delX: {:.3f}. Stay in center".format(norm_x))
					vel.angular.z = 0
					if self.lds > 0.2:
						print(self.lds)
						vel.linear.x = 0.1
					else:
						vel.linear.x = 0.0

					
			# publish vel on the publisher
			self.pub_vel.publish(vel)
			#state = 1
			
			# publish to /cmd_vel topic the angular-z velocity change
			
		else:
			pass

if __name__ == '__main__':
	# intialize the node
	rospy.init_node('follow_colour', anonymous=True)
	status = stuff()

	
	#while not rospy.is_shutdown:
	
	#if status.trig == 1:
		##print("yes")
	##print("no")
		#pass
		
	rospy.spin()
