import socket
import json
import rospy
from geometry_msgs.msg import Twist
import thread
import time
from std_msgs.msg import String

#Global variables go here.
HOST = ''
PORT = 50000
lin,ang = 0.0,0.0
turtlebot_state_variable = 'Nothing'
variable_to_not_spam_topic = 0



#Function definitions goes here.
def publish_cmd_vel():

	#Function that creates the node, and publishes to the topic /cmd_vel and subscribe to /state 
	global variable_to_not_spam_topic
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5) #queqe size can be adjusted maybe
	rospy.Subscriber("/turtlebot_state", String, turtlebot_state_function)
	rospy.init_node('post_office')
	rate = rospy.Rate(10) #10 hz executing on the node
	while not rospy.is_shutdown():
		while turtlebot_state_variable == 'Nothing' or turtlebot_state_variable == 'hit' or turtlebot_state_variable == 'turtle_hit': #checking the rospy.is_shutdown() flag and then doing work. You have to check is_shutdown() to check if your program should exit (e.g. if there is a Ctrl-C or otherwise).
			twist.linear.x = lin; twist.linear.y = 0; twist.linear.z = 0 #liniar has to be .x value to change
			twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = ang #angular has to be .z value to change
			variable_to_not_spam_topic = 1
			try:
				pub.publish(twist)
				rate.sleep()
			except:
				print('unable to publish')
		#rospy.loginfo(twist) #debugging: performs triple-duty: the messages get printed to screen, it gets written to the Node's log file, and it gets written to rosout. rosout is a handy for debugging: you can pull up messages using rqt_console instead of having to find the console window with your Node's output.
		if turtlebot_state_variable == 'Front': #What to do if the turtlebot detects something in front of it
			twist.linear.x = -0.2; twist.linear.y = 0; twist.linear.z = 0 #liniar has to be .x value to change
			twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0 #angular has to be .z value to change
			pub.publish(twist)
			time.sleep(0.5)
			print('back')
		elif turtlebot_state_variable == 'Back': #What to do if the turtlebot detects something in front of it
			twist.linear.x = 0.2; twist.linear.y = 0; twist.linear.z = 0 #liniar has to be .x value to change
			twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0 #angular has to be .z value to change
			pub.publish(twist)
			time.sleep(0.5)
			print('forward')
		elif twist.linear.x != 0 and variable_to_not_spam_topic == 1:
			twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0 
			twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
			pub.publish(twist)
			variable_to_not_spam_topic = 0
			print('going back so stop')

def recv_from_controller():

	#Function that receives information from the connected controller.

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

def turtlebot_state_function(data): #Subscriber which listen to topic state
	global turtlebot_state_variable 
	turtlebot_state_variable = data.data
	#print(state)



#While True loop retrying to accept a connection if the old breaks dowm. TODO: Check if the thread gets killed if the connection drops. If not kill it.
while True:

		#Creation of socket object and accept of incoming connection. NB! s.accept() blocks untill a connection is made.
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(1) #the parameter 1 indicates only 1 connection will be accepted.
	conn, addr = s.accept()
	print ('Connected by', addr)

	#Creation of object from the Twist() class. This object is used as a message type on to publish on the topic /cmd_vel.
	twist = Twist()

	#Starting a thread to feed information from the connected controller into the global variables lin and ang.		
	thread.start_new_thread( recv_from_controller, ())    

	while True:     
		publish_cmd_vel()
			
		#rospy.ROSInterruptException: #rospy.ROSInterruptException exception, which can be thrown by rospy.sleep() and rospy.Rate.sleep() methods when Ctrl-C is pressed or your Node is otherwise shutdown. NB! We have not placed any rates on our communication yet. 
		#pass

