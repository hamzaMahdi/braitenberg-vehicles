#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
from std_msgs.msg import Float32MultiArray
import math
import numpy
pub = rospy.Publisher("proximity",Float32MultiArray,queue_size=1)

def multi_range(l, *args):
	output = []
	for indices in args:
		output += l[indices[0]:indices[1]]
		return output
def removeInf(data):
	output = []
	for point in data:
		if( numpy.isfinite(point)):
			print(point)
			output.append(point)
	return output
def check_obstacles(data):
	left = [data.ranges[i] for i in range(0,90)]
	right =[data.ranges[i] for i in range(270,359)]
	left=removeInf(left)
	right=removeInf(right)
	avgLeft = numpy.median(left)
	avgRight = numpy.median(right)
	if(math.isnan(avgRight)):
		avgRight = 3.5 # lidar range
	if(math.isnan(avgLeft)):
		avgLeft = 3.5
	my_array_for_publishing = Float32MultiArray(data=[avgLeft,avgRight])
	pub.publish(my_array_for_publishing)
rospy.init_node('proximity_checker', anonymous=True)
rospy.Subscriber("/scan", LaserScan, check_obstacles,queue_size=1)
rospy.spin()
