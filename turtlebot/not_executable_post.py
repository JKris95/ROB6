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

twist = Twist()
lin = 0.0
ang = 0.0


def publish_cmd_vel():
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5) #queqe size can be adjusted maybe
	rospy.init_node('post_office')
	rate = rospy.Rate(10)
	while not rospy.is_shutdown(): #checking the rospy.is_shutdown() flag and then doing work. You have to check is_shutdown() to check if your program should exit (e.g. if there is a Ctrl-C or otherwise).
		twist.linear.x = lin; twist.linear.y = 0; twist.linear.z = 0 #liniar has to be .x value to change
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = ang #angular has to be .z value to change
		try:
			pub.publish(twist)
			rate.sleep()
		except:
			print('unable to publish')
		#rospy.loginfo(twist) #debugging: performs triple-duty: the messages get printed to screen, it gets written to the Node's log file, and it gets written to rosout. rosout is a handy for debugging: you can pull up messages using rqt_console instead of having to find the console window with your Node's output.

def recv_from_controller():
	while True:
		global lin, ang
		move_bytes = conn.recv(1024) #receive information as bytes
		print("Received", move_bytes, type(move_bytes))
		#move_info_string = move_bytes.decode()
		#print("After decoding", type(move_info_string))
		try:
			move_info = json.loads(move_bytes) #decode into a dictionary
		except ValueError:
			print('value error')
		lin = move_info['lin']
		ang = move_info['ang']
		#print(type(lin), lin, type(ang), ang)
		
thread.start_new_thread( recv_from_controller, ())    

while True:     
	publish_cmd_vel()
	
	#rospy.ROSInterruptException: #rospy.ROSInterruptException exception, which can be thrown by rospy.sleep() and rospy.Rate.sleep() methods when Ctrl-C is pressed or your Node is otherwise shutdown. NB! We have not placed any rates on our communication yet. 
	#pass
