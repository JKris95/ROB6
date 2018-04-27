import socket
import json
import rospy
from geometry_msgs.msg import Twist
import thread
import time
from std_msgs.msg import String

HOST = ''
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
detected = 'Nothing'
print ('Connected by', addr)

twist = Twist()
move_info = {'lin': 0, 'ang': 0}
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5) #queqe size can be adjusted maybe

def callback(data):
    global detected = data.data

def publish_cmd_vel():
    while not rospy.is_shutdown():
	    while detected = 'Nothing':
		    twist.linear.x = move_info["lin"]; twist.linear.y = 0; twist.linear.z = 0 #liniar has to be .x value to change
		    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = move_info["ang"] #angular has to be .z value to change
		    try:
			    pub.publish(twist)
		    except:
			    print('unable to publish')
        if detected = 'Forward':
        	twist.linear.x = 0.1; twist.linear.y = 0; twist.linear.z = 0 #liniar has to be .x value to change
		    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0 #angular has to be .z value to change
            time.sleep(1)
        if detected = 'Back':
            twist.linear.x = -0.1; twist.linear.y = 0; twist.linear.z = 0 #liniar has to be .x value to change
		    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0 #angular has to be .z value to change

def recv_from_controller():
	while True:
		global move_info
		move_bytes = conn.recv(1024) #receive information as bytes
		print("Type received", type(move_bytes))
		#move_info_string = move_bytes.decode()
		#print("After decoding", type(move_info_string))
		move_info = json.loads(move_bytes) #decode into a dictionary
		print("after JSON", type(move_info), move_info)

thread.start_new_thread( recv_from_controller, ())    

rospy.init_node('post_office', anonymous = False)
rospy.Subscriber("detect_angle", String, detection)

while True:     
	try:
		publish_cmd_vel()
	except rospy.ROSInterruptException: #rospy.ROSInterruptException exception, which can be thrown by rospy.sleep() and rospy.Rate.sleep() methods when Ctrl-C is pressed or your Node is otherwise shutdown. NB! We have not placed any rates on our communication yet. 
		pass
