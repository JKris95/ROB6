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
    if data.data == 'turtle_hit':
        s.sendall(b'hit')

rospy.init_node('connection_node', anonymous=True)
rospy.Subscriber("/turtlebot_state", String, turtlebot_state_function)
pub = rospy.Publisher('turtlebot_state', String, queue_size=10)


while True:
	data = s.recv(1024)
	print(data)
	if data == 'go back':
		pub.publish(data)
	if data == 'hit':
		pub.publish(data)
		time.sleep(1)
		pub.publish('Nothing')
	if data == 'Nothing'
		pub.publish('Nothing')
