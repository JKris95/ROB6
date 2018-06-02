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
Cone_front = Obstacle()
Cone_back = Obstacle()


while True:
	#start = time.time()
	if turtlebot_state_variable != 'Nothing':
		print(turtlebot_state_variable, 'detection node')
	if turtlebot_state_variable == 'hit':
		Front.get_reading()
		Front.make_list(100, 300, 0.3, Front.msg)
		Back.make_list(100, 130, 0.3, Front.msg)
		Cone_front.make_list(178, 271, 0.3, Front.msg)
		Cone_back.make_list(178, 91, 0.3, Front.msg)
		Cone_front.obstacle_cone('Front')
		Cone_back.obstacle_cone('Back')
		#Front.obstacle_not_cone('Front')
		#Back.obstacle_not_cone('Back')
	elif turtlebot_state_variable != 'go back':
		Front.get_reading()
		Front.make_list(50, 325, 0.3, Front.msg)
		Back.make_list(50, 155, 0.3, Front.msg)
		Front.obstacle_not_cone('Front')
		Back.obstacle_not_cone('Back')
    #end = time.time()
    #print(end-start)





     
