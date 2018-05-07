import time
import rospy
from geometry_msgs.msg import Twist

def move():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
    twist = Twist()
    for i in range (0,2):
        twist.linear.x = 0.01; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        time.sleep(0.25)
        
    twist.linear.x = 0.2; twist.linear.y = 0; twist.linear.z = 0
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
    pub.publish(twist)
    time.sleep(2)
    twist.linear.x = -0.2; twist.linear.y = 0; twist.linear.z = 0
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
    pub.publish(twist)
    time.sleep(4)
    twist.linear.x = 0.2; twist.linear.y = 0; twist.linear.z = 0
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
    time.sleep(2)
    twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
    pub.publish(twist)

if __name__ == "__main__":
    rospy.init_node('moveinit', anonymous=False)   
    move()
