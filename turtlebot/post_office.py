import socket
import json
import rospy
from geometry_msgs.msg import Twist
import thread
import time

HOST = ''
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print ('Connected by', addr)

move_info = {'lin': 0, 'ang': 0}


def publish_cmd_vel():
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
	while True:
		twist = Twist()
		twist.linear.x = move_info["lin"]; twist.linear.y = 0; twist.linear.z = 0 #liniar has to be .x value to change
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = move_info["ang"] #angular has to be .z value to change
		pub.publish(twist)

def recv_from_controller():
	while True:
		move_bytes = conn.recv(1024) #receive information as bytes
		move_info = json.loads(move_bytes.decode()) #decode into a dictionary


thread.start_new_thread( recv_from_controller, ())    

rospy.init_node('post_office')

while True:    
	publish_cmd_vel()
