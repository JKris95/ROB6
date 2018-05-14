import rospy
from go_back_class import GoToPose
import time
import socket
from std_msgs.msg import String

rospy.init_node('go_back', anonymous=True)

#Connecet to server
HOST = '192.168.1.34'  
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
s.connect((HOST, PORT))

#Publisher
pub = rospy.Publisher('turtlebot_state', String, queue_size=10)
#Subscriber
rospy.Subscriber("/turtlebot_state", String, turtlebot_state_function)


#Create object and declare global cordinates for robots returning position
Goback = GoToPose()
position = {'x': 0, 'y' : 0}
quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000} 
while True:
    data = s.recv(1024)
    if data == 'Goback':
        pub.publish('Going_Back')
        Goback.goto(position, quaternion)
        pub.publish('Nothing')
    elif data == 'hit':
        pub.publish('hit')
        time.sleep(1)
        pub.publish('Nothing')
    #elif data == 'STOP':
        #Goback.shutdown()

def turtlebot_state_function(data):
    if data.data == 'White turtlebot hit' or data.data == 'Black turtlebot hit':
        s.sendall(data.data)
    
