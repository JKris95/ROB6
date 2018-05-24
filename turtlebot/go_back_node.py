import rospy
from go_back_class import GoToPose
import time
from std_msgs.msg import String

topic_status_value = 'Nothing'
rospy.init_node('go_back', anonymous=True)

def turtlebot_state_function(data):
	global topic_status_value
	topic_status_value = data.data
	print(data.data)

#Publisher
pub = rospy.Publisher('/turtlebot_state', String, queue_size=10)
#Subscriber
rospy.Subscriber("/turtlebot_state", String, turtlebot_state_function)


#Create object and declare global cordinates for robots returning position
Goback = GoToPose()
position = {'x': 0, 'y' : 0}
quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000} 
while True:
    if topic_status_value == 'go back':
		time.sleep(2)
		print('topic_status_value')
		Goback.goto(position, quaternion)
		while topic_status_value == 'go back':
			print('wait for nothing to be send')
        #pub.publish('Nothing')
    #elif data == 'STOP':
        #Goback.shutdown()

    
