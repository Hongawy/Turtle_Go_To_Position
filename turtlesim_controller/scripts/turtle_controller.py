#!/usr/bin/env python3
from turtle import delay
import rospy
import math
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
#from std_msgs.msg import String#

#Load the values from the yaml file#
x_goal =rospy.get_param("/x_goal")
y_goal =rospy.get_param("/y_goal")
k_linear = rospy.get_param("/k_linear")
k_angular = rospy.get_param("/k_angular")

def pose_callback(pose: Pose):
    #Create an object from Twist Class#
    cmd = Twist()

    #Round up the position coordinates to 4 decimals#
    pose.x =round(pose.x,4)
    pose.y =round(pose.y,4)

    #Calculate Remaining Distance#
    distance_to_move= abs(math.sqrt(((x_goal-pose.x)**2) + ((y_goal-pose.y)**2)))
    #Calculate Desired Angle#
    desired_angle = -(pose.theta) + math.atan2((y_goal-pose.y) , (x_goal-pose.x))
    desired_angle = abs(desired_angle)
    if distance_to_move>= 0.11:
        #Calculate linear and angular velocities#
        cmd.linear.x= (k_linear) * (distance_to_move)
        cmd.angular.z=(k_angular) * (desired_angle)
        #Publish the calculated values#
        pub.publish(cmd)
    else:  
        cmd.linear.x= 0.0
        cmd.linear.y= 0.0
        cmd.linear.z= 0.0
        cmd.angular.x= 0.0
        cmd.angular.y= 0.0
        cmd.angular.z= 0.0
        pub.publish(cmd) 
        rospy.loginfo("7amdella 3al slama ^_^")

if __name__ == '__main__':

    rospy.init_node("turtle_go_to_pose")
    rospy.loginfo("Node Has Been Started")
    pub = rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=10)
    sub = rospy.Subscriber("/turtle1/pose",Pose,callback=pose_callback)
    
    rospy.spin()