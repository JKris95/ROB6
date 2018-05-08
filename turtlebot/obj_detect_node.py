from TurtlebotObstacleClass import Obstacle
import rospy
import time

rospy.init_node('turtlebot3_obstacle', anonymous=True)
rospy.Subscriber("/state", String, state)

Obstacles = Obstacle()

while True:
    #start = time.time()
    Obstacles.get_reading()
    if state == 'Nothing' or 'Front' or 'Back':
        Obstacles.obstacle(100, 300, 0.3, 'Front')
        Obstacles.obstacle(100, 130, 0.3, 'Back')
    #end = time.time()
    #print(end-start)

def state(data): #Subscriber which listen to topic state
	global state 
	state = data.data



     
