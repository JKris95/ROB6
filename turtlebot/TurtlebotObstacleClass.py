
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
import numpy as np


class Obstacle():
	def __init__(self):
		self.pub = rospy.Publisher('det_ang', String, queue_size=10)
		self.LIDAR_ERR = 0.05
		self.is_detected = 0

	def get_scan(self, data, min_val, max_val):
		scan = LaserScan()
		scan = data
		for i in range(360):
			if i <= min_val or i > max_val:
				if scan.ranges[i] >= self.LIDAR_ERR:
					self.scan_filter.append(scan.ranges[i])

	def get_reading(self):
		self.msg = rospy.wait_for_message("/scan", LaserScan)

	def obstacle(self, steps, start, distance, direction):
		self.scan_filter = []
		msg_ranges_lenght = len(self.msg.ranges)
		for i in range(steps):
			if self.msg.ranges[start] >= self.LIDAR_ERR and self.msg.ranges[start] <= distance:
				self.scan_filter.append(self.msg.ranges[start])
			start = (start + 1) % msg_ranges_lenght
		#print(start)

		if np.mean(self.scan_filter) >= 0.18 and len(self.scan_filter) >= 10:
			self.pub.publish(direction)
			print(direction)
			self.is_detected = 1

		elif np.mean(self.scan_filter) >= 0.195 and len(self.scan_filter) >= 9:
			self.pub.publish(direction)
			print(direction)
			self.is_detected = 1

		elif np.mean(self.scan_filter) >= 0.222 and len(self.scan_filter) >= 8:
			self.pub.publish(direction)
			print(direction)
			self.is_detected = 1

		elif np.mean(self.scan_filter) >= 0.271 and len(self.scan_filter) >= 6:
			self.pub.publish(direction)
			print(direction)
			self.is_detected = 1

		elif np.mean(self.scan_filter) >= 0.291 and len(self.scan_filter) >= 3:
			self.pub.publish(direction)
			print(direction)
			self.is_detected = 1


		elif self.is_detected == 0:
			self.pub.publish('Nothing')
			#print('Nothing')

		else:
			self.is_detected = 0

def main():
	#rospy.init_node('turtlebot3_obstacle')
	try:
		obstacle = Obstacle()
	except rospy.ROSInterruptException:
		pass

if __name__ == '__main__':
	main()
