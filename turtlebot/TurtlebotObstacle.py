
#!/usr/bin/env python
#################################################################################
# Copyright 2018 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#################################################################################

# Authors: Gilbert #

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import String



class Obstacle():
    def __init__(self):
        self.pub = rospy.Publisher('detect_angle', String, queue_size=10)
        self.LIDAR_ERR = 0.05

    def get_scan(self, data, min_val, max_val):
        scan = LaserScan()
        scan = data
        for i in range(360):
            if i <= min_val or i > max_val:
                if scan.ranges[i] >= self.LIDAR_ERR:
                    self.scan_filter.append(scan.ranges[i])

    def obstacle(self, steps, start, distance, direction):
        msg = rospy.wait_for_message("/scan", LaserScan)
        self.scan_filter = []
        msg_ranges_lenght = len(msg.ranges)
        for i in range(steps):
            if msg.ranges[start] >= self.LIDAR_ERR:
                self.scan_filter.append(msg.ranges[start])
            start = (start + 1) % msg_ranges_lenght
	    print(start)

        if self.scan_filter and min(self.scan_filter) < distance:
            #self.pub.publish(direction)
	    #print(self.scan_filter)
            print(direction)

        else:
            self.pub.publish('Nothing')
            #print('Nothing')


def main():
    #rospy.init_node('turtlebot3_obstacle')
    try:
        obstacle = Obstacle()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()
