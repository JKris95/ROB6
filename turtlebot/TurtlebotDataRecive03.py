import socket
import json
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import sys, select, termios, tty
import thread
import time

HOST = ''
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print ('Connected by', addr)

turtle_go = [0,0]
turtle_stop = 0

speedAngular = 2 #Change turning speed
speedLinear = 0.2 #Change linear speed
speedAngularAngular = 0.2 #Change turning speed when driving linear and turning
speedAngularLinear = 0.1 #Change linear speed when driving linear and turning

'''def obstacle():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
    twist = Twist()
    lidarErr = 0.05
    global turtle_stop
    while True:
        msg = rospy.wait_for_message("/scan", LaserScan)
        scan_filter = []
        for i in range(360):
            #if i <= 15 or i > 335:
            if msg.ranges[i] >= lidarErr:
                scan_filter.append(msg.ranges[i])

        if min(scan_filter) < 0.175:
            turtle_stop = 1
            rospy.loginfo('Stop!')
	    time.sleep(1.5)
        else:
            turtle_stop = 0'''

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def eightWay():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
    while True:
        key = getKey()
        while turtle_stop == 0:
            twist = Twist()
            key = getKey()
            twist.linear.x = turtle_go[0]; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = turtle_go[1] 

            if (key == '\x03'):
                twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
                twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
                break
            pub.publish(twist)
        twist.linear.x = -turtle_go[0]; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = -turtle_go[1]
	pub.publish(twist)
	time.sleep(1)
        if (key == '\x03'):
            twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
            break



def Data():
    while True:
        global turtle_go
        data = conn.recv(1024)
	data = json.loads(data.decode())
	turtle_go = data.get("a")


if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('turtlebot3_obstacle')
    thread.start_new_thread( Data, ())
    #thread.start_new_thread( obstacle, ())
    eightWay()
