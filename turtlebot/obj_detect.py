import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

rospy.init_node('turtlebot3_obstacle', anonymous=True)
pub = rospy.Publisher('/det_ang', String, queue_size=10)

def obstacle():
    someVal = 0
    lidarErr = 0.05 #Some error values
    while True:
        msg = rospy.wait_for_message("/scan", LaserScan)
        scan_filter = []
        scan_filter2 = []
        for i in range(360):
            if i <= 50 or i >= 300: #Front values
                if msg.ranges[i] >= lidarErr:
                    scan_filter.append(msg.ranges[i])
                    if min(scan_filter) < 0.2: #Range where the turtlebot will react
                        pub.publish('Front')
                        rospy.loginfo('Front')
                        someVal = 50
                    elif someVal is not 0: #Not a pretty way to only publish one time, but i works with little to no delay.
                        someVal = someVal - 1
                        if someVal == 0:
                            pub.publish('Nothing')


            elif i <= 230 and i >= 130: #Back values
                if msg.ranges[i] >= lidarErr:
                    scan_filter2.append(msg.ranges[i])
                    if min(scan_filter2) < 0.2: #Range where the turtlebot will will react
                        pub.publish('Back')
                        rospy.loginfo('Back')
                        someVal = 50
                    elif someVal is not 0:
                        someVal = someVal - 1
                        if someVal == 0: 
                            pub.publish('Nothing')


obstacle()








