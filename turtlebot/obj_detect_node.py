from TurtlebotObstacleClass import Obstacle
import rospy
import time
from std_msgs.msg import String


rospy.init_node('turtlebot3_obstacle', anonymous=True)
turtlebot_state_variable = 'Nothing'

def turtlebot_state_function(data): #Subscriber which listen to topic state
	global turtlebot_state_variable 
	turtlebot_state_variable = data.data

rospy.Subscriber("/turtlebot_state", String, turtlebot_state_function)

Front = Obstacle()
Back = Obstacle()
Cone = Obstacle()

'''for i in range(0,10):
	Front.get_reading()

while True:
	print(hej)'''

while True:
	#start = time.time()
	Front.get_reading()
	Front.make_list(100, 300, 0.3, Front.msg)
	Back.make_list(100, 130, 0.3, Front.msg)
	if turtlebot_state_variable == 'hit':
		Cone.make_list(360, 0, 0.2, Front.msg)
		Cone.obstacle_cone('Front')
		Front.obstacle_not_cone('Front')
		Back.obstacle_not_cone('Back')
	elif turtlebot_state_variable != 'go back':
		Front.obstacle_not_cone('Front')
		Back.obstacle_not_cone('Back')
    #end = time.time()
    #print(end-start)





     
