import random
import time
class Player():
	def __init__(self, **kwargs):
	   
		self.player_info = {}
		for key, value in kwargs.items():
			self.player_info[key] = value
			
		self.max_lin_speed = 0.22 # Turtlebot 3 max speed (m/S)
		self.max_ang_speed = 2.84 # Turtlebot 3 max speed (r/s)
		self.speeds = {}
		self.speeds['lin'] = self.max_lin_speed
		self.speeds['ang'] = self.max_ang_speed
		#self.image = ''
		self.control_mode = '' # Determines the joystick mode
		self.flip_directions = False # Determines if directions should be randomly flipped when driving
		self.flipped = False # Keeps track of whether directions have been flipped or not
		self.flip_chance = 1

	def change_settings(self, settings, keys, values):
		"""change or add one or multiple key-value pairs of a given dictionary
		settings: dictionary to change\nkeys: list of keys to change or add\n
		values: list of values corresponding to the keys by index"""
		for key, value in zip(keys, values):
			settings[key] = value

	def set_angular(self, ang_lin=0.8, ang_ang=0.5):
		"""Sets speed values for curved movements"""
		self.speeds['ang_lin'] = round(ang_lin * self.max_lin_speed, 2) #New linear speed for curved movement
		self.speeds['ang_ang'] = round(ang_ang * self.max_ang_speed, 2) #New angular speed for curved movement    

	def very_easy(self):
		try:
			self.speeds['ang'] = 0.5 * self.max_ang_speed
			self.control_mode = 'rotation'
			print('difficulty changed')
			print(self.speeds.items(), self.control_mode, self.flip_directions)
		except:
			print('Did not change all parameters')

	def easy(self):
		try:
			self.speeds['lin'] = 1.0 * self.max_lin_speed
			self.speeds['ang'] = 0.25 * self.max_ang_speed
			self.control_mode = 'eight_way'
			self.set_angular()
			print('difficulty changed')
			print(self.speeds.items(), self.control_mode, self.flip_directions)
		except:
			print('Did not change all parameters')

	def medium(self):
		try:
			self.speeds['lin'] = 1.0 * self.max_lin_speed
			self.speeds['ang'] = 0.5 * self.max_ang_speed
			self.control_mode = 'four_way'
			#self.set_angular() 
			print('difficulty changed')
			print(self.speeds.items(), self.control_mode, self.flip_directions)
		except:
			print('Did not change all parameters')

	def hard(self):
		try:
			self.speeds['lin'] = 1.0 * self.max_lin_speed
			self.speeds['ang'] = 0.75 * self.max_ang_speed
			self.control_mode = 'four_way'
			#self.set_angular()
			print('difficulty changed')
			print(self.speeds.items(), self.control_mode, self.flip_directions)
		except:
			print('Did not change all parameters')

	def very_hard(self):
		try:
			self.speeds['lin'] = 1.0 * self.max_lin_speed
			self.speeds['ang'] = 1.0 * self.max_ang_speed
			self.control_mode = 'angular'
			self.set_angular()
			print('difficulty changed')
			print(self.speeds.items(), self.control_mode, self.flip_directions)
		except:
			print('Did not change all parameters')


	def new_difficulty(self, difficulty_params):
		"""Function intended to create a new difficulty based on
		difficulty parameters from a dictionary"""
		self.speeds['lin'] = difficulty_params['lin_scale'] * self.max_lin_speed
		self.speeds['ang'] = difficulty_params['ang_scale'] * self.max_ang_speed
		self.control_mode = difficulty_params['control_mode']
		self.set_angular()
		
	def flip_direction(self, probability_of_flipping=0.01):
		odds = random.random() #Pick a random fraction between 0 and 1
		if odds < probability_of_flipping:
			for key, value in self.speeds.items(): 
				self.speeds[key] = -value
				if not self.flipped:
					self.flipped = True
				else:
					self.flipped = False

	def reverse_directions(self):
		"""Reverses directions to return to default after flipping. 
			Can also be applied to accomodate left-handed participants"""
		for key, value in self.speeds.items():
			self.speeds[key] = -value
			self.flipped = False
	
	


#Should possibly encapsulate the send_dict lines in the Joystick file
	def accelerate(self, rate): 
		#Send increasing fractions of respective members of self.speeds until the targeted speed is reached
		#param rate specifies how much the fraction should increase i.e. how fast to accelerate
		#the function should return as soon as the joystick direction changes
		#Maybe it is possible to return and store the fraction it reached before returning and continue with this value if direction was not changes since returning
		pass

# Should possibly be used when the joystick is idle and every time the joystick direction is changed or flip direction is changed
	def decelerate(self, rate): 
		#Gradually set every speed value to 0
		#maybe use the same fraction as accelerate to continue from the speed where it left off. (like a car)
		pass
	
if __name__ == '__main__':
	random.seed()
	counter = 0
	for i in range(1000):
		odds = random.random()
		if odds < 0.01:
			counter += 1
	print(counter)

	s = -3
	d = -s
	print(d)
	
