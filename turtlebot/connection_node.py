import rospy
import time
import socket
from std_msgs.msg import String
from geometry_msgs.msg import Twist



HOST = '192.168.1.34'  #HOST IP
PORT = 50007 #PORT number

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        

#Connect to game unit, if fail try again
while True:
    try:
        s.connect((HOST, PORT))
        break
    except:
        print("did not connect")

def turtlebot_state_function(data):
	print(data.data, 'connection node')
	if data.data == 'turtle_hit':
		s.sendall(b'hit')
		print('I sent a hit')
		pub.publish('Nothing')
		while data.data == 'turtle_hit':
			print('Waiting for which is not turtle_hit')


rospy.init_node('connection_node', anonymous=True)
rospy.Subscriber("/turtlebot_state", String, turtlebot_state_function)
pub = rospy.Publisher('/turtlebot_state', String, queue_size=10)
pubTwist = rospy.Publisher('/cmd_vel', Twist, queue_size=5) #queqe size can be adjusted maybe



while True:
	recv_data = s.recv(1024)
	if recv_data == 'go back':
		time.sleep(0.7)
		for i in range(0,5):
			pub.publish(recv_data)
			time.sleep(0.1)
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0 
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
		pubTwist.publish(twist)
		print('go back')
	if recv_data == 'hit':
		pub.publish(recv_data)
		print(recv_data)
		time.sleep(0.5)
		pub.publish('Nothing')
		print('Nothing')
	if recv_data == 'Nothing':
		pub.publish('Nothing')
		print('Nothing')
