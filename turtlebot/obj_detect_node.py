from TurtlebotObstacleClass import Obstacle
import rospy
import time

rospy.init_node('turtlebot3_obstacle', anonymous=True)
turtlebot_state_variable = 'Nothing'

def turtlebot_state_function(data): #Subscriber which listen to topic state
	global turtlebot_state_variable 
	turtlebot_state_variable = data.data

rospy.Subscriber("/turtlebot_state", String, turtlebot_state_function)

Obstacles = Obstacle()

while True:
	#start = time.time()
	Obstacles.get_reading()
	Obstacle.make_list(100, 300, 0.3)
	if turtlebot_state_variable == 'hit'
		Obstacle.obstacle_cone('Front')
		Obstacle.obstacle_cone('Back')
		Obstacles.obstacle_not_cone('Front')
    	Obstacles.obstacle_not_cone('Back')
	elif turtlebot_state_function is not 'go back'
		Obstacles.obstacle_not_cone('Front')
    	Obstacles.obstacle_not_cone('Back')
    #end = time.time()
    #print(end-start)





     
