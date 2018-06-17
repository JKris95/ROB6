
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
import time
import csv


class Obstacle():
	def __init__(self):
		self.pub = rospy.Publisher('/turtlebot_state', String, queue_size=10)
		self.pub.publish('Nothing')
		self.LIDAR_ERR = 0.05
		self.is_detected = 0
		self.nothing_sent = 0
		self.msg = 0


	def get_scan(self, data, min_val, max_val):
		scan = LaserScan()
		scan = data
		for i in range(360):
			if i <= min_val or i > max_val:
				if scan.ranges[i] >= self.LIDAR_ERR:
					self.scan_filter.append(scan.ranges[i])

	def get_reading(self):
		self.msg = rospy.wait_for_message("/scan", LaserScan)


	def make_list(self, steps, start, distance, reading):
		self.scan_filter = []
		msg_ranges_lenght = len(reading.ranges)
		for i in range(steps):
			if reading.ranges[start] >= self.LIDAR_ERR and reading.ranges[start] <= distance:
				self.scan_filter.append(reading.ranges[start])
			start = (start + 1) % msg_ranges_lenght
		'''with open('turtle70.csv', 'a') as f:
			writer = csv.writer(f)
			writer.writerow(self.scan_filter)'''

	def obstacle_cone(self, direction):
		print(self.scan_filter)
		if self.checkList(self.scan_filter, 0.13, 0.24, 2) == True:
			print('hit')
			self.pub.publish(direction)
			self.nothing_sent = 0
			time.sleep(0.3)
			self.pub.publish('turtle_hit')
			time.sleep(0.5)

	def obstacle_not_cone(self, direction):
			if len(self.scan_filter)-(-23*np.mean(self.scan_filter)+13) >= 0:
				self.pub.publish(direction)
				print(direction)
				self.is_detected = 1
				self.nothing_sent = 0

			elif self.is_detected == 0 and self.nothing_sent == 0:
				self.pub.publish('Nothing')
				self.nothing_sent = 1
				#print('Nothing')

			else:
				self.is_detected = 0
							


	def checkList(self, the_list, minimum, maximum, chunk):
		for i in range(len(the_list)-1):
			if the_list[i] >= minimum and the_list[i] <= maximum:
				hits = 1
				for j in range(1,chunk):
					ite = i+j
					try:
						if the_list[ite] >= minimum and the_list[ite] <= maximum:
							hits +=1
						if hits == chunk:
							return True
					
					except IndexError:
						return False
		return False  


def main():
	#rospy.init_node('turtlebot3_obstacle')
	try:
		obstacle = Obstacle()
	except rospy.ROSInterruptException:
		pass

if __name__ == '__main__':
	main()
