class Player():
	def __init__(self, **kwargs):
	   
		self.player_info = {}
		for key, value in kwargs.items():
			self.player_info[key] = value
			
		self.max_lin_speed = 0.22
		self.max_ang_speed = 2.84
		self.lin_speed = self.max_lin_speed
		self.ang_speed = self.max_ang_speed
		self.image = ''
		self.control_mode = ''
		self.flip_directions = False
		
	def change_settings(self, settings, keys, values):
		for key, value in zip(keys, values):
			settings[key] = value

	def set_angular(self, ang_lin=0.8, ang_ang=0.2):
		"""Sets speed values for curved movement"""
		self.ang_lin = ang_lin * self.lin_speed #New linear speed for curved movement
		self.ang_ang = ang_ang * self.ang_speed #New angular speed for curved movement    
	def easy(self):
		self.lin_speed = 1.0 * self.max_lin_speed
		self.ang_speed = 0.25 * self.max_ang_speed
		self.control_mode = 'eight_way'
		self.set_angular()
	def medium(self):
		self.lin_speed = 0.8 * self.max_lin_speed
		self.ang_speed = 0.5 * self.max_ang_speed
		self.control_mode = 'four_way'
		#self.set_angular() 
	def hard(self):
		self.lin_speed = 0.6 * self.max_lin_speed
		self.ang_speed = 0.75 * self.max_ang_speed
		self.control_mode = 'four_way'
		#self.set_angular()
	def very_hard(self):
		self.lin_speed = 0.4 * self.max_lin_speed
		self.ang_speed = 1.0 * self.max_ang_speed
		self.control_mode = 'angular'
		self.set_angular()
	def new_difficulty(self, difficulty_params):
		"""Function intended to create a new difficulty based on
		difficulty parameters from a dictionary"""
		self.lin_speed = difficulty_params['lin_scale'] * self.max_lin_speed
		self.ang_speed = difficulty_params['ang_scale'] * self.max_ang_speed
		self.control_mode = difficulty_params['control_mode']
		self.set_angular()
	
	
if __name__ == '__main__':
	def make_dict(keys, values):
		"""Takes a list of keys and a list of values
		and returns dictionary made from them"""
		d = {}
		for key, value in zip(keys, values):
			d[key]=value
		return d

	player = Player(name='player', robot='192.168.1.x')
	print(player.player_info)
	player.change_settings(player.player_info, ['name', 'robot'], ['nina', '192.168'])
	print(player.player_info)
	print(-player.lin_speed)
	print(make_dict(['lin', 'ang'], [-player.lin_speed, player.ang_speed]))
