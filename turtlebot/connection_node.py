import rospy
import time
import socket
from std_msgs.msg import String

HOST = '192.168.1.34'  
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
s.connect((HOST, PORT))

rospy.Subscriber("/turtlebot_state", String, turtlebot_state_function)
pub = rospy.Publisher('turtlebot_state', String, queue_size=10)


def turtlebot_state_function(data):
    if data.data == 'turtle_hit':
        s.sendall(b'hit')

while True:
	data = s.recv(1024)
	pub.publish(data)
