
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

state = 'Nothing'
rospy.Subscriber("/state", String, state)


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
		
		if state == 'Cone_hit'
			self.checkList(self.scan_filter, 0.14, 0.18, 5)



		#print(start)

		if np.mean(self.scan_filter) >= 0.18 and len(self.scan_filter) >= 10:
			self.checkList(self.scan_filter, 0.17, 0.19, 10)
			if self.checkList() == True:
				self.pub.publish(direction)
				print(direction)
				self.is_detected = 1

		elif np.mean(self.scan_filter) >= 0.195 and len(self.scan_filter) >= 9:
			self.checkList(self.scan_filter, 0.185, 0.25, 9)
			if self.checkList == True:
				self.pub.publish(direction)
				print(direction)
				self.is_detected = 1

		elif np.mean(self.scan_filter) >= 0.222 and len(self.scan_filter) >= 8:
			self.checkList(self.scan_filter, 0.212, 0.232, 8)
			if self.checkList() == True:
				self.pub.publish(direction)
				print(direction)
				self.is_detected = 1

		elif np.mean(self.scan_filter) >= 0.271 and len(self.scan_filter) >= 6:
			self.checkList(self.scan_filter, 0.261, 0.281, 6)
			if self.checkList == True:
				self.pub.publish(direction)
				print(direction)
				self.is_detected = 1

		elif np.mean(self.scan_filter) >= 0.291 and len(self.scan_filter) >= 3:
			self.checkList(self.scan_filter, 0.28, 0.3, 3)
			if self.checkList() == True:
				self.pub.publish(direction)
				print(direction)
				self.is_detected = 1


		elif self.is_detected == 0:
			self.pub.publish('Nothing')
			#print('Nothing')

		else:
			self.is_detected = 0

	def checkList(self, the_list, minimum, maximum, chunk, direction):
		for i in range(len(the_list)-1):
			if the_list[i] >= minimum and the_list[i] <= maximum:
				hits = 1
				for j in range(1,chunk):
					ite = i+j
					try:
						if the_list[ite] >= minimum and the_list[ite] <= maximum:
							hits +=1
						if hits == chunk and state is not 'Going_Back':
							return True
					
					except IndexError:
						return False
		return False  

def state(data): #Subscriber which listen to topic state
	global state 
	state = data.data


def main():
	#rospy.init_node('turtlebot3_obstacle')
	try:
		obstacle = Obstacle()
	except rospy.ROSInterruptException:
		pass

if __name__ == '__main__':
	main()
