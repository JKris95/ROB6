import rospy
import time
import socket
from std_msgs.msg import String


HOST = '192.168.1.34'  
PORT = 50007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        

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

rospy.init_node('connection_node', anonymous=True)
rospy.Subscriber("/turtlebot_state", String, turtlebot_state_function)
pub = rospy.Publisher('/turtlebot_state', String, queue_size=10)


while True:
	recv_data = s.recv(1024)
	print(recv_data, 'just recived this')
	if recv_data == 'go back':
		pub.publish(recv_data)
		print('go back')
	if recv_data == 'hit':
		pub.publish(recv_data)
		print(recv_data)
		time.sleep(1)
		pub.publish('Nothing')
		print('Nothing')
	if recv_data == 'Nothing':
		pub.publish('Nothing')
		print('Nothing')
