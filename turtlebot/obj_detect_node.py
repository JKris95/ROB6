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

while True:
	#start = time.time()
	Front.get_reading()
	Front.make_list(100, 300, 0.3, Front.msg)
	Back.make_list(100, 130, 0.3, Front.msg)
	if turtlebot_state_variable == 'hit':
		Front.obstacle_cone('Front')
		Back.obstacle_cone('Back')
		Front.obstacle_not_cone('Front')
    	Back.obstacle_not_cone('Back')
	elif turtlebot_state_function is not 'go back':
		Front.obstacle_not_cone('Front')
    	Back.obstacle_not_cone('Back')
    #end = time.time()
    #print(end-start)





     
