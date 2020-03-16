#!/usr/bin/env python
import rospy # Python library for ROS
from sensor_msgs.msg import LaserScan # LaserScan type message is defined in sensor_msgs
from geometry_msgs.msg import Twist #
from std_msgs.msg import String, Int16


class stuff:
    def __init__(self):
        self.trig = 0
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)  # Publisher object which will publish "Twist" type messages
                                                # on the "/cmd_vel" Topic, "queue_size" is the size of the
                                                            # outgoing message queue used for asynchronous publishing
        self.trigger = rospy.Subscriber("/trigger_msg",Int16,self.msg_callback)
        self.sub = rospy.Subscriber("/scan", LaserScan,self.callback)  # Subscriber object which will listen "LaserScan" type messages
                                                        # from the "/scan" Topic and call the "callback" function
                                # each time it reads something from the Topic
    def msg_callback(self,msg):
        self.trig = msg.data
        print(self.trig)

    def callback(self,dt):
        if self.trig == 0:
            print '-------------------------------------------'
            print 'Range data at 0 deg:   {}'.format(dt.ranges[0])
            print 'Range data at 15 deg:  {}'.format(dt.ranges[15])
            print 'Range data at 345 deg: {}'.format(dt.ranges[345])
            print '-------------------------------------------'
            move = Twist() # Creates a Twist message type object
            thr1 = 0.7 # Laser scan range threshold
            thr2 = 0.7
            if dt.ranges[0]>thr1 and dt.ranges[15]>thr2 and dt.ranges[345]>thr2: # Checks if there are obstacles in front and
                                                                                # 15 degrees left and right (Try changing the
                                            # the angle values as well as the thresholds)
                move.linear.x = 0.5 # go forward (linear velocity)
                move.angular.z = 0.0 # do not rotate (angular velocity)
            else:
                move.linear.x = 0.0 # stop
                move.angular.z = 0.3 # rotate counter-clockwise
                if dt.ranges[0]>thr1 and dt.ranges[15]>thr2 and dt.ranges[345]>thr2:
                    move.linear.x = 0.5
                    move.angular.z = 0.0
            self.pub.publish(move) # publish the move object 
        else:
			pass 

if __name__ == '__main__':
    # intialize the node
    rospy.init_node('obstacle_avoidance_node') # Initializes a node
    status = stuff()

    rospy.spin()   
