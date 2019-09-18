#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
pub = rospy.Publisher("/cmd_vel",Twist,queue_size=1)
mode = "love"
def move(data):
    vel_msg = Twist()

    if(mode=="fear"):
        vel_msg.linear.x = (((data.data[0] + data.data[
            1]) / 2) - 2) / 3.5 * 0.25  # faster when there is no obstacle and slows down
        # the division by 3.5 and multiplication by 0.25 is to normalize it to the max speed of the robot
        # see documentation on the robot's physical properties
        vel_msg.angular.z = (data.data[0]-data.data[1])*0.1
    if(mode == "aggression"):
        vel_msg.linear.x = 0.25
        if(data.data[0]>data.data[1]):
            vel_msg.angular.z = -0.1
        elif(data.data[0]<data.data[1]):
            vel_msg.angular.z = 0.1
        else:
            vel_msg.angular.z = 0
    if(mode=="love"):
        vel_msg.linear.x = (((data.data[0] + data.data[
            1]) / 2) - 1) / 3.5 * 0.25
        if (data.data[0] > data.data[1]):
            vel_msg.angular.z = -0.1
        elif (data.data[0] < data.data[1]):
            vel_msg.angular.z = 0.1
        else:
            vel_msg.angular.z = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    pub.publish(vel_msg)

rospy.init_node('braitenberg_turtle', anonymous=True)
rospy.Subscriber("/proximity", Float32MultiArray, move,queue_size=1)
rospy.spin()