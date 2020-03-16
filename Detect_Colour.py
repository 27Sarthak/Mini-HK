#!/usr/bin/env python
import rospy
import sys
import cv2
import numpy as np
from cv_bridge import CvBridge 

from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage

'''
Function for detecting the ball 
and returning its coordinate
'''
def detectBall(frame):
	global counter, X, Y
	counter += 1

	# lime-green
	#colorLower = ( 25, 50,  0)
	#colorUpper = ( 90,255,255)
	#i1, i2 = 3, 10

	# # blue
	#colorLower = ( 205,54,86)
	#colorUpper = (135,255,255)
	#i1, i2 = 3, 5

     	# red
	#colorLower = (50 ,180,0)
	#colorUpper = (180,270,180)
	#i1, i2 = 3, 5

	# red simulation
	#colorLower = (0 ,0,0)
	#colorUpper = (0,100,100)
	#i1, i2 = 3, 5

	# blue simulation
	#colorLower = (100,150,0)
	#colorUpper = (140,255,255)
	#i1, i2 = 3, 5

	# red_rohelio
	colorLower = (161 ,155,84)
	colorUpper = (179,255,255)
	i1, i2 = 3, 5

	# blue_rohelio
	#colorLower = (94, 80,2)
	#colorUpper = (126,255,255)
	#i1, i2 = 3, 5

	# Convert to HSV color-space and create the mask
	hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=i1)
	mask = cv2.dilate(mask, None, iterations=i2)
	
	# Find all contours after a series of erosion/dilation
	(_,cnts, _) = cv2.findContours(mask.copy(), \
		cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	# Initializing x & y lists every nth frame
	if counter%4 == 0:
		X, Y = [], []

	# For each contour, get area, perimeter, filter, and find centroid
	for (i,c) in enumerate(cnts):
		area = cv2.contourArea(c)
		perimeter = cv2.arcLength(c, True)
		if area > 6000 and perimeter > 600:
			print ("Contour #%d -- area: %.2f, perimeter: %.2f" \
				% (i + 1, area, perimeter))			
			c = max(cnts, key=cv2.contourArea)
			M = cv2.moments(c)
			(cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			X.append(cX)
			Y.append(cY)

	# Average out each x & y location determined
	if X and Y:
		cX = int(sum(X)/len(X))
		cY = int(sum(Y)/len(Y))
		return cX, cY, mask
	else:
		return -100, -100, mask

# Callback called whenever image received
def image_callback(data):
	global cX, cY, pub

	# convert to numpy -> RGB
	image = bridge.compressed_imgmsg_to_cv2(data, "bgr8")
	h , w = image.shape[:2]

	# image = imutils.resize(image, width=int(w*8))
	cX, cY, mask = detectBall(image)

	# Create Point instance and set x, y methods
	point = Point()
	point.x = cX
	point.y = cY
	point.z = w 	# width of the frame
	pub_point.publish(point)		# Publish point on the publisher




	# just displaying it
	length = int(w/100)
	(startX, endX) = (int(cX - length), int(cX + length))
	(startY, endY) = (int(cY - length), int(cY + length))
	cv2.line(image, (startX, cY), (endX, cY), (0, 0, 255), 2)
	cv2.line(image, (cX, startY), (cX, endY), (0, 0, 255), 2)

	# image = imutils.resize(image, width=500)
	# mask = imutils.resize(mask, width=500)
	# cv2.imshow('image',image)
	# cv2.imshow('mask',mask)
	# cv2.waitKey(5)

if __name__ == '__main__':
	global counter, X, Y, cX, cY, pub
	counter = 0
	X, Y = [], []

	# Initialize the node
	#rospy.init_node('find_ball', anonymous=True)
	rospy.init_node('colour_detect', anonymous=True)

	# Subscribe to raspicam_node and receive the image
	img_sub = rospy.Subscriber("/raspicam_node/image/compressed",\
		CompressedImage, image_callback)
	#img_sub = rospy.Subscriber("/camera/rgb/image_raw/compressed",\
		#CompressedImage, image_callback)
	bridge = CvBridge()
	
	# Publish x-y coordinates over ball_location topic
	pub_point = rospy.Publisher('/ball_location', Point, queue_size=5)

	#Publishing with sys.argv
	#namespace = sys.argv[3]
	rospy.spin()
