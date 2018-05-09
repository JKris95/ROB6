import rospy
from go_back_class import GoToPose
import time
import socket
from std_msgs.msg import String

#Connecet to server
HOST = '192.168.1.36'  
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
s.connect((HOST, PORT))

#Publisher
pub = rospy.Publisher('state', String, queue_size=10)

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
    elif data == 'Cone_hit'
        pub.publish('Cone_hit')
        time.sleep(1)
        pub.publish('Nothing')
    #elif data == 'STOP':
        #Goback.shutdown()
